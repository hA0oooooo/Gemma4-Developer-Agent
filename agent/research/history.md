##### 目标与边界

2026-10-14 用户授权自主开展 Gemma4 比赛研究，使用已有 Linux 与可访问资源，验证候选后按规则与每日额度正式提交；不购买资源、不注入解答或隐藏测试、不将本地结果冒充官方分数

保留 submission/ 为唯一正式配置；研究配置与原始产物放 output/research，固定语义路径保存对照。本文保留原始研究过程，最新计数与分类结论统一维护在 agent/research/optimizations.md 及其分类文档，AGENT.md 作为导航

##### 开发与验证划分：初始记录

以下保留初始选集过程，部分任务已因失败分析转入开发；当前新独立集与正向计数以 agent/research/optimizations.md 为准，不将下列旧验证任务再次声称为未见任务

开发任务：fastapi_15661、requests_7205，均已有探索记录；不能作为独立验证集

独立验证任务在候选形成前固定，跨仓库选取：requests_7427、requests_7505、rich_3472、rich_4006、fastapi_14962、fastapi_9555；按 SHA256("gemma-research-holdout:" + instance_id) 升序，每仓库取前两个，排除已探索的开发任务。只读取 instance_id、repo、base_commit 与公开 problem_statement，不读取解答字段来制定策略。不得针对任务 ID 写策略特判

验证集用于候选验收，不根据失败的具体修复内容改提示；若使用其轨迹继续研究，则须将对应任务转为开发集并另行冻结新的验证集

12B 用于快速筛选；正式配置当前为 31B，12B 结果不能证明 31B 收益。正式切换模型或预算必须通过 schema 校验与实际模型验证，并记录变化

##### 基线证据

12B、单 A6000、官方 runtime 与官方上下文设置，8 tool calls、20 turns、10 分钟、max_output_tokens=1024、thinking_budget=256

fastapi_15661：76.65 秒，8 次工具调用，patch=0，pytest 未进入，resolved=False

requests_7205：101.01 秒，8 次工具调用、10 次模型调用，patch=0，pytest 未进入，resolved=False；trace 多次重复 read_file，同一目标片段反复推理，终态中编辑请求被输出为文本而非实际工具调用

上述结果证明服务与工具可用，未证明任务修复；目前不能断言根因只有工具预算或只有模型能力

##### 实验：推理预算

假设：thinking_budget=256 / max_output_tokens=1024 可能使推理中断，造成反复读取；这是待检验假设，不是已证实根因

只修改生成预算到 thinking_budget=2048 / max_output_tokens=4096，其余提示、工具、8 次调用、20 turns、10 分钟及 12B 模型保持不变。先运行 requests_7205，观察是否产生真实 edit/write/submit_patch、非空补丁与 pytest；即使通过，也需要跨任务独立验证

对照产物：output/research/control；候选配置与结果：output/research/reasoning-budget

结果：requests_7205 耗时 401.22 秒、8 tool calls、11 次模型调用、patch=0、pytest 未进入、resolved=False；累计 prompt=72338、completion=11599 tokens。Agent 从重复读文件转为反复构造格式错误的 netrc 复现脚本，仍未编辑

结论：提高生成预算没有解决此任务的无补丁问题，延迟显著增加；不能将原失败归因为单纯 token 预算不足

##### 实验：关闭 thinking

只在原精简配置中将 thinking_budget 从 256 改为 0，仍为 max_output_tokens=1024、8 次工具调用、20 turns、10 分钟与原提示。检验显式思维循环是否抑制编辑；不向模型加入本任务解答或路径提示

产物：output/research/direct-action；结果：18.31 秒，8 次工具调用、10 次模型调用，patch=0、pytest 未进入、resolved=False。耗时显著下降，但仍在查找/读取代码且出现行号参数错误；关闭 thinking 没有单独解决编辑行为

##### 下一步：模型与阶段控制

准备当前官方 31B 权重，与已有 12B 分开存放；先复用原精简配置，避免把模型切换与多项策略变化混在一起

另准备官方 SequentialAgent 结构：分析阶段返回具体目标与原代码，编辑阶段只开放 edit_file/write_file，验证阶段检查补丁并提交；通过工具可见范围限制重复探索。该方案必须经过 schema 与真实模型检验，尚不能声称有效

分阶段配置已通过官方 validate_directory，仍保持原 8 calls / 20 turns / 10 分钟与 1024/256 生成预算；更改架构及阶段提示是一个联合干预，不把其收益单独归因于某一句提示。requests_7205 的 12B 真实实验已启动

结果：221.65 秒、8 次工具调用、17 次模型调用、patch=0、pytest 未进入、resolved=False。编辑阶段确实尝试 edit_file，但分析阶段已消耗全局工具预算，调用被 BudgetExceeded 拒绝；分析记录还出现了不正确的目标路径。分阶段结构本身不能保证每个阶段都有工具预算，不能宣称架构已经解决问题

##### 实验：放宽会话预算

以关闭 thinking 的候选为对照，只提高会话预算到 32 tool calls / 60 turns，时间仍为 10 分钟；保留原提示、工具与输出 1024。这联合改变工具/turn 上限，用于判断 8 次预算是否直接阻止了已经定位后的编辑，不单独归因于某个上限

产物：output/research/tool-budget；结果：121.92 秒、32 次工具调用、33 次模型调用，agent_patch_size=161、test_exit_code=1、resolved=False。未显式 submit_patch，harness 回收了非空工作树 diff

实际补丁只是新建 .netrc 临时文件，没有修改 Requests 目标源码；写入复现脚本不能当作实现修复。官方验证阶段实际启动 pytest，输出 202 passed / 4 failed / 13 skipped，失败为 Content-Type 参数解析相关测试。没有取得持久 JUnit XML，不能声称完成完整 JUnit 审计；尚未做干净基线对照，不将这四个失败归因于 Agent 的临时文件

结论：真实 Agent→非空 patch 回收→独立验证 pytest 已执行，但 patch 无效、任务未修复；提高预算只解除部分流程门槛，没有带来有效修复

本地 Requests 缺少的公开测试插件已从清华镜像补齐：pytest-httpbin、pytest-cov、pytest-mock、pytest-xdist、httpbin、trustme、PySocks、chardet；pip check 通过。未修改测试文件、官方任务或测试判定逻辑

环境稳定后，用 src/check_patch.py 分别复核空补丁基线与同一 161 字节补丁，均得到 205 passed / 1 failed / 13 skipped，JUnit 均有 219 个 testcase，唯一失败均为 TestGetNetrcAuth::test_empty_default_credentials_ignored；证据保存在 output/research/clean-baseline 与 patch-audit

因此该补丁没有解决目标回归。初次运行的四个 Content-Type 失败未在稳定环境重现，不能归因于 .netrc 文件，也不能作为候选修复率依据；补依赖曾与该次 Agent 运行重叠，后续必须先固定环境再启动对照实验

check_patch.py 只调用官方 verify_task，并在 sandbox 清理前复制其原生 JUnit；不修改官方测试或打分规则，不启动模型

##### 官方配置锚点

复制只读官方 sample_submission 到 output/research/official-anchor/config；使用官方根提示、检索工具与 code_analyzer AgentTool、4096 thinking / 16384 output。仅将演示性的 1 分钟 / 10 calls 改为本地研究 10 分钟 / 32 calls / 60 turns；模型切到 12B 并按官方 Notebook 删除 31B 示例 adapter 引用及占位权重

这不是完全原样 sample 的效果，也不是与前面候选的单变量对照；它用于检查官方提示、检索与分析结构能否改善本地修复行为。requests_7205 真实评测已启动，尚无结论

结果：248.48 秒、5 次工具调用、patch=0、pytest 未进入、resolved=False；16384 输出预留与至少 16385 提示 token 超过 32768，触发 ContextWindowExceededError。当前官方示例的生成参数不能在此实际轨迹下直接保证可运行，不能把 sample 来源等同于成功基线

下一候选保持官方提示、检索及分析结构，改为 output=4096、thinking=1024、include_thoughts=false；不保留历史 thought 片段但当前调用仍允许推理。此联合干预以控制上下文与推理循环为目标，产物 output/research/official-compact

结果：602.55 秒、25 tool calls、27 次模型调用，patch=0、pytest 未进入、resolved=False；没有再次出现上下文溢出，但 Agent 在无效的 netrc 复现命令上循环直到 10 分钟超时。当前参数解决的是窗口溢出，不是有效修复能力

12B 简单算术请求实测返回 2、finish_reason=stop、无 reasoning，证明基础服务输出正常；这不证明代码修复或复杂工具决策能力正常。现阶段不将任何上述失败候选替换正式 submission，也不消耗每日提交去重复验证无效补丁

官方 API 已确认 31B 模型当前 version_number=2，下载到 data/models/31b，不覆盖 data/models/12b 中的 12B；只使用现有服务器资源

权重目录已统一为 data/models/12b 与 data/models/31b；早期 protocol 中的 data/model 是当时的真实路径，保留原始证据，不重写历史产物

下载速度约 1–2 MB/s，已保存前 768 MiB 为 download.part 并启用同一官方模型输入的续传；后台仅进行权重下载，没有训练或自动正式提交。模型尚未就绪，不能报告为已验证 31B

尝试 aria2 并行后没有观察到新增下载数据，已撤回该未验证路径，恢复确实能接收数据的 curl 续传；证书验证始终开启，没有修改系统网络。Mac 小范围探测约 0.45 MB/s，不能据此推出完整模型下载更快，暂不转运权重

已冻结 output/research/model-control/config（当前正式精简配置）与 model-candidate/config（无示例 LoRA 的官方结构紧凑候选），下载完成后在 31B、TP=4 下先做 requests_7205 配对开发检查；候选若 resolved=False，则不触碰独立验证集

后台续接作业保存为 output/research/continue_research.sh，只等待当前下载进程，准备失败或四张 GPU 空闲显存不足则退出，不抢占其他作业；开发检查通过后才运行固定六项独立验证的配对对照，并保存非空补丁的 JUnit 审核。它不执行正式提交，正式候选须在结果审核及规则/额度核验后再决定

##### 环境边界

用户没有 Docker daemon socket 访问权限，2026-10-14 docker info 实测 permission denied。当前真实评测沿用官方 subprocess sandbox，它不是 Docker 容器隔离；依赖兼容性和正式评分一致性须分别审计，不因本地成功自动声称官方收益

##### 官方评分状态

2026-10-14 API 实测 Linux 直接提交 ref=57129840 为 COMPLETE，public_score=0.06；此前相同精简 CPU/GPU 打包分别为 0.05，Mac 中转的另一次为 0.03。没有评分日志，不解释分数差异为硬件或模型收益，也不把单次变化作为实验统计证据

Linux 校验打包→直接提交→官方评分闭环已成立，当前研究要解决的是任务修复率而非提交方式

##### 31B 配对开发结果

官方 31B 权重已完整准备，后台配对作业已结束，四张 A6000 在两轮之间与结束后均释放，没有训练或新正式提交

| 配置 | 时间 | 工具 / 模型调用 | 补丁 | 官方验证 |
| --- | --- | --- | --- | --- |
| 当前精简正式配置的开发副本 | 169.82 秒 | 8 / 13 | 0 字节 | test_exit_code=1，resolved=False |
| 官方结构紧凑候选 | 317.74 秒 | 22 / 24 | 1609 字节 | test_exit_code=1，resolved=False；干净副本复核与 JUnit 已保存 |

结果路径：output/research/model-control/requests_7205 与 output/research/model-candidate/requests_7205。候选 JUnit 为 205 passed、1 failed、13 skipped；之前目标空凭据用例不再失败，但产生了普通 URL 的新回归，失败为 TypeError。这说明候选首次完成源码编辑及 submit_patch，但不是正确修复

候选只测试自行写的复现脚本和改写的模拟函数，没有跑仓库既有 pytest，也没有记录导入模块的 __file__；修改前后复现均打印 Auth: None，因此这些输出不能证明针对本 checkout 的有效修复。疑似测试了环境已安装包，尚未直接取得当时导入路径证据，不能把该假设写成已证实根因

补丁还包含两个临时复现文件；Agent 先 submit 后清理，清理没有改变已捕获补丁。下一策略只编码通用的测试来源、回归检查与先清理再提交规则，不编码该任务的函数、文件路径、条件表达式或 verifier 返回的具体测试名

固定六项独立验证集保持未使用；上轮候选开发未通过，后台作业按计划停止

##### 公开来源驱动的验证闭环候选

来源与可迁移边界见 agent/competition/references.md 的策略来源段。源码只读分析，没有执行社区 Notebook，也没有将任务 gold patch 输入模型

新候选 output/research/verified-edit/config 从 model-candidate/config 复制，仅替换根 prompts/system.md；保持同一 31B、TP=4、工具与 analyzer、4096 output / 1024 thinking、32 calls / 60 turns / 10 分钟。根提示整体替换属于联合提示干预，不声称可归因到某一个句子

预期观察：真实工具 edit_file、checkout 源码导入检查、仓库既有测试、失败反馈后再编辑、无 scratch 污染、最后 submit_patch；最终仍以干净副本官方 verify_task 和 JUnit 判定。先在已有开发任务检查，开发通过再固定候选，独立验证与控制配对；未经验证不替换 submission 或正式提交

结果：314.02 秒、32 tool calls / 34 模型调用、patch=0、test_exit_code=1、resolved=False；没有编辑或 Agent 侧 pytest，没有达到预期，因此不提升为正式配置，独立验证集仍不动，四张 GPU 已释放

轨迹发现具体工具接口错误：例如 step 5 的参数键为 `start_line"`、`end_line"`，而非 schema 要求的 start_line、end_line；Agent 请求 1000–1084 行，工具实际返回 1–150 行且 is_truncated=true。多个带引号的范围键及同一读取反复出现，累计 prompt=316578 tokens，completion=3348 tokens。这是已观察到的参数/反馈失配，不足以区分模型原始输出与 vLLM/ADK 解析责任；下一步先检查原始工具响应与解析链，并尝试范围参数明确或只用短 shell 读取的受控接口实验，不直接改官方 harness

同轮 Evaluator 日志报告 202 passed、4 failed、13 skipped，失败为 Content-Type 用例；随后不改环境、不启动模型的独立官方 verify_task 审核同一干净 snapshot 为 205 passed、1 failed、13 skipped，只有目标空凭据用例失败，JUnit 已保存 output/research/verified-edit/requests_7205/audit。两种执行路径的差异尚未解释，不能将这四个失败归因于模型，更不能用不一致的测试计数评价策略收益；空补丁与参数失配的结论不依赖此差异

当前不新增正式提交，不训练，不修改 submission 或 data/competition。后续优先级为工具参数解析/反馈一致性→Agent 侧真实源码与回归验证→冻结候选的独立配对评测→按规则正式评分；不凭公开 Notebook 的标题或论文报告直接声称提分

##### 本地验证路径修正 — 2026-10-15

无模型配对检查已定位测试差异：官方 SubprocessManager 的 exec 只将 workspace 根加入 PYTHONPATH；对于 src 布局，setup 又依据精确类名跳过 editable 安装，导致 Python 实际导入宿主已安装的 Requests。路径探针实测 native 导入 site-packages/requests，而加入 /workspace/src:/workspace 后导入当前 sandbox 的 workspace/src/requests

同一干净 snapshot、同一原生 manager 与官方 verify_task，未改任务或测试：native 为 202 passed、4 failed、13 skipped；仅修正源码导入路径后为 205 passed、1 failed、13 skipped。前者四个 Content-Type 失败不是该 snapshot 的有效策略结果

此前 check_patch.py 使用 ArtifactSandbox 子类保留 JUnit，意外改变了官方 setup 的精确类名分支，因此不能说它与 Evaluator 原先执行环境一致。现已删除该子类，新增 src/local_sandbox.py，在原生 manager 实例上适配源码导入与 JUnit 保存；run_baseline、run_local_mock 和 check_patch 统一调用它，没有编辑已安装 SDK、官方数据或测试，保持官方返回的 resolved 判据

修正后的无模型 Evaluator 与独立 audit 都得到 test_exit_code=1、resolved=False，并保存 JUnit；模拟链路仍为 273 字节 patch、test_exit_code=2，只证明工具→补丁→验证调用链，不是任务修复成功。pyflakes 与 pip check 均通过。历史模型结果中的原始测试计数保留，但后续以当前源码导入的独立验证重新判读，不据旧计数选择策略

这仍是 subprocess 适配，不等于 Docker 隔离或官方评分环境完全一致。任务依赖现改为安装进每个 sandbox 自己的 venv，避免跨仓库依赖污染模型服务；test_deps.json 记录 install_scope=task_venv、每次实际 pip 退出码与输出尾部。跨仓库实验仍须检查兼容性、保持对照环境一致，不把环境失败当模型失败

##### 简化源码导航候选

output/research/shell-navigation/config 从官方结构紧凑候选复制：根 Agent 移除 read_file，可选行号参数不再进入根 Agent 的调用路径；根提示明确以 grep -n / sed -n / nl 做短窗口源码阅读，编辑仍用官方 edit_file、提交仍用 submit_patch，保留只读 analyzer 作难定位任务的后备。analyzer 未改，不声称所有子 Agent 的范围参数都已修好

模型仍为同一官方 31B、TP=4、4096 output / 1024 thinking、32 tool calls / 60 turns / 10 分钟；无 adapter、无训练、无任务特判。提示与导航接口为联合干预，不能将结果归因到单一提示句；本地 source-path 适配是验证修正，不算候选策略增益

先对 requests_7205 做开发检查；若成功，独立复核补丁与 JUnit，再冻结该配置并对原定六项独立集及正式低预算控制做配对评测。输入准备只增量下载官方缺失 snapshot/graph/embedding，不改现有原始文件。验收要求完成六项、候选 resolved 多于控制且没有已解决任务的回归；环境失败需单独处理，不能算作公平胜负。满足这些条件后再核验最新规则与额度，决定是否正式提交一次；失败候选不重复提交

结果：386.36 秒、29 tool calls / 31 模型调用、2014 字节 patch、test_exit_code=1、resolved=False。消除了根 Agent 的错误行号读取循环并产生真实编辑，但仍将原有保护条件错误替换，且遗留复现文件；新的 task-venv 独立审核同样失败，因此不进入独立集

##### 更强提示的边界

output/research/focused-repair 进一步减少为 run_command、edit_file、get_status、submit_patch 四个工具，要求先编辑后运行既有测试，不创建复现脚本；其余 31B、4096/1024、32 calls、60 turns、10 分钟不变

结果：601.32 秒、27 tool calls / 29 模型调用、1321 字节 patch、test_exit_code=1、resolved=False。模型仍绕过提示，通过 run_command 创建并重复运行复现脚本，保留错误修改与临时文件。仅在提示中禁止探索、减少工具名称，没有形成足够的行为约束

##### 环境与格式检查补充

不依赖任务答案的直接 API 探针，仅要求读取虚构 pkg/example.py 的 200–240 行；原始生成 token 为正常 Gemma4 工具格式，解析后的 filepath/start_line/end_line 均正确。此前错误参数仍属真实轨迹问题，但不能据此声称解析器对所有请求都错误；没有修改 vLLM/ADK 解析器或评分工具

固定 FastAPI 验证任务的空补丁环境检查暴露 ModuleNotFoundError: inline_snapshot。其 pyproject 声明 PEP 735 dependency-groups.tests，旧依赖收集器未处理该组及 include-group。现按声明递归补齐测试组，缓存与声明下限一致的 inline-snapshot==0.21.1 及其依赖到 data/local-wheels，通过清华镜像下载，实际安装仍在 task venv；缓存已加入 gitignore，不修改官方 wheels 或测试

补充命令：python -m pip download --only-binary=:all: --dest data/local-wheels --index-url https://pypi.tuna.tsinghua.edu.cn/simple inline-snapshot==0.21.1

补齐后测试可以加载，空补丁 test_exit_code 从 2 变为 1，剩余断言失败与快照不匹配 teardown 报告仍保留；不能把后者称为缺包或自动忽略。这里只用环境异常修复依赖，没有利用独立任务的修复内容修改 Agent 提示，六项模型对照仍使用事先冻结的任务集。宿主 pip check 通过，模型服务依赖未被测试安装升级

##### 三阶段候选与首次开发通过

output/research/staged-repair/config 使用官方 SequentialAgent，以职责和可用工具组织行为，不提供任务特判、gold patch、额外模型或训练

| 阶段 | 可用工具 | 交接 |
| --- | --- | --- |
| source_locator | run_command，职责限定为检索源码与既有测试 | source_context，包含当前源码和定位结果 |
| implementation_editor | edit_file、write_file，没有执行命令工具 | implementation_report，完成实际修改后返回 |
| implementation_reviewer | run_command、edit_file、get_status、submit_patch | 检查 diff、执行测试、修正回归并提交 |

run_command 本身不是机械只读，因此定位阶段的只读职责仍依赖提示；编辑阶段不提供执行工具，才实际阻断其执行复现循环。编辑与审核使用 include_contents=none 加状态交接；已核对当前 ADK 实现，这会保留当前轮工具上下文，并非清空所有工具反馈

所有阶段共用同一 31B 服务、4096 output / 1024 thinking、全局 32 calls / 60 turns / 10 分钟；不是每阶段各获得一份预算。配置通过 schema、实际 SDK 编译与 pyflakes 检查，没有载入三份基座模型

requests_7205 结果：455.32 秒、16 tool calls / 20 模型调用、503 字节单文件源码 patch、test_exit_code=0、resolved=True、error=None。定位阶段完成交接，编辑阶段一次 edit_file 修改源码，审核阶段运行当前 checkout 的 tests/test_utils.py，得到 205 passed、13 skipped，并执行 inline assertions、diff 检查和真实 submit_patch

在另一干净副本上应用同一模型补丁，加入官方 test_patch 后独立 verify_task 仍为 resolved=True、test_exit_code=0；原生 JUnit 共 219 cases，206 passed、13 skipped、0 failures、0 errors。审核产物为 output/research/staged-repair/requests_7205/audit。补丁不含复现文件或测试改动，没有任何人工补丁后处理

这是已反复研究的开发任务，不能将 1/1 当泛化准确率，也不能单独归因到阶段数。单阶段强提示未奏效、三阶段实际完成编辑和审核，是下一轮验证的依据，不是公榜提分结论

##### 当前独立配对作业

开发成功并独立复核后，已冻结配置到 output/research/paired-candidate/config，将当前正式 baseline 复制到 paired-control/config，并启动既定六项任务的串行配对作业。两侧使用相同权重、SDK、源码导入与 task-venv 适配；原 baseline 的低预算配置保留不变

入口 output/research/staged-repair/validate.sh，日志 validation.log；这是一次性计算作业，不是恢复定时监控。开发或复核失败即停止，不启动独立集；资源不足或运行报错停止，不抢占其他进程、不自动重复提交

完整配对结果写 output/research/paired-candidate/summary.json。脚本的 passes_local_gate 只提供产物层初筛，正式决策还须审核环境异常、JUnit、回归、验证路径一致性和整体时间预算；不能将相同的环境失败当作双方公平失分。该作业不修改 submission、不打包正式候选、不创建 Kaggle 提交

首个未参与提示调试的冻结任务 requests_7427 已完成：控制 resolved=False、patch=0、172.99 秒；候选 resolved=True、patch=1077 字节、311.44 秒。两侧独立干净副本审核与各自 Evaluator 结论一致，候选 pytest 退出码为 0、JUnit 已保存。其余五项仍在运行，暂记一次独立胜出，不据 1/6 推断总体准确率或公榜分数，不修改冻结提示

##### 完整配对结论与后续开发

六项配对已结束，原精简 baseline 没有通过任务；三阶段候选在 requests_7427、requests_7505、fastapi_9555 三项通过，非空补丁均经另一干净副本官方 verify_task 审核通过。候选与对照预算不同，这证明候选整体有正向信号，不能单独归因于架构

rich_3472 与 fastapi_14962 因工具预算耗尽失败，原始轨迹的 author 元数据显示定位阶段分别消耗 32 与 31 次 run_command。rich_4006 的两侧官方验证均超时且没有 JUnit，候选同时有会话超时，因此不将该项作为可靠的修复胜负；summary.json 的 passes_local_gate=False 保持原样，不据三次胜出直接正式提交

rich_3472 的定位轨迹现用于下一步接口开发，该任务从此转为开发集，不再声称对后续候选独立。其余已完成结果保留为历史冻结实验，不用具体测试答案编写策略

下一候选 output/research/bounded-navigation/config 仅更换定位阶段：移除 run_command，使用官方允许的 sandbox skill，提供只读 Python 源码关键词检索和符号级原文查看。输出限制为 4300 字符，符号最多 85 行，禁止越出 workspace；不执行仓库代码、不联网、不读取解答或隐藏测试。编辑、审核、模型、采样及全局预算维持原三阶段配置。一次检索加三次查看仍为提示约束，不声称已实现官方框架没有提供的阶段级硬预算

预期证据：定位调用明显少于 31/32 次，能够进入实际编辑、审核与 submit_patch，并在 requests_7205 保留已有修复能力。先对已有开发任务 requests_7205 与新转开发的 rich_3472 检查，再决定是否进入新独立集；运行失败或修复能力退化不替换正式配置

为排除额外预算的混杂，另冻结 budget-matched-control/config：保留原单 Agent 提示和工具，只将预算及 sampling 对齐三阶段候选，先在 requests_7205 作同预算开发对照

新的独立任务在新候选结果产生前按 SHA256("gemma-navigation-holdout:" + instance_id) 每仓库取前两项，排除此前八项已使用任务：requests_7502、requests_6592、rich_3105、rich_3006、fastapi_14482、fastapi_15785。这里只选取任务 ID，不读取修复答案，暂不开始新独立集计算

导航工具首次真实调用暴露本地路径适配问题：skill 的脚本内容中的 /workspace 不会经过 subprocess 命令路径翻译，因此检索为空；已中止该次运行并正常释放 GPU，保留到 bounded-navigation/path-diagnostic，不算作模型策略结果。脚本现使用 sandbox shell 保留的 PWD，而不是 skill 临时解包后的 cwd；实际 ADK skill wrapper 与原生 subprocess 的检索、符号列表、原文读取三项探针均通过，源码与路径边界检查通过。补充 show 缺少 symbol 时返回符号列表，不因可恢复的查看请求直接失败

rich_4006 的空补丁重新审核仍为 124 超时、无 JUnit；公开问题描述本身就是 split_graphemes 死循环，执行时测试进程持续占满一个 CPU。因此超时与任务缺陷一致，不能将其直接归因为环境错误或通过延长时限算作修复。环境变量形式的 pytest 诊断参数被 sandbox 环境过滤，未取得栈证据，故不声称已经定位到具体阻塞栈

随后通过仅用于诊断的 shell 环境前缀开启 pytest faulthandler，45 秒诊断上限内已取得 10 秒时的真实栈：阻塞发生在当前 checkout 的 rich/cells.py::split_graphemes，调用方为 chop_cells；不是下载、权限或缺包等待。原始无补丁与两侧补丁的 300 秒验证超时均不改写为成功；诊断另存 verification-diagnostic/rich_4006/stack，不替代正常评分。此任务也不再用于未来独立验收，不把官方验证测试的具体输入或栈内容传给 Agent

导航代码进一步排除隐藏 Python 文件，避免检索 ADK 临时写入的 .adk_exec 脚本本身。使用真正的 AdkSandboxCodeExecutor（包含写脚本、临时解包、执行、清理）完成检索、符号列表、原文读取与执行包装文件排除检查，全部通过；早期中止检查保留在 path-diagnostic 与 executor-diagnostic。之后冻结候选重新启动开发任务与同预算对照，不修改运行中的配置

##### 只读导航候选的开发结果

requests_7205 已完成：308.46 秒、官方预算计数 tool_calls=8、503 字节单文件源码补丁、test_exit_code=0、resolved=True。另一干净副本官方 verify_task 同样通过；JUnit 219 cases，其中 206 passed、13 skipped、0 failures、0 errors。原三阶段在同一开发任务为 455.32 秒、tool_calls=16、同样 503 字节补丁并通过独立审核

这只是一次已知开发任务的修复保持与速度正向信号，不是独立准确率或稳定加速结论。两种接口的预算计数口径不完全相同：完整轨迹的工具交互为原候选 17 次、新候选 11 次；定位阶段均为 4 次，原候选审核阶段 12 次、新候选 6 次。因此不能把 tool_calls 减半直接解释为定位效率翻倍，也不能将随机轨迹差异单独归因到某条提示或检索算法

首项完成后一次性 develop.sh 已继续 rich_3472，随后执行 budget-matched-control 的 requests_7205；当前尚无这两项结论。正式 submission 不变，无新 Kaggle 提交或定时监控，新独立集尚未执行

##### 后续开发结果与研究目标

rich_3472 的只读导航候选为 484.22 秒、366 字节补丁、resolved=False，独立审核同样失败；定位阶段仍有 24 次脚本执行。因此先前关于“新工具已经控制定位循环”的假设没有被泛化验证支持，只读不等于正确定位或阶段硬预算

budget-matched-control 的 requests_7205 为 216.04 秒、12 次预算计数、1752 字节补丁、resolved=True，独立干净副本审核通过。相比三阶段 455.32 秒、只读导航 308.46 秒，简单单 Agent 同样成功且更快；暂不把多阶段架构计为独立正向机制

用户最初要求持续寻找十项有证据的不同正向优化，于 2026-10-15 将目标提高到二十项并授权夜间继续研究。分类台账现移交 [optimizations.md](../research/optimizations.md)，本文保留原始实验记录而不重复维护逐项状态。旧的 fastapi_9555 转入开发集，新六项独立集保持冻结

第一组新的单因素筛选固定原高预算单 Agent、4096 output、32 calls、60 turns、10 分钟与官方 31B，仅比较 1024 / 256 / 0 thinking，两个开发任务、两个种子，共十二项。各 case 使用新的任务环境与独立复核；src/run_experiments.py 只复用同一模型服务，不复用会话或工作树，不修改官方 SDK

原单任务 runner 通过提取 prepare_case、create_server、evaluate_case 共用实现保留既有入口，新增 seed 与实际配置哈希记录；pyflakes、CLI 参数和模拟链路检查通过，真实共享服务集成及参数筛选正在执行。模拟 resolved=0 不是模型质量结果，正式提交配置保持未变
