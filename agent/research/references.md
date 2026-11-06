##### 研究补充来源

完整官方、公开 Notebook 与既有论文索引见 [统一来源索引](../competition/references.md)，这里仅记录后续研究补充，不重复维护官方目录

##### 本轮公开方法筛选

2026-10-19 静态查阅，不下载、执行、复制或部署社区Notebook，不把外部成绩写成本项目收益

| 来源 | 实际核对 | 可迁移假设与边界 |
| --- | --- | --- |
| [Budget-Fit已评分页面](https://www.kaggle.com/code/samvalladares/gemma-4-agent-budget-fit-single-agent?scriptVersionId=355976064)与[对应日志](https://www.kaggle.com/code/samvalladares/gemma-4-agent-budget-fit-single-agent/log?scriptVersionId=355976064) | 对齐到页面Public Score=0.18的具体artifact；日志显示四文件ZIP、8分钟、28calls、80turns、命令240秒，CPU只用于24秒打包 | 优先做完整预算适配，而不是堆代理；本地6分钟是假设，不是完整复现0.18，不把最新版代码与旧最佳成绩混用 |
| [作者公开实验](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/747696)、[0.17对应评分页](https://www.kaggle.com/code/yiyu0716/g4-pack-yiyu-v19-fixed-trace-t7p5?scriptVersionId=356344238)与[源码目录](https://www.kaggle.com/code/yiyu0716/g4-v19-complete-harness-source/output) | 具体评分页显示Public Score=0.17；正文区分31/129任务、失败与本地专用改动。另读导出目录的Skill说明与g4edit.py跟踪核心，未证明导出源码和已评分ZIP逐字一致 | 借鉴执行路径辅助定位；短编辑与语法保护与既有工具箱重叠，不重复计数。本地时钟补偿、host guard及其scratch清理不照搬，当前原型也不是完整复现 |
| [工作人员关于验证时长的回复](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/743663) | 工作人员估计每题交patch时验证另耗约两小时，无patch任务跳过验证 | 评分墙钟不等于12小时Agent计时；11小时不能单独判异常，也不能忽视明确的Notebook Timeout，具体阶段仍需日志 |

[Analyzing and Mitigating Cost-Inefficient Behaviors in Coding Agents](https://arxiv.org/html/2609.30725v3)是预印本；已读行为分类、方法比较与开发者指导附录。提取按已有上下文、代码状态与新证据决定是否重读/重测，不直接借用其成本百分比；结构化检索也可能增加成本，须做实际作用审核

[Probe-and-Refine Tuning of Repository Guidance](https://arxiv.org/html/2606.20512)是预印本；已读设计、预算实验和限制。指导与步数预算存在交互，复杂复现/跟踪流程在低预算下可能来不及编辑；跨模型结果不支持把Qwen规则原样视作Gemma收益。只迁移先诊断失败、再做受控短指导的方法，不运行其调优模型或将答案标签喂给同次Agent

- [Agentic Bug Reproduction for Effective Automated Program Repair at Google](https://arxiv.org/abs/2502.01821)：公开式 bug report 的行为复现与修复选择参考；其内部代码、模型与训练结果不视为本比赛已复现收益，不引入训练方案
- [Agentless 作者仓库](https://github.com/OpenAutoCoder/Agentless)：仅静态阅读定位、修复与验证流程，不执行社区代码、下载解答或声称完整复现其多候选系统
- [pip install 官方选项](https://pip.pypa.io/en/stable/cli/pip_install/)：--no-compile 只控制安装时字节码工作，开发成本必须计回首次导入、pytest 和环境清理；本项目完整对照未达到冻结收益门槛
- [uv 官方命令说明](https://docs.astral.sh/uv/reference/cli/)：offline、no-index、no-cache、copy 安装及显式 Python 目标可用于本地新鲜测试环境；不使用文档宣传速度作项目收益证据，不改变官方评分安装器
- [ADK Session State 官方说明](https://adk.dev/sessions/state/)：系统指令可引用已存在状态，缺失变量需明确处理；本项目实际可用的公开 problem_description 键另以官方 Guide 与安装版 Harness 源码核对，原生多轮 fixture 验证，不把功能支持当效果证据
- [CodePlan 作者论文概述](https://www.microsoft.com/en-us/research/publication/codeplan-repository-level-coding-using-llms-and-planning-2/)：仓库级修改由有上下文的局部编辑链组织；本项目据此提出匹配角色和编辑粒度的按文件委派假设，不声称实现其增量依赖、影响分析、自适应规划或复现论文成绩
- [Refine 原文](https://arxiv.org/html/2510.03588v1)：实际阅读上下文提取、多样增量与聚合章节，作为修复前比较不同诊断的动机；本地不复现其完整增量池与聚合系统，不用官方 verifier 给同一次修复选择答案
- [The Complexity Trap 原文](https://arxiv.org/html/2508.21433v3)：已读§3.1的旧观察遮蔽与摘要定义、§5.2的摘要调用开销，区分观察体量、模型生成与摘要成本。当前可提交内容不能任意改Harness历史，工具端重复检查回执只是动机迁移，不复现其年龄窗口遮蔽、论文基准或收益；旧短输出、unchanged-views负结果均保留
- [LoRA 原论文](https://arxiv.org/abs/2106.09685)：低秩增量的基础来源；是否存在非零更新以本地实际权重为准，不依据论文摘要的模型成绩或延迟结论预测动态 vLLM 服务
- [RepoGraph 原文](https://arxiv.org/html/2410.14684v2)：实际阅读构图与接入章节，区分过程式自动上下文和新增可选图动作；本地只借此检验有界同名调用行的自动反馈，不声称实现 tree-sitter 图、类型解析、k-hop 检索或复现论文成绩，既有图动作负结果不删除
- [Gemma 4 Agent Working Baseline](https://www.kaggle.com/code/leoprovorov/gemma-4-agent-working-baseline)：通过浏览器静态阅读当前可见正文和四文件打包单元，未下载、执行、复制或部署社区 Notebook。其 CPU 打包不代表 CPU 推理，页面 Best Score 不证明当前可见配置的成绩；作者的时间、调用、输出及命令超时建议只作待验证假设，不转为本地优化计数

##### 接口与源码反馈

[SWE-agent 原论文](https://arxiv.org/abs/2405.15793) 与[作者 ACI 说明](https://swe-agent.com/1.0/background/aci/)提供面向模型的编辑、反馈与错误恢复思路，不能把接口组件本身当性能证据

本项目的原文保护、坏源码可读性和新增全局名称反馈来自真实 Agent 失败轨迹，前两项未满足各自完整门禁，保留全部证据而不照搬其他基准数字。新的名称反馈只分析修改前后的源码，不注入隐藏测试或预期修复

##### 局部修复表示与未实现方向

[Agentless 原文](https://arxiv.org/html/2407.01489v2)将定位、局部修复与验证分开；本项目据此及多文件修改轨迹提出成组短片段编辑假设，不声称复现其候选采样、重排或基准成绩

固定总预算下的少量候选生成再选择仍未实现、排队或计数。若实施，选择只能用任务内公开测试与自生成有效探针，不能调用官方隐藏 verifier 给同次 Agent 选答案，也不能把增加采样算力和选择机制混为一谈

##### 公开 Notebook 建议的兼容核对

Working Baseline 的可见正文以单 Agent、四文件 ZIP、CPU 打包和关闭 Internet 为基本通路；它不是在 CPU 上执行基座推理。作者的八分钟、28 次调用、早编辑和较长命令超时建议属于其自述实验，不自动移植为本地收益，页面展示的最佳成绩也不能直接归给当前配置

当前安装版 verification.py 优先使用 verification_timeout_seconds，只有缺失时才退回命令超时；HarnessLimits 默认验证超时300秒，当前本地任务命令上限60秒，独立复核另显式设300秒。因此不能机械套用“提高命令上限才不会让 pytest 超时”的说法。当前未据该建议改配置或重新跑模型

当前 search_similar_code 的安装版说明允许符号路径、后缀以及未匹配时的词法回退，不是仅接受完整精确 ID；不将作者对图工具的概括当 API 规范。既有本地图工具负结果仍保留，它们不证明所有检索算法无效。这些是源码与提交通路知识补强，不新增优化计数

##### 官方 E4B 配置与本机实现

[Google 官方量化 E4B 配置](https://huggingface.co/google/gemma-4-E4B-it-qat-w4a16-ct/raw/main/config.json)使用 ConditionalGeneration 外层、嵌套文本配置和每层输入嵌入，不是仅把31B的型号字符串改短。该公开配置是研究参考，不能据此冒称与另一路 Kaggle 文件逐字一致，运行时以完整取得的官方文件及hash为准

[vLLM 对应版本文档](https://docs.vllm.ai/en/v0.19.1/models/supported_models/)与实际安装源码同时核对：本机 registry 登记了 Gemma4ForCausalLM 与 Gemma4ForConditionalGeneration，模型实现含 PLE 处理分支。注册存在仍不证明某组权重、量化、音视频组件或工具生成能够完整运行，需要后续原生配置资格检查与真实单卡测试，不升级或修改 SDK 来假造兼容

##### 源码坐标编辑的接口动机

[SWE-agent 原文](https://arxiv.org/html/2405.15793v3)的文件查看器显示行号，编辑器按起止行与替换文本执行，并用语法检查阻止错误传播。本地借此提出源码版本锁定的范围寻址假设，而不是复制其基准修复、复现文件权限、自动源码回显或历史过滤设置

本项目的实验两侧共同显示相同行号与源码版本，只比较原文OLD与版本号加行范围两种目标表达，原有4 /8行编辑限制和语法保护相同。版本校验是本地新增的防过期约束，不冒称论文原方法或已经有效；需真实作用、同质量成本和人工补丁审核，不把原文结论迁移为本项目的计数

##### KV缓存的原生精度控制

[vLLM对应版本的量化KV说明](https://docs.vllm.ai/en/v0.19.1/features/quantization/quantized_kvcache/)区分默认缩放、随机token启动校准和数据集校准，也区分默认模型精度与FP8。它提供接口和潜在资源方向，不保证当前Gemma量化权重或A6000的真实修复精度

本地只测试不校准的原生fp8_e4m3，不采用训练或数据集量化流程；固定相同缓存块数，仍要求实际完整上下文和真实任务质量。声明支持、理论存储字节和自造参数检查都不自动计收益

##### 原生服务的内部调度

[vLLM对应版本的Scheduler配置](https://docs.vllm.ai/en/v0.19.1/api/vllm/config/scheduler/)说明异步调度旨在减少GPU执行间隙；本机安装源码在兼容执行器下默认开启。该接口依据不证明当前31B编码任务有可测收益，仍须显式开关的完整真实对照，不把既有默认值、类选择或文档描述当作新增计数

##### 量化线性算子的原生选择入口

[vLLM环境变量](https://docs.vllm.ai/en/stable/configuration/env_vars/)公开VLLM_DISABLED_KERNELS以过滤混合精度线性实现；在线stable可能滚动更新，实际资格仍按本机0.19.1源码及官方权重头信息核实。只说明存在不改SDK的控制入口，不证明Exllama、FP16或某个内核更快，也不把接口发现计优化点

##### 整批时限重新核对 — 2026-10-19

[官方Evaluation](https://www.kaggle.com/competitions/gemma-4-developer-agent/overview)明确12小时覆盖全部任务的Agent执行与sandbox setup，排除patch验证；[官方Data](https://www.kaggle.com/competitions/gemma-4-developer-agent/data)给出约120个隐藏任务、public/private均分。Data内HARNESS_README的预算表明确eval_config.yaml支持四个字段，max_time_minutes在setup后启动，timeout_seconds只控制Phase 1单条命令，Phase 2验证另限300秒。没有找到允许参赛者通过ZIP扩大整批12小时的配置入口

[官方排错页](https://www.kaggle.com/code-competition-debugging)将Notebook Timeout定义为超过允许运行时限，并提醒隐藏输入规模和内容可能不同；它不是要求把打包Notebook改GPU的证据。本项目从Linux直接提交声明式ZIP，无须为本次预算修正重新建立Notebook

[工作人员对验证时间的答复](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/743663)估计全部题都有patch时验证约2小时，这是估计，不是运行额度或SLA，也不能用来反推我们的超时阶段

[同赛道时间/思考研究](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/747696)分列本地15/8分钟条件、超时数和公榜7.5分钟提交，证明本地长预算与实际提交不能混作同一条件；作者结果不是我们的受控对照，不将7.5或8分钟称为官方推荐或直接照搬其本地时钟补偿。当前5分钟是为整批可行性作的保守选择，未证明质量保持

##### 泛化与动作效率的本轮依据

[固定公开0.18 Notebook](https://www.kaggle.com/code/samvalladares/gemma-4-agent-budget-fit-single-agent?scriptVersionId=355976064)已静态读取可见正文与打包代码：单Agent、原生工具、提前编辑和定向测试，8分钟/28calls、8192输出/4096思考。它支持研究接口与预算配合，不是我们候选的对照结果，不直接复制预算或作者的隐藏题数推测；没有运行社区代码

[SWE-agent](https://arxiv.org/html/2405.15793v3)提供有界检索、局部源码窗口和编辑反馈的动作接口依据；[Agentless](https://arxiv.org/html/2407.01489)提供文件→符号→编辑位置→修复→验证的分层流程依据。本轮只借鉴这些机制，不复现论文的其他模型、多候选筛选、生成测试或引用其成绩作为本项目收益

两篇为成熟代码Agent研究起点，没有核实引用量排名。具体候选、原生工具资格与30/24题验收边界统一见[泛化与开源节流](generalization.md)，不向Agent提供参考补丁或官方验证答案
