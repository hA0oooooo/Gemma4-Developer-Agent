##### 2026-10-28 有界一手筛选：不生成近义候选

[SGAgent](https://arxiv.org/html/2602.23647v1)采用自建图工具、定位后建议、候选修复及多阶段筛选。当前接口与已有staged-repair／source-summary／graph-first／critic／proposal路线边界已核对；不能把三角色名称当新机制或把作者成绩当我方分数。[MemScope](https://arxiv.org/abs/2610.21170v1)仅完成摘要筛查，尚未审核全文／实现，其内存架构更新不是已验证Gemma配置。两者本次均未立候选／模型／提交。

公开源码和检索范围在output/research/public-candidate-screen/source-contract-screen-20261028/{review.json,retrieval-boundary.json}。主来源由web工具读到；四项Linux原始缓存请求超时，无字节hash／固定commit，不声称缓存成功，不继续盲试；控制SSH仍正常。未执行外部代码、读取Notebook输出／参考补丁或扩权。

##### VeriHarness：环境证据原则的迁移边界

[VeriHarness原文](https://arxiv.org/html/2610.00972v1)在工作区长任务中，以生成器相同模型检查多份产物的分歧与共同遗漏，再以环境证据裁决或修订。实验对象为通用工作区任务与前沿模型，不能据其数字推定Gemma五分钟代码修复收益。这里仅核查方法与适用范围，没有下载其轨迹池、外部代码或gold，也不把已失败的双草稿／独占复核改名重跑；选择之前须有完成的候选和真实证据链。阅读范围与去重记录见failure-semantics/post-isolated-triage.json。

##### 重复采样与小模型成本：仅作边界核查

[Large Language Monkeys固定v3](https://arxiv.org/html/2407.21787v3)将SWE-bench的一次尝试看作完整多轮轨迹，并分别讨论候选覆盖率、识别正确候选的精度及任务相关的计算成本。论文的多次采样结果不是五分钟内两个零温角色的收益证据；不能把pass@k或更小模型的名义成本直接当作最终选中补丁的正确率。此次未执行作者代码、下载关联数据／gold或训练，不据此新开模型实验。

本地去重还确认自适应思考已有decoding／control_flow记录，原native-e4b不完整封签及12B完整负结果不能改名复跑。当前isolated-proposals仍按原规则等待完整模型结果，原始来源核查在output/research/isolated-proposals/inference-scaling-source-check.json；不是新可提交方案或官方得分。

##### 文献与实现机制

##### AutoFL覆盖引导定位：可迁移条件，不是修复率证据

新核对[AutoFL固定v3方法3.1—3.3](https://arxiv.org/html/2308.05487v3)：使用给定失败测试的覆盖信息收窄候选函数，再通过工具读取实现并解释／定位；其定位成绩不是任务修复率。当前比赛Agent不自动得到验证test_patch，不能拿隐藏失败测试补齐论文输入条件，本方向只追踪Agent自己选定的既有测试，不原样复现AutoFL或借其成绩预测公榜

[Python3.12 profiling接口](https://docs.python.org/3.12/library/sys.html#sys.setprofile)与[线程接口](https://docs.python.org/3.12/library/threading.html#threading.setprofile_all_threads)支持新探针的调用事件实现；执行证据不等于故障因果，Python线程支持不等于子进程／C调用或完整分支覆盖。新自有实现与8组CPU资格见context_and_tools.md，未复制论文代码、训练模型或启动GPU比较，不计新正向因素

本轮公开检索另发现[elamurg/gemma-4-dev](https://github.com/elamurg/gemma-4-dev)，读取时仓库仅README和plan，结果表明确为placeholder，不能把文中规划的检索／双Agent／验证组件当已发布实现或高分实证。未安装或执行该项目；未确认新的可直接采用高分包，不从搜索标题推断真实评分

这里只保存已核对来源、可迁移机制与实验边界，不把论文成绩、代码可运行或检索成功计作本项目正向提分；现有SWE-agent、Agentless与CodeAct实验解释见[泛化研究](generalization.md)

##### LocAgent：从实体定位到依赖关系

来源为[ACL论文](https://aclanthology.org/2025.acl-long.426/)、[方法原文](https://arxiv.org/html/2503.09089v1#S3)与[作者仓库固定提交](https://github.com/gersteinlab/LocAgent/tree/4935b557326c154bad8e8dcf3747cc8d32d1f387)，读取时用git远程HEAD确认该提交，不将之后的master变化视为同一实现

方法把Python代码组织为目录、文件、类、函数及其包含、导入、调用、继承关系，先从关键词找到实体，再沿相关边扩展并取回必要源码，避免只按目录来回寻找。输出有折叠、预览与完整代码等粒度；这提供定位和控制上下文的机制依据，不保证Gemma上的修复率收益

论文还包含模型微调、重复定位及排序汇总，外部结果不能归因为一个图工具，也不是本项目单次修复成绩；本轮不下载训练数据、不训练或采用其他基座，不照搬多次采样预算

##### 固定提交的代码入口

下列路径均在上述固定提交中核对，只阅读公开代码，未运行该项目或建立额外参考仓库

```text
auto_search_main.py
dependency_graph/
  batch_build_graph.py
  __init__.py
plugins/location_tools/
  __init__.py
  locationtools.py
  repo_ops/
    __init__.py
    repo_ops.py
```

定位入口为auto_search_main.py的run_localize → set_current_issue → auto_search_process → 响应动作解析与工具执行；set_current_issue加载或调用build_graph建立索引并构造RepoEntitySearcher/RepoDependencySearcher。batch_build_graph.py提供提前建图入口，auto_search_main.py的merge调用merge_sample_locations汇总定位结果

LocationToolsRequirement读取locationtools.DOCUMENTATION；locationtools.py从repo_ops.__all__导入函数并由函数签名/文档构造说明。已核对这些包装、状态初始化与查询/遍历实现的连接，未审计全部解析器或复现训练/下游修复实验

| 论文概念 | 固定代码当前导出 | 本比赛可考虑的入口 |
| --- | --- | --- |
| 实体查找 | search_code_snippets，内部有search_entity等分层查找 | search_similar_code与有界文本搜索，但算法不等价 |
| 依赖遍历 | explore_graph_structure、explore_tree_structure | get_code_neighbors；get_code_subgraph只是给定节点的诱导子图，不是任意深度BFS |
| 源码取回 | 不能把论文的RetrieveEntity名称直接当成当前导出API；get_entity_contents在该__all__中被注释 | 按查到的路径使用read_file核对当前工作树 |

工具和初始化实现见[repo_ops.py](https://github.com/gersteinlab/LocAgent/blob/4935b557326c154bad8e8dcf3747cc8d32d1f387/plugins/location_tools/repo_ops/repo_ops.py)，工具说明生成见[locationtools.py](https://github.com/gersteinlab/LocAgent/blob/4935b557326c154bad8e8dcf3747cc8d32d1f387/plugins/location_tools/locationtools.py)，主循环见[auto_search_main.py](https://github.com/gersteinlab/LocAgent/blob/4935b557326c154bad8e8dcf3747cc8d32d1f387/auto_search_main.py)

##### 对本项目的可迁移假设

现有开发轨迹仍有重复阅读、较晚开始编辑及共享接口调用点遗漏，可考虑只利用官方预置代码图缩小待查范围，再检查当前源码，而不是另建索引或复制LocAgent运行框架。是否增加图工具及定位提示应作为明确的架构包比较，不能把联合变化归因于图本身

比赛官方入口和参数以本地official_guide.md第6.3节及实际SDK为准：get_code_neighbors(node, edge_type, max_neighbors)返回双向邻居；get_code_subgraph(nodes)只返回给定节点间的边。search_similar_code离线时按已有符号/节点查询并有词法后备，不是实时自然语言向量服务。它们都消耗原生工具额度，输出有截断

图只是静态线索，查不到不证明没有调用点，邻居不等于完整调用者清单；必须用有界文本查找及当前源码核实，再编译和做定向既有测试。若数据不可用或符号与当前快照不符，不能凭图改代码或无限重试

该方向尚未建立模型候选、运行或证明收益，预留24题未用于设计；当前已选策略及首次独立比较保持冻结，不在途中加入图工具

##### Agentless：有界定位与独立复现

[论文](https://arxiv.org/html/2407.01489v2)将流程分为定位、修复和验证；主要可借鉴点是先缩到文件、再缩到符号与局部源码，以及先确认复现脚本能在原源码触发预期缺陷，再用它检查补丁。生成脚本声称“已修复”本身不是正确性证据

[官方仓库](https://github.com/OpenAutoCoder/Agentless/tree/5ce5888b9f149beaace393957a55ea8ee46c9f71)固定源码为5ce5888b9f149beaace393957a55ea8ee46c9f71，已静态核对以下入口，未克隆、执行其模型或测试流程

```text
agentless/
  fl/localize.py
  fl/FL.py
  util/compress_file.py
  repair/repair.py
  repair/rerank.py
```

| 已核对实现 | 职责及边界 |
| --- | --- |
| localize.py的localize_instance → FL.py的LLMFL.localize → localize_function_from_compressed_files → localize_line_from_coarse_function_locs | 文件、符号、局部编辑范围逐层收缩；不同CLI开关可走不同分支，不是所有运行都执行完整三层 |
| compress_file.py的get_skeleton、CompressTransformer | 用LibCST压缩函数体，不能把骨架当作实际实现或完整调用图 |
| repair.py的repair → process_loc → construct_topn_file_context | 根据定位片段构建修复上下文；post_process_repair另调用post_process_raw_output做语法与空白差异检查 |
| rerank.py的majority_voting | 先使用回归/复现结果筛选，再按归一化补丁频次选取；复现筛选可回退，不是完整正确性证明 |

定位代码见[localize.py](https://github.com/OpenAutoCoder/Agentless/blob/5ce5888b9f149beaace393957a55ea8ee46c9f71/agentless/fl/localize.py)，骨架与局部范围见[FL.py](https://github.com/OpenAutoCoder/Agentless/blob/5ce5888b9f149beaace393957a55ea8ee46c9f71/agentless/fl/FL.py)，修复与候选选择见[repair.py](https://github.com/OpenAutoCoder/Agentless/blob/5ce5888b9f149beaace393957a55ea8ee46c9f71/agentless/repair/repair.py)和[rerank.py](https://github.com/OpenAutoCoder/Agentless/blob/5ce5888b9f149beaace393957a55ea8ee46c9f71/agentless/repair/rerank.py)

后续假设是给原生单Agent增加一次有界的文件→符号→局部源码定位约束，并在预算允许时优先使用原源码确实失败的断言式复现，检查修改前后同一行为。它是待开发集完整比较的机制，不是新增正向点，也不根据正在执行的独立题结果改当前提示

不直接照搬完整框架：论文使用每题多份补丁和复现候选，其成本不能套入本比赛整批12小时；代码128k上下文限制也不能套入当前32k服务。它的编辑函数签名不是比赛SDK的edit_file签名，不能再引入错误工具参数；自定义后处理、外部模型API和判分时选择补丁也不属于当前已验证的提交接口

开发时可选少量既有回归帮助诊断，但最终必须执行官方固定测试，不让模型删除或豁免评分测试，不读取gold或隐藏答案。外部论文通过率、费用与本项目成绩分开，不声称本地Gemma已获得论文收益

##### 公开获评分基线：区分实际源码与最佳成绩标签

2026-10-21通过只读网页核对[Bounded Rescue获评分源码](https://www.kaggle.com/code/lynnsakurai/gemma-4-budget-fit-agent-w-bounded-rescue?scriptVersionId=358320692)：该页自身Public Score为0.18，输出ZIP声明SHA256为a4b10f6b8034fd7fffa144a7ee3fbd8faf9a84503ffb1349d1522ba048b534d3。[默认页面](https://www.kaggle.com/code/lynnsakurai/gemma-4-budget-fit-agent-w-bounded-rescue)自身为0.15，最佳标签仍0.18，不能把当前正文和历史最佳成绩拼接为同一实验

获评分配置为31B、temperature 0.2、8192输出/4096思考、28动作/80轮/8分钟、单次工具240秒。机制是有界文本定位优先，失败后仅一次图检索及至多一次邻居查询；编辑匹配失败先缩短精确锚点，之后才做带唯一性断言的命令恢复；限制验证次数并尽早提交。只作机制参考，没有下载或执行社区Notebook，也不因页面标有Apache-2.0就把其断言当作本地事实

两份公开源码的差异与一次公榜成绩不能证明某条提示导致增减；8分钟也是硬上限而非每题实际平均成本。此前public-budget的完整比较和负面证据保留，不为新公开标题重跑相同实验，更不照搬“忽略所有导入/fixture错误”的判断。当前温度比较保持冻结，后续若引入有界检索或较多思考，须单独登记变化、完整开发比较及真实预算

##### 官方小模型支持：预算研究线索，不是既成收益

2026-10-21复核[官方工作人员公告](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/748287)，允许同一提交选择31B、12B、E4B或E2B量化基座，但所有角色必须使用同一变体，不能混搭大小模型。工作人员将更快推理及更多迭代列为探索方向，不是本项目已测得的收益；允许同题并行模型调用也不等于工具并行或多任务并行

该帖还出现12B权重键加载错误，工作人员称最新wheelhouse已修复，但回复没有绑定具体本地包版本；关于各变体完全相同评分硬件的提问不能当已获官方确认。Linux已有三个规格的config.json不等于本轮已经启动、验证权重完整或测得速度。若以后比较小模型，先核验本地启动兼容，再保持提示、工具与预算可比，完整报告能力与总成本，不能拿旧复杂Skill小样本的失败直接排除新的原生工具策略

随后本地12B完成真实服务启动和三个合成参数请求，仍不是修复质量证明；同一六工具策略的12B/31B旧30题完整比较已启动，状态和冻结规则见generalization.md，不将正在运行的局部结果写成模型选择结论

##### SWE-agent：论文机制与固定源码不能混为一谈

[NeurIPS论文](https://arxiv.org/html/2405.15793v3)强调专为模型设计动作、简洁反馈及错误恢复，而不只是增加提示。其设置、模型和预算不同，不能直接移植成绩；本文只提取待验证机制

2026-10-21只读查看官方仓库历史标签v0.2.0，固定commit为[58aa046a9b5d4032cfc28c2509095b23ad408c72](https://github.com/SWE-agent/SWE-agent/tree/58aa046a9b5d4032cfc28c2509095b23ad408c72)。这是有界历史实现核对，不声称等同论文所有最终实验配置；只取源码对象，未读取演示轨迹、测试解答或执行该项目

```text
run.py
config/default.yaml
config/commands/edit_linting.sh
config/commands/search.sh
sweagent/agent/agents.py
sweagent/agent/history_processors.py
```

调用链为run.py的main → Agent.run → forward/forward_model → model.query(local_history) → 命令解析 → env.step；命令文件由init_environment_vars装入环境。local_history调用所选history_processor，所以“代码包含某处理器”不等于当前配置实际启用了它

| 固定实现 | 已核对行为 | 移植边界 |
| --- | --- | --- |
| edit_linting.sh的edit | 备份、写入、限定flake8检查；成功展示新内容，失败恢复原文件并展示差异上下文 | 是先写再回滚，不是写前原子保证；该实现未先扣除原有lint错误，不能照搬为增量检查 |
| search.sh的search_dir | 按文件汇总匹配数量，超过100个匹配文件时要求收窄 | 论文与这份历史实现的阈值不能混用；搜索范围和计数单位须另测 |
| search_file | grep -nH后用第一列计算所谓num_lines | 同一个文件的第一列是文件名，不能把这个判断当作可靠的100行上限 |
| history_processors.py与default.yaml | Last5Observations保留最初任务、演示和最近观察，旧输出变简述；但该default实际选DefaultHistoryProcessor，即原样返回 | 不能把论文的历史压缩效果归给默认配置，也不在本比赛主机侧私改历史处理 |

编辑实现见[edit_linting.sh](https://github.com/SWE-agent/SWE-agent/blob/58aa046a9b5d4032cfc28c2509095b23ad408c72/config/commands/edit_linting.sh)，搜索见[search.sh](https://github.com/SWE-agent/SWE-agent/blob/58aa046a9b5d4032cfc28c2509095b23ad408c72/config/commands/search.sh)，历史处理见[history_processors.py](https://github.com/SWE-agent/SWE-agent/blob/58aa046a9b5d4032cfc28c2509095b23ad408c72/sweagent/agent/history_processors.py)，实际配置见[default.yaml](https://github.com/SWE-agent/SWE-agent/blob/58aa046a9b5d4032cfc28c2509095b23ad408c72/config/default.yaml)

可继续检验的是“编辑后一次获取小窗口、编译结果和局部diff”的反馈合并，以及按文件汇总搜索后主动收窄；不是照搬不同工具签名、默认历史器或循环重试。此前命令编辑/写入保护已有负结果，不能为新论文标题重复计数；若设计提交内可控制的实现，须另作完整开发比较，当前模型比较的工具、提示、SDK与预算不改

##### 推理预算：提示约束与解码约束要分开

[TALE固定原文方法段](https://arxiv.org/html/2412.18547v1#S5)先估计预算，再将预算写入提示；其离线最优预算搜索使用正确答案标签。不能把这种软提示预算等同于SDK硬思考上限，也不能照搬带答案的逐题搜索来选择本比赛隐藏题策略

[s1固定原文方法段](https://arxiv.org/html/2501.19393v1#S3)在SFT后的Qwen上用解码干预结束或延长思考；反复延长也可能循环。它不是不训练即可复现的Gemma coding-agent成绩，不能据此断言减少思考必然更快或质量不变

对本项目只保留研究纪律：实际生成量、完整修复质量和含失败成本共同报告，不把配置上限当消费量或把较短失败当节省。当前[2048思考比较](thinking_balance.md)的参数、旧30题与接受条件早于本次阅读已冻结；未增加预算预测器、提示、训练或反复逐题搜索，未改正在运行的候选

此次只核对原文方法及相关设置，不声称复现论文或已核作者GitHub执行器，也不宣称引用排名；这些是机制与边界说明，不计新增正向点

##### CodeMonkeys：执行反馈与候选选择，不能只看覆盖率

已读[固定论文方法与限制段](https://arxiv.org/html/2501.14723v1#S2)，并用git远程HEAD将[作者代码](https://github.com/ScalingIntelligence/codemonkeys/tree/7c35e1a79f4ebe40f94e5d0052f4daa7681412a5)锁定为7c35e1a79f4ebe40f94e5d0052f4daa7681412a5。GitHub树API因公共限额返回403，未继续尝试认证，改读同一提交的公开raw源文件；不克隆仓库、不取演示轨迹／参考答案、不运行安装或gold评测示例

论文把上下文、候选生成、最终选择分开：先形成复现脚本，再比较同一脚本在原始代码和补丁上的结果；多个候选会增加至少一份正确的机会，但必须另外解决选中正确补丁的问题。模型生成的测试只是有缺陷的验证器，不等于完整正确性。论文使用不同模型、较长上下文和多次采样，其成绩不是Gemma比赛或五分钟同预算证据，不能直接搬十条轨迹或128k上下文

```text
codemonkeys/
  run_codemonkeys.py
  stages/
    testing_state_machine.py
    editing_state_machine.py
    selection_state_machine.py
  utils/
    majority_voting.py
    abstract_state_machine.py
```

入口[run_codemonkeys.py](https://github.com/ScalingIntelligence/codemonkeys/blob/7c35e1a79f4ebe40f94e5d0052f4daa7681412a5/codemonkeys/run_codemonkeys.py)依次连接relevance、ranking、testing、editing、generated_test_execution、selection与导出。只核对这些调用关系及下表核心函数，没有执行完整生成／投票链

| 固定实现 | 已读行为 | 不能据此声称 |
| --- | --- | --- |
| [TestingStateMachine.exec_script／handle_approve_or_revise_response](https://github.com/ScalingIntelligence/codemonkeys/blob/7c35e1a79f4ebe40f94e5d0052f4daa7681412a5/codemonkeys/stages/testing_state_machine.py) | 在原始代码执行脚本，把结果给模型，模型返回test或done决定继续 | done分支没有独立硬检查原始退出码，不能把模型批准直接等同于已复现真实缺陷 |
| [EditingStateMachine.exec_script／approve_or_revise](https://github.com/ScalingIntelligence/codemonkeys/blob/7c35e1a79f4ebe40f94e5d0052f4daa7681412a5/codemonkeys/stages/editing_state_machine.py) | 对相同脚本分别运行原始与当前补丁，并把两侧输出、退出码及diff反馈；可修正脚本或补丁 | 原始失败可能是导入、配置或脚本自身错误，必须核实针对的是任务缺陷 |
| [get_patches_for_selection](https://github.com/ScalingIntelligence/codemonkeys/blob/7c35e1a79f4ebe40f94e5d0052f4daa7681412a5/codemonkeys/utils/majority_voting.py)与[SelectionStateMachine](https://github.com/ScalingIntelligence/codemonkeys/blob/7c35e1a79f4ebe40f94e5d0052f4daa7681412a5/codemonkeys/stages/selection_state_machine.py) | 按生成测试的退出0票数、补丁长度排序去重取前3，再生成区分测试，比较原始与多个候选后选择 | 任一候选通过、投票胜出或短diff不是提交修复正确性的证明 |
| [StateMachine.generate](https://github.com/ScalingIntelligence/codemonkeys/blob/7c35e1a79f4ebe40f94e5d0052f4daa7681412a5/codemonkeys/utils/abstract_state_machine.py) | 每次生成均增加attempt_counter，格式纠错也消耗上限；超上下文和超次数是终态 | 不能忽略格式恢复或验证／选择成本来宣传搜索收益 |

对本项目只登记待检验的推断：先在六原生工具骨架内研究一次有界的“原始确实触发任务缺陷→同一断言在修改后通过”，再考虑候选选择；暂不增加并行Agent或采样。当前源代码常见的额外repro脚本会捕获异常再打印成功，不能作为这种链的证据；应记录实际断言、失败类型及两侧退出码，不能把“原始任意失败”当校准通过

该假设与既有Agentless复现／验证同属执行反馈家族，不按新论文名重复计点。若未来实施，仍须通过官方允许的提交内工具完成，不改SDK历史、原测试或计分器，不调用其他基座／商业API、不使用私有评分标签选择补丁，完整计算同一会话时间与调用；需要重新冻结公平对照，而不是在当前模型批次中途加入。当前仅来源与机制核对，无新模型、GPU、训练或正式提交

##### 自写测试与工具菜单：文摘初筛，不是复现结果

[Rethinking the Value of Agent-Generated Tests，固定v2](https://arxiv.org/abs/2602.07900v2)在SWE-bench Verified上分析六个模型，并对四个模型做自写测试提示干预，未包含Gemma。[方法与RQ3](https://arxiv.org/html/2602.07900v2#S5)采用mini-SWE-agent，测试抽取按test_／_test.py／tests.py命名，不能完整覆盖本项目大量repro.py；提示干预不是强制执行器、工具菜单或隐藏验证器修改，尚未完整审核作者代码

补读§5表7—8：抑制条件删除默认测试提示并要求不新建测试或脚本，不是禁止运行既有测试。Kimi K2-T修复317→304、平均API调用减少35.4%；DeepSeek v3.2-R修复300→291、调用减少24.5%。修复差异的exact McNemar p分别0.228／0.435，未检出显著差异不等于证明质量等价，不能只报成本收益

后续去重已直接读到精确0.17的prompts/system.md：原EDIT段已有“Do not create scratch scripts or new tests; use short inline Python checks instead”，事后检查候选也保留同一条；因此论文抑制自写测试不能当本项目全新机制再跑。另有早期工具箱联合限制的混合负结果，不能因关键词初筛未命中就称首次探索。保留合法新实现文件和既有测试的边界，不把命名规则当完整语义，也不把API调用下降换算为原生／wall成本达标

execution-paths全60项后置命名下界盘点：候选15/30、对照20/30曾尝试写原快照不存在的repro／debug／check／test类文件，最终保留分别10/30和11/30；候选脚本更少却支持修复6/30对7/30、超时19对13，不能据相关性认定限制脚本必有收益。该只读盘点含9项分类检查、原始快照与全组trace身份，证据failure-analysis.json SHA256=601fc41836b53437425c0fba93709b25d34168a2f91c4c91561707244bc6fd6e，不是全部脚本识别、完整语义失败审核或新机制增益。本轮不创建近义提示候选、不启动新GPU或正式提交

[Beyond the Model／NanoHarness，固定v1](https://arxiv.org/html/2609.32459v1)已补读§3.1、4.4、5.2：组件消融在200道ProgramBench仓库生成题，使用非思考的Qwen／DeepSeek；工具注册及专门子Agent有效，压缩／通用子Agent可能有害，组合收益不能简单相加。该组300步、6小时会话、350K压缩预算，与本赛31B／5分钟／24原生动作／32K不同，不能照搬其收益或开更大隐藏预算；本次没有核验作者实现代码或复现其分数

[Is Bash All You Need，固定v1](https://arxiv.org/abs/2609.11999v1)讨论企业数字工作流中的五种接口，摘要报告在其两个模型／两个企业基准上bash-only优于类型工具；不是本比赛修复实验。[mini-SWE-agent官方设计说明](https://github.com/SWE-agent/mini-swe-agent/blob/main/docs/index.md)也强调单shell、线性历史与独立子进程，但该链接是移动分支，此处不称固定代码复现，不引用其排行榜数字预测Gemma

对项目的有限启发是把“验证反馈是否真实”和“接口是否诱发无效动作”分开研究，而非继续堆提示或机械取消测试。已有command-localization曾同时删edit_file与write_file，不等于仅删write_file、保留原生精确编辑的实验；如后续做单一工具菜单消融，应说明这项区别、保留创建新实现文件的合法途径，并从精确0.17重新冻结公平对照，不能把旧失败当成功或中途改变当前calibrated-repro

第一篇已补读方法／干预段，NanoHarness现补读了组件、预算与消融方法，第三篇仍仅文摘筛查；未宣称高引用量、完整论文复现、稳定收益或新增正向点，没有因论文结论另启动模型／GPU／正式提交

##### 工具命名敏感性：训练证据与推理假设分开

[Hammer，固定v1的§3—4](https://arxiv.org/html/2410.04587v1)研究函数及参数命名依赖：测试时替换名称可使未经对应训练的模型退化；作者在训练时随机替换名称，结合无匹配工具的负例来提高鲁棒性。它不是只在推理时改名的Harness实验，也不是Gemma或本比赛修复成绩

当前脚本研究中，解析后的请求曾把Agent名填入skill_name，这是标识值混淆，与论文扰动schema名称并非同一干预。只能登记命名敏感性的风险，不能据论文认定名称对齐或随机掩码必提分，更不能从trace唯一断定生成端／parser责任。当前候选不变；若以后比较名称，须另行前瞻冻结，不把修复调用格式计作修复质量，也不重复早期同类计点。没有下载其训练集、权重或启动训练

##### 上下文管理：旧观察遮蔽、新输出筛选与源码保真

[The Complexity Trap，固定v1的§3.1—3.2及表1](https://arxiv.org/html/2508.21433v1#S3)比较SWE-agent的历史观察遮蔽与模型摘要：前者仅替换窗口外工具观察，保留推理／动作，不是统一缩短新输出。Qwen3-32B非思考组修复率反而下降，说明降成本不保证提分；其上下文／模型配置不同于本项目。此处不用后续v3新增实验替代v1证据

[SWE-Pruner，固定v1的§3](https://arxiv.org/html/2601.16746v1#S3)把目标问题附到新工具输出，经训练的Qwen3-Reranker-0.6B进行按行筛选，未给目标时可绕过。它不是纯提示词剪裁，也不等于修改旧历史；额外训练／模型部署不在当前Harness研究权限内，本轮没有下载其模型或训练数据

[Skip the Compressor／CQ2-CARE，固定v1的§2—3](https://arxiv.org/html/2610.21073v1#S2)使用同一模型多次定位，再提供原文整文件与少量相关片段，在300道SWE-rebench题比较预算匹配的上下文。其80K上限／额外定位调用不适用于我方32K／五分钟预算，且并非所有训练方法比较都显著；不能直接搬其成绩或将截断后的任意文件称为整文件方案

第三篇的gold资格过滤属于作者评测设计，不是给推理Agent喂gold；本项目不搬用该步骤、oracle上下文或示例答案。这里只核对固定论文的方法、实验设置与相关结果，未执行作者实现／下载评测数据，未核实引用量，不称完整复现或高引用背书

本项目的推断应分三层：改写旧历史需要宿主能力，不能用已禁止的events_compaction或未注册callback假装可提交；额外神经筛选器需要新的训练／部署条件，不能冒充现有单基座方案；若研究提交内的工具输出整理，则必须保留源码字节和完整可回读产物，并把退出码、超时、真实失败与压缩展示区分开

较小的待核查方向是先压缩重复执行日志，而非删除精确编辑所需的源码字符；但这不是上述任一论文的原样复现，也尚未证明能通过正式Skill路径保持执行／计数／超时语义。先完成当前90项及完整失败分析，再决定是否另立候选；不在运行中换工具、不启动新GPU、训练或正式提交，不把文献启发计作正向结果

##### 完整源码块与较小观察：新原型的来源和区别

当前90项及失败审核已完成，真实轨迹显示源码读取占观察字符71%—78%，相同路径／行号／文本的复读仅占源码正文约12%—16%。这些不是token或因果成本，不支持先采用重复日志压缩器；详细定义与hash见tool-output-budget/trace-profile.json和source-reuse.json

[SWE-agent作者文档](https://swe-agent.com/0.7/background/aci/)强调有限窗口与简洁搜索反馈，其100行选择是特定实验结果，不是所有函数都应裁成100行的规则。[Agentless固定v1 §2.1](https://arxiv.org/html/2407.01489v1#S2.SS1)先用声明骨架定位，再取所选位置的完整源码；这不等于只给骨架就足以修复，本文没有复现其多候选流程或把其成绩转移到本项目

[SWE-Edit固定v1 §3.1及附录A.2](https://arxiv.org/html/2604.26102v1#S3.SS1)用Viewer子代理选择相关完整代码块、Editor执行高层修改，两者工作在专门上下文；论文另有训练编辑策略的部分，不能把整套收益归给一个源码窗口。此处只核对方法，不下载模型／数据或运行作者实现，不采用其异构模型、训练与额外预算

本项目symbol-context是另一个待检验推断：用确定性AST和现有Skill返回指定符号的完整原文，不增模型子代理、不改写旧历史。旧source-pane会按85行及字符限制裁断所选符号，新原型遇超限明确不给半截源码，允许显式行段及现有命令回读。它是读取路由、菜单与说明的联合干预，不称纯块大小因果实验或上述论文复现；完整语法块也不等于包含全部依赖，imports／globals／长函数仍需主动查看，成本和退化必须完整比较

##### Gemma4原生工具解析：组件事实与策略收益分开

只读核对[上游vLLM v0.19.1解析器](https://github.com/vllm-project/vllm/blob/v0.19.1/vllm/tool_parsers/gemma4_tool_parser.py)，与当前安装文件SHA256逐字相同。自有四份CPU合成输入证实：正确Gemma分隔符数组可往返，普通双引号简单数组会保留引号，含列表代码的普通引号数组及意外右方括号可触发数组游标不推进；观察器与单独无观察器截止均确认。证据在differential-probe/analysis/parser-qualification.json，详情见execution_feedback.md；没有加载模型或改SDK，未证实它就是当前分片中断根因

另发现同比赛的评测工具项目[gemma4-swe-kit固定提交](https://github.com/damsolanke/gemma4-swe-kit/tree/a9270ed02964c0b42ef420fa1afec9bb03da7362)，作者也报告同一数组解析死循环；已静态阅读[该提交的fuzz入口](https://github.com/damsolanke/gemma4-swe-kit/blob/a9270ed02964c0b42ef420fa1afec9bb03da7362/tools/fuzz_vllm_parser.py)，其调用原版纯函数并以子进程截止验证。没有执行其完整随机语料、安装代理、训练功能或采用其成绩／官方等价性主张；本项目的四例复现与作者更大数量主张分开，不把独立报告当本次现场响应

下一项可核查假设是降低数组参数里的复杂代码负载，而不是仅增加“不要格式错误”提示；例如把复杂文本留在原生标量文件编辑接口、脚本参数只传短路径。但额外文件与动作可能抵消收益，不能因一个组件缺陷就采用新Harness或重新命名旧失败路线。任何研究须先结束当前批次、冻结不同接口与精确对照、验证真实Gemma解析／工具路径、完整计入预算并统一审核质量；官方后端不可由提交控制，本地修解析器不等于可迁移的公榜收益

##### 同比赛公开实测记录：成绩与验证边界

新读作者[10月24日更新的实测总结](https://pilkwangkim.github.io/posts/Gemma-4-Developer-Agent-Part-2-Measuring-an-Agent-While-Its-Evaluator-Moved/)。作者报告同字节包曾得0.10与0.15，且未从公开0.18基线获得更高有效成绩；属于其项目记录，不是我方重复实验或通用噪声估计。启发是分清实际行为断言、原生验证、整次超时和最终成绩，不从打印／编译成功推断修复

文中提及相同版本号的评测依赖可能重建；本地当前标签为swegemma0.2.11、adk-submission0.2.13、vLLM0.19.1，标签相同不证明公开产物或隐藏评分端字节相同。本轮未更新依赖、下载新模型或重跑旧包；既有冻结源码hash、原始JUnit与运行回执保持，新的来源核查不计正向点

##### Aider仓库地图：结构索引与自动注入的迁移边界

核对[Aider官方说明](https://aider.chat/docs/repomap.html)、[作者方法说明](https://aider.chat/2023/10/22/repomap.html)及读取时固定的[源码提交](https://github.com/Aider-AI/aider/tree/5dc9490bb35f9729ef2c95d00a19ccd30c26339c)。仅阅读公开材料，未克隆、安装、运行Aider或复制其代码，不把产品说明当竞赛评分证据

方法用定义／引用关系选取简明符号上下文，并按预算筛选；不是发送全库，也不是完整运行时调用图。当前代码以文件关系图做个性化PageRank，再渲染重要定义；默认地图约1k token，但上下文扩张、近似计数与容差意味着它不是严格固定上限。渲染还会截短长行，地图只能用于定位，不能直接当精确编辑原文

```text
aider/
  repomap.py
  coders/base_coder.py
```

固定[调用侧](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/base_coder.py)的Coder.get_repo_messages→get_repo_map取聊天提及与文件集合；固定[索引侧](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/repomap.py)经get_ranked_tags_map／其uncached实现，调用get_ranked_tags、get_tags／get_tags_raw建立定义引用关系，随后排序并由to_tree渲染。已核对这些入口和预算选择连接，未全面审计多语言查询、缓存和编辑器

对本项目的关键差别是Aider宿主主动把地图放进请求，而不是只给模型一个可选图工具。当前官方声明式提交没有已验证的任意宿主预处理回调，若改用Skill或额外阶段，调用、输出、生成开销和未调用风险必须重新计入；不能声称已经原样移植。旧graph-localization四题未调用图工具、旧BM25排序只有有限小样本信号、symbol-context完整筛选未采用，这些结果保持，不换名称当新正向点

后续若当前实验完整结案后选择该方向，应先确认与旧检索路线的实质差异、源码／索引保真和正式接口可提交性，再冻结等预算比较与真实定位作用证据。只检验通用代码关系与公开任务关键词，不按任务ID或答案指定目标文件；排名不是正确修复证明。本轮只有来源核查，没有新候选、模型作业或正式请求

##### 新公开论文：交叉执行与轨迹选择的预算边界

[TEX](https://arxiv.org/html/2610.27290v1)使用多代理测试／补丁交叉执行矩阵，论文为Sonnet4、4代理3轮；86.4%是测试生成成绩，修复实验57.8%到59.8%。完整配置约12倍单代理开销，不能直接套我方五分钟24动作。仅保留紧凑执行反馈动机，先解决独立副本与完整成本，不读实例修复附录／gold。

[Scaling Test-Time Compute for Agentic Coding](https://arxiv.org/html/2604.16529v1)用结构化轨迹摘要作小组选择并在新环境重试，需要额外rollout／总结／投票。更强模型的收益不是Gemma同预算证明，也不改变handoff-memory没有实际后段采用链的负结果。方法／预算阅读范围见public-candidate-screen/paper-review.json，未执行外部代码或模型。


##### 新公开来源筛查：持久运行时与指令遵循

2026-10-27在feedback-budget完整结案后，只读核对[Prime Agent固定v1论文](https://arxiv.org/html/2608.23552v1)§2.2—2.6／3.2／5及[作者运行时shim](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/prime-agent-runtime/src/rlm/__init__.py)、[持久REPL](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/prime-agent-runtime/src/rlm/repl.py)。论文的持续Python命名空间与递归会话依赖宿主桥接、状态和完整计费，并非多注册一个工具或每次独立shell。当前提交Schema仅有Llm／Sequential／Parallel／Loop四类，未提供参与者code_executor字段；组织者code_executor参数用于沙箱Skill，不能据其存在声称能替换宿主REPL或注册任意callback。直接移植不成立；Skill内自建沙箱状态服务并非已证不可能，但属另外的适配，须先证明生命周期、共享预算、真实模型采用与修复收益，不能把既有native-shell／handoff-memory／isolated-proposals的负结果换名重跑。本轮未安装作者代码、建daemon、训练或启动模型。

[Harness-IF固定v1](https://arxiv.org/pdf/2608.11727)§3.1／3.4／4.4—4.5／5区分默认行为与受干预规则的实际遵循。其主面板的提示面分层不是配对放置因果比较；冲突pilot并非通用层级，较多判据依赖LLM judge，文中明确限制相邻排名解释，也无Gemma修复收益。本项目只吸收作用证据边界，不据此移动同义预算提示再做扫描。论文／代码URL、实时main分支源码hash及本机Schema身份保存在persistent-runtime-and-if-screen.json（SHA256=ba430adab201936267cd8a70fbf49ebaefe7dd571f796b15d20045d0ffc9974f）；源码观察未固定commit，不能称固定版本实现复现；模型／verifier／正式请求均0。


##### 需求oracle与恢复文献：当前不立候选

三份最新精确对照失败的源码／轨迹焦点已完成，详见context_and_tools.md及failure-semantics/post-feedback-three-focus.json。随后核查[CodeMetaAgent固定v1](https://arxiv.org/html/2511.18249v1)§3—5及7的方法／预算，未读修复案例：修复侧实为否定／翻译／分步骤／释义的描述变换，BERT相似度阈值过滤，不是可执行语义等价证明；测试变换侧还用oracle实现筛选。论文开销也高于直接生成，没有我方五分钟Gemma的等预算证据。因此不把描述释义、旧前置规划或现有原始／当前副本差分检查换名重测，不下载新reviewer模型或引入oracle答案。真正无gold的关系检查器仍需另立设计，未在此普遍否定。

[RippleCP固定v1](https://arxiv.org/html/2610.09088v1)测量注入fail-stop后的恢复成本，首检查点与额外检查点的价值分开；学习放置策略尚属未来工作。SSH脱离而本作业继续，并不是论文注入崩溃，三份修复失败也不是已做工作丢失，故不增加检查点框架或恢复重跑。主方法与范围／去重决策保存在public-candidate-screen/specification-oracle-and-recovery-screen.json（SHA256=589e8d37999ccd272139232bf5b78ce0dd768ad28f0e2fd414b38b7a8a497432）；两条均无新候选、模型、verifier或正式请求，不作提分结论。

##### 有界上下文组件研究：运行时干预与固定机制分开

[An Empirical Study of Harness Design，固定v1](https://arxiv.org/html/2609.20804v1)已读§2.1—2.4及3.1：持久计划逐轮注入与旧观察遮蔽由宿主实现；规划／bash消融只在T4／128K，不能据此推定本赛32K效果。自动编辑诊断与卡住检测在各组固定，未被单独消融，不提供它们的独立因果收益。作者使用BF16／300步／每轮16384输出，并非Gemma五分钟对照。

与旧前规划、60项native-shell及90项自动诊断负结果去重，不据这篇论文重复提示、shell或语法反馈候选；当前SDK回调registry边界也不改。原始筛查在output/research/public-candidate-screen/empirical-harness-context-screen.json；正在运行的固定五题诊断保持冻结，本来源新增模型／正式请求0。

##### 额外需求说明的输入边界

[Where Should a Stuck Agent Spend Its Next Tokens，固定v1](https://arxiv.org/html/2610.28834v1#S3)的§3.2及附录D说明，specification从参考解／参考patch生成，location从参考hunk与定义生成。去掉直接代码／测试字符串的发表审查不改变其答案来源，因此不能当作本项目可用的无gold需求通道；不取这些数据或在同题中注入，也不把仅用题面的改写当作论文已测干预。来源资格回执output/research/public-candidate-screen/specification-and-wholefile-eligibility-20261027.json。CQ2-CARE已在上文记录，本次复核不计新机制或重开整文件定位实验。

##### 结构检索：定位收益不能直接当作修复收益

[How Do Small Coding Agents Use Code Graphs and Embeddings，固定v1](https://arxiv.org/html/2610.33958v1)的主体是SWE-bench函数定位；可用Gemma为E2B／E4B，12B部分运行异常，没有本比赛31B。下游固定Qwen3-8B仅修复6—13／160，不能换算本项目分数。方法与限制已读，作者源码和原日志未审核，不称已复现

较相关的启示是返回精确符号名与紧凑邻居，而非默认扩大图遍历；部分定位收益来自提交名称格式，强制先检索或加预算没有可靠改善。作者的tool_choice=required需要控制harness，我们现有SDK拒绝追加该字段，不能直接搬入提交。当前仅作证据筛选，不立新候选，不下载含gold标注的划分或轨迹

同赛单shell路线也不是新空白：[既有公开源码核查](public_budget.md)与本项目output/research/native-shell/development/selection.json均已存在。后者完整结案且不采用，旧preparation的零模型请求只代表准备时点，不能据其重启。当前稳定性作业不变，无额外模型／verifier／正式请求
