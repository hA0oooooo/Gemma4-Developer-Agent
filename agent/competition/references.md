##### 官方来源

访问日期按下表与各研究条目记录，原始基础索引最早于 2026-10-01 整理；后续静态复读不代表已复现公开分数

| Title | URL | Purpose | Access Date |
| --- | --- | --- | --- |
| Competition / Overview | https://www.kaggle.com/competitions/gemma-4-developer-agent | 名称、timeline、模型约束、提交格式与奖金 | 2026-10-01 |
| Competition Data | https://www.kaggle.com/competitions/gemma-4-developer-agent/data | 认证 CLI 已列出 524 个官方文件，包含 guide 与 sample_submission | 2026-10-01 |
| Harness & Competitor Guide | https://www.kaggle.com/competitions/gemma-4-developer-agent/data | 官方 HARNESS_README.md，完整原文保存 agent/harness/official_guide.md | 2026-10-13 |
| Competition Rules | https://www.kaggle.com/competitions/gemma-4-developer-agent/rules | 登录浏览器完整核验，提交次数、外部资源与 winner obligations | 2026-10-01 |
| Competition Code | https://www.kaggle.com/competitions/gemma-4-developer-agent/code | 用户于 2026-10-14 授权参考公开 Notebook；只读源码，不直接执行整份 Notebook | 2026-10-14 |
| Paper Track | https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/overview | 独立论文赛道入口 | 2026-10-01 |
| Official SDK Wheelhouse | https://www.kaggle.com/datasets/metric/gemma-4-developer-agent-wheelhouse | 已下载至 data/wheelhouse 并安装当前官方包 | 2026-10-13 |
| Host SDK clarification | https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/743800 | Kaggle Staff 确认 wheelhouse 为准，不支持 ADK 2.x | 2026-10-01 |
| Development model | https://www.kaggle.com/models/google/gemma-4/Other/gemma-4-12b-it-qat-w4a16-ct | 已下载官方 12B 量化权重；31B、E4B、E2B 也在当前官方允许列表 | 2026-10-13 |

##### 下载记录

2026-10-13 已完整拉取官方 [Getting Started Notebook](https://www.kaggle.com/code/ryanholbrook/getting-started-gemma-4-developer-agent/notebook)，原始源码保存 [getting_started.ipynb](getting_started.ipynb)，最新代码对照与 Linux 适配见 [official_starter.md](../workflow/official_starter.md)

当前官方 Notebook 默认使用 12B，列出四种模型，并使用新的 Evaluator 参数；此前 2026-10-01 的模型与 SDK 记录是旧快照，后续应先阅读上述适配说明

使用此前已认证的 Kaggle CLI 下载官方 HARNESS_README.md，账号可访问该文件，无需提供新 token

保留下载原文，不修改官方内容；文档中具体字段和默认值需在后续安装官方 SDK 后交叉检查

已下载官方 guide、完整 sample_submission、tasks.jsonl、fastapi_15661 snapshot 和五个核心 SDK wheels；未下载第三方 Notebook 或 clone GitHub 仓库

Notebook 开发状态和安装排障记录见 agent/workflow/baseline.md，包存在或导入成功不等于完整 issue 已评测

Google / DeepMind 的一般 ADK 文档不能自动替代本比赛受限配置 schema，当前以比赛 guide 为准

##### 策略来源与证据边界

2026-10-14 通过已认证 Kaggle API 读取以下四份公开源码，原文只存服务器临时目录，不新增持久化 Notebook 副本，不执行其中的数据分析、gold 标签提取或打包代码

| 来源 | 实际源码内容 | 可以借鉴与不能推出的结论 |
| --- | --- | --- |
| [GEMMA: EDA, Baseline for a start](https://www.kaggle.com/code/romanrozen/gemma-eda-baseline-for-a-start-lb-top-1) | 默认 coder + 只读 analyzer；8192 output / 4096 thinking；定位、复现、编辑、编译、临近测试、diff 审核；另含使用公开 gold 文件标签的定位分析 | 借鉴精确标识符搜索、短报告、缩进保持、临近回归测试、scratch 放 /tmp；不运行 gold 分析，不把页面标注 0.12 当作当前代码已复现成绩 |
| [Black Cat SWE Agent](https://www.kaggle.com/code/lucifer19/black-cat-swe-agent-pack-instinct) | CPU 打包；嵌入保留锚点及新候选；锚点 prompt 与上面 Notebook 相同；新候选增加有界 BM25 多视角定位、源码展示和测试 skill | 两份相同 prompt 不是独立实验支持；作者明确区分已计分锚点与尚未证明的新候选，不能把新定位脚本归因到 0.12；只静态解码读取嵌入文本 ZIP，未执行其脚本 |
| [Gemma4 Localization Repaired](https://www.kaggle.com/code/woldywei/gemma4-localization-repaired) | 修复 async-aware 代码图，比较 TF-IDF、embedding、PPR、RRF 的文件/函数定位；gold patch 用于定位指标 | 定位 Hit@k 不等于完整任务 resolved；仅借鉴审计图覆盖与词法检索回退的方向，不读取任务答案，不修改官方图 |
| [Multi-Agent + Graph-RAG Base](https://www.kaggle.com/code/dedquoc/google-gemma4-multi-agent-graph-rag-base) | 反复覆盖多个打包模板；最终 coder + analyzer、8192/4096、60 calls；复制 sample adapter，输入缺失时创建空占位目录 | 这是配置参考而非可靠修复证据；不能将示例 adapter 称作自行训练且有效的策略权重，也不能复制空 adapter 或直接执行全部单元 |

上述 Notebook 页面或作者文字里的成绩未由我们的独立 GPU 实验复现；公开分享的存在不保证兼容当前官方 SDK，也不保证候选收益

##### 论文机制与本比赛映射

| 原始论文 | 可迁移的机制 | 在当前项目中的约束与实验 |
| --- | --- | --- |
| [SWE-agent](https://arxiv.org/html/2405.15793v3) | 简单紧凑的操作接口、有行号的短窗口、编辑后反馈和语法检查；减少重复与过长 observation | 官方工具不能任意替换，先通过 prompt 与允许的 skill 组织调用；检查工具参数、源码导入路径、编译和既有回归测试；论文模型与任务不同，不能套用其修复率 |
| [Agentless](https://arxiv.org/html/2407.01489v2) | 文件→符号→编辑位置的层级定位，修复与验证分离，多候选后以测试及归一化补丁选择 | 先研究短阶段流程；SequentialAgent 仍共享全局工具预算，不自动获得阶段配额；生成的复现测试可能错误，必须结合仓库已有测试，不能使用官方 verifier 标签给同次 Agent 提示 |
| [SWE-Search](https://arxiv.org/html/2410.20285v1) | 多路径搜索、执行反馈与迭代修正，不沿错误假设无限延伸 | 后续再考虑候选分支/评审；完整 MCTS 需要额外状态和预算，不能直接把作者框架 Python 当作本比赛声明式提交 |
| [Beyond the Model](https://arxiv.org/html/2609.32459v1) | Harness 组件效果依赖任务与模型；结构化工具和特定职责分工比盲目增加通用子 Agent 更值得审计 | 其组件实验主要在其他模型与 ProgramBench 上，不能推出 Gemma4 必然获益；以同模型同任务配对实验验证，不先上复杂架构 |

##### 当前直觉与优先级

这里的直觉来自已学到的一般知识，不表示能够查询或识别训练语料，也不是实测结论

1. 优先检查测试是否执行了当前源码，再约束小补丁与回归测试；服务正常、打印预期结果、非空 diff 都不足以证明修复
2. 精确符号优先，词法/图检索作补充；先提升定位到有效编辑的转化，而不是增加思考 token 或 Agent 数量
3. 短生命周期的定位、编辑、验证职责可能减少错误累积，但全局预算与状态传递必须实测
4. 多候选采样与测试选择在单路径能稳定产生有效补丁后再研究；现有失败候选不正式提交

当前优先实验仅替换根 prompt：强调真实源码导入、既有测试前后对照、保留原有行为、先清理再 submit；模型、工具、采样与任务预算保持上轮候选不变。新 prompt 是上述原则的原创整合，不复制社区脚本或 gold 答案

该候选实测仍为空补丁，完整结果见 research.md；新证据显示带多余引号的范围参数没有生效、导致重复读取。因此“更清楚的自然语言流程”尚未有效，下一步按 SWE-agent 的接口设计原则定位原始工具输出/解析问题，再测试更简单的读取动作。论文机制只提供假设，不替代实验结果

##### 新增来源 — 2026-10-15

已通过已认证 Kaggle API 静态读取 [Gemma 4 Agent Working Baseline](https://www.kaggle.com/code/leoprovorov/gemma-4-agent-working-baseline) 的原始 Notebook，9.7 KB，临时保存但不执行其单元。源码为单 Agent、31B、8192 output / 4096 thinking、28 calls / 8 分钟 / 命令 240 秒，强调有限探索、及时编辑、定向测试通过后立即提交，抑制无结果图查询

作者声称进行过 129 次本地运行并据此拟合预算；我们没有取得其原始配对评测，不能将这些文字或页面分数当成本项目已确认收益，也不采纳无证据忽略测试失败的做法。其验证超时说明不适用于当前官方 SDK：本地 HarnessLimits.verification_timeout_seconds 实测默认 300，官方 guide 表格也说明评分端固定 300 秒；不能把 Agent 命令上限直接等同验证上限，也不因此盲目将命令时间改成 240 秒

[Scaling Test-Time Compute for Agentic Coding](https://arxiv.org/html/2604.16529v1) 的原始论文研究以短结构化轨迹总结进行候选选择和后续尝试复用，而不是简单追加单次思考 token。可借鉴“保留假设、进展、失败原因，剔除低信息输出”的表示思路；其前沿模型和其他基准结果不能直接迁移为 Gemma4 分数，也不能把官方 verifier 标签作为后续同任务模型输入

新增来源仅形成 [分类优化台账](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/optimizations.md) 中的假设，正式正向计数仍须由本项目对照实验产生

[SWE-Edit](https://arxiv.org/html/2604.26102v1) 将源码查看、修复推理和格式化编辑区分，提示一种可能机制：定位产生的大量上下文与精确编辑要求互相干扰。当前只借鉴无需训练的职责和接口设计，不采用其训练方案，也不把论文在其他模型上的收益当作 Gemma 成果；已有三阶段对照与小片段编辑实验分别检验相关机制

[LocAgent](https://aclanthology.org/2025.acl-long.426/) 使用代码图辅助定位，适合作为后续图检索对照的来源。定位正确率与最终任务修复率是不同指标，不能因论文的定位结果就默认本比赛的图工具优于词法和符号查看；目前尚未据此登记正向点

进一步读取 [LocAgent 方法原文](https://arxiv.org/html/2503.09089v2) 后，本地只借鉴“符号检索、关系遍历、源码确认”的分工；论文的完整实体源码接口与当前比赛的 induced-subgraph 接口不同，不直接照搬名称或训练结果。graph-localization 对照使用现有公开图，不训练或重写官方输入，具体 API 边界见 [上下文与接口](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/context_and_tools.md)

已静态下载并检查 [Gemma 4 AST Graph-Augmented SWE Multi-Agent System](https://www.kaggle.com/code/avikdas567/gemma-4-ast-graph-augmented-swe-multi-agent-system)，78,779 字节、39 个单元，SHA256 为 2f45816df9482c3a73760a030e5a6f4ed6d5d50b2309fe54b7686ac5172f7a9d。未执行 Notebook，不使用 EDA 输出或参考补丁；其根 Agent 加分析子 Agent 的结构接近官方示例，没有取得足以证明本项目收益的配对轨迹

该源码在缺少 adapter 文件时有写入 512 字节零填充占位文件的分支，并在部分运行阶段捕获异常；不采用该占位分支，也不把 Notebook 页面完成或打包成功当作真实 LoRA、模型运行或测试通过证据。这里只提取通用的接口与流程参考，不移植其整套配置

重新核对 SWE-agent 第 3 节的编辑接口：成功编辑后直接展示实际更新源码，错误编辑撤回并给反馈。本地 edit-feedback 仅测试成功写入后的有限源码反馈，不照搬其完整编辑器，也不把其他模型上的论文结果当作本比赛提分证据

##### 夜间新方向与证据边界

[The Complexity Trap](https://arxiv.org/html/2508.21433v1) 在其他模型与 SWE-agent 中比较保留原历史、旧观察遮蔽及 LLM 总结；仅为本地减少单次工具观察体量提供假设，不在提交外改写历史，也不将论文成本数字记入本项目计数

[CodeStruct](https://arxiv.org/html/2604.05407v1) 提供按 AST 实体读写的动作空间，并明确不同模型收益与工具错误并非一致。本地 symbol-edit 只测试函数级定位替换与缩进接口，保留其余工具及预算；不是论文完整复现

[MarsCode Agent](https://arxiv.org/html/2409.00899v2) 讨论冲突块式精确编辑、缩进与静态诊断。可供后续失败反馈设计参考，不自动采纳模糊匹配、不训练，也不把其他模型的修复率当作本比赛成绩

[同比赛公开仓库](https://github.com/rlawoals0529/gemma-4-developer-agent) 自述简单单 Agent 得 0.05，而含可选定位、critic、无进展制动的后续方案仍明确为候选。这支持先做对照再加复杂度的研究顺序，不证明其升级策略有效；只静态读取网页，没有克隆或执行社区代码

[匹配版本的 vLLM 工具调用文档](https://docs.vllm.ai/en/v0.19.1/features/tool_calling/) 提出 auto 与 required/named 的约束差异，但本地实际提交 schema 不允许该 tool_config 入口。较新的 [上游 issue](https://github.com/vllm-project/vllm/issues/53363) 涉及其他版本和模型，仅作线索，不能替代本地原始输出证据

[CodeAct 原始论文与作者摘要](https://proceedings.mlr.press/v235/wang24h.html) 研究以可执行 Python 统一动作表示，并包含其独立的训练与解释器系统。本地只测试无训练的双工具命令接口，不使用其数据或模型、不声称有状态解释器或完整复现，收益必须重新由当前 Gemma 配对验证

[vLLM 0.19.1 CUDA Graphs 设计](https://docs.vllm.ai/en/v0.19.1/design/cuda_graphs/) 说明运行模式会按注意力后端能力降级，编译、捕获和执行速度之间有启动及内存取舍。本地只研究开发端显式 profile，不修改 SDK、模型或官方评分；先核对安装版 worker 的真实捕获日志，不能仅凭设置存在就记成性能收益

##### 新增原始论文 — 2026-10-16

[BLAgent](https://arxiv.org/html/2605.17965) 将结构标识符与运行行为分别组织为检索查询，再在有限候选中读源码并排序；源码定位与最终修复仍分开评估。可作为后续查询组织假设，不将其其他模型、SWE-bench Lite 的定位成绩或修复率转记为本项目收益，也不复制文中的任务修复示例

[NameRTS](https://arxiv.org/html/2605.25356) 结合名称依赖图、上下文与既有运行观测选择回归测试，其完整安全性边界包含动态导入、反射与初始运行成本。仅靠同名静态搜索不能声称复现其安全测试选择；当前不缩减官方 verifier 测试，也不因该论文报告的加速登记本项目正向点

静态读取另一份[同比赛公开研究仓库](https://github.com/happyc0der/gemma-swe-agent)，作者区分低速 T4、代理与评分栈的不同结果，并自述相同开发配置重复会波动、工具错误减少也不必然提高修复率。仅借鉴其运行栈核对与反例记录方法，没有克隆或执行代码，没有读取 gold 或复现其分数；不能把代理的参数类型错误直接归因为本机 Gemma / vLLM 错误

[The Devil Is in the Interface](https://arxiv.org/html/2608.11386v1) 在固定能力下比较工具组织方式：结构化原子动作、自然语言检索与 Python 可执行动作各有稳定性、探索和交互成本取舍，简单记事提示未显示一致收益。当前命令接口试验只借鉴动作表示，不将其他模型的结果迁移为 Gemma 收益，也不能把无状态 shell 当作论文解释器

[Agent Retrieval Bench](https://arxiv.org/html/2607.24882v1) 将代码到已有测试、失败轨迹到根因等检索需求分开，明确检索命中不等于补丁通过。支持将本地行为示例作为待测上下文来源，但本项目不导入其 gold 路径、修复 commit 或答案，也不把组件检查算真实修复

[Diagnosis Before Recovery](https://arxiv.org/html/2608.11772v1) 按失败类型选择恢复信息，而非给每次失败堆叠所有指令；其主要实验证据来自交互环境和金融格式任务，不是当前比赛。本地接口恢复只作独立待证策略，不采用论文的训练扩展

已通过官方 CLI 静态取得 [同比赛紧凑提交 Notebook](https://www.kaggle.com/code/nihilisticneuralnet/0-10-gemma-4-developer-agent-submission)，原文保存在 output/research/public-notebooks/compact-submission，未执行单元。源码有多组配置，默认选择 lean，侧重精确检索、已有测试、短唯一编辑和实际检查；不照搬关闭 pytest 插件等环境假设，也不把作者最高成绩归因当前源码或其中某个字段

[vLLM 0.19.1 APC 说明](https://docs.vllm.ai/en/v0.19.1/features/automatic_prefix_caching/) 与 [服务指标定义](https://docs.vllm.ai/en/v0.19.1/usage/metrics/) 用于设计本地前缀缓存消融及实际命中检查，只是性能机制参考，不是本项目已获加速或官方提分

[SWE-Replay](https://arxiv.org/html/2601.22129v1) 通过已有仓库回归测试筛除坏轨迹，再以文件探索状态和推理结构选择中间分支；不是简单增加多次独立采样，也不是使用官方任务隐藏测试来选择。其环境恢复及轨迹续接依赖控制器能力，当前声明式提交不能假定可原样接入，因此先保留为后续可迁移性假设，不修改 Harness 或把作者成绩登记为 Gemma 收益

[Rethinking the Value of Agent-Generated Tests](https://arxiv.org/html/2602.07900v1) 比较改变自写测试倾向后的真实轨迹，测试产出数量变化大于总体修复结果变化，且成本效果依模型而异。它支持将反馈信息和测试数量分开审查，不证明 Gemma 可以不验证，也不支持因生成了测试文件就增加正向计数；当前继续保留仓库既有测试与独立 JUnit 审核

[Gemma 4 官方格式说明](https://ai.google.dev/gemma/docs/core/prompt-formatting-gemma4) 和 [官方函数调用指南](https://ai.google.dev/gemma/docs/capabilities/text/function-calling-gemma4) 区分原生字符串序列化、工具调用循环的推理保留与普通轮次的历史处理；[匹配安装版本的 vLLM 解析器文档](https://docs.vllm.ai/en/v0.19.1/api/vllm/tool_parsers/gemma4_tool_parser/) 提供对应解析行为。它们用于设计原生格式和推理连续性对照，不将 Google 的其他配置性能数字移植为本项目收益，也不绕过比赛 SDK 或直接改官方模板
##### 补充生成与验证来源 — 2026-10-16

[Google 官方 Gemma 4 模型卡](https://ai.google.dev/gemma/docs/core/model_card_4) 当前给出统一采样建议 temperature=1.0、top_p=0.95、top_k=64。仅据此冻结温度单变量复核，不从推荐本身推断编码任务收益，也不把不同温度值计作多个优化点

[Teaching Agents to Code Reliably](https://arxiv.org/html/2610.03984) 将候选覆盖与选择可靠性分开，测试时以补丁树和还原树上的行为差异识别无区分力的复现，并检查既有回归测试。当前只保留可迁移的验证假设，不采用其训练、gold 监督或 oracle；一次差分通过仍不证明完整问题修复，不据论文成绩增加本项目计数

[vLLM 0.19.1 并行与扩展说明](https://docs.vllm.ai/en/v0.19.1/serving/parallelism_scaling/) 区分单卡可容纳模型、单实例张量并行及通信开销，[同版本数据并行说明](https://docs.vllm.ai/en/v0.19.1/serving/data_parallel_deployment/) 解释独立副本与各自 KV 缓存。它们只用于提出固定硬件下的布局假设，不保证 Gemma4 修复保持或本机加速；当前候选是显式多 API 实例，不声称复现原生 DP 协调器
