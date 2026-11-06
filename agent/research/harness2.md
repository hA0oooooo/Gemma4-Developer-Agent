##### 结论与使用边界

Harness²适合借鉴为开发阶段的策略优化方法，目前不适合直接替换Gemma比赛的官方执行器，也不建议把完整递归放进每道隐藏题

它优化模型周围的提示、工具说明、记忆、技能和编排，不训练模型权重。我们可以在Linux开发集上借用“提出改动→执行对照→按行为差异组合→保存有证据的经验”，最后只提交符合官方声明式schema的静态策略

本次只完成官方源码审阅，没有安装运行外部模型通道、调用付费API或把该框架放入正式包；所有迁移建议仍是假设，不计作正向点

##### 固定源码与实际调用链

来源：[Google Research官方仓库](https://github.com/google-research/harness2)，本次固定提交为`1cfe254e8d25b15f37048c3730134686abe60335`

```text
cli/run_sweep.py::_main
  → core/schedule.py::run_sweep / run_domain / run_task
  → core/recursion.py::run_mode → run_parallel / run_sequential
  → core/selection.py::selection_pool / run_selection / reflect_adoption
  → core/library.py::Library.add
```

- [recursion.py](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py)：从当前任务的基础执行出发，提出通用与领域相关的候选，实际试跑，再组合改进；parallel与sequential分别扩展宽度与深度
- [context.py](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py)：把任务、完整轨迹、产物、候选配置及历史经验作为文件供改进器读取，而不是只给成功率摘要；包含grader-verdict标记检查
- [selection.py](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py)：匿名化候选产物后选用并反思；发布流程的选择池只包含组合后的finals，明确排除基础执行，不天然保证“差则退回baseline”
- [library.py](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/library.py)：按领域保存已选harness完整文件树和经验，经验要求cue、lesson、evidence；同领域任务只能读更早的记录
- [spec.py](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py)：用BenchmarkAdapter连接任务与验证接口，用Substrate连接实际执行框架；发布的benchmark为JobBench、LAB与WorkBuddy，执行底座为OpenCode与Codex，没有现成Gemma比赛适配器

这是源码中已实现的文件编辑、试跑与经验更新机制，不是参数学习，也不是“递归就必然持续提升”的保证

##### 哪些部分可以迁移

| 机制 | 我们的使用方式 | 当前判断 |
| --- | --- | --- |
| 轨迹与产物驱动改进 | 将空补丁、无效调用、收尾超时、窄测试误通过分别分析，再只改一个策略机制 | 适合开发侧复用，不把反思文字当修复证据 |
| 通用候选与领域候选分开 | 通用工具契约与框架级导航经验分别提出，再测组合是否优于各自单独版本 | 值得做受控消融，不能按任务编号指定修复 |
| 经验必须有证据 | 保存触发条件、通用教训、适用边界、来源轨迹；负例也保留 | 适合简短持久文档，不保存题目答案或gold diff |
| 多候选试跑与组合 | 放在旧开发集离线执行，统计所有候选与失败的总成本 | 可以研究，不直接给每道隐藏题复制整套流程 |
| 在线跨任务经验库 | 依赖任务顺序、持久目录和写回能力 | 官方接口与隔离边界未验证，暂不依赖 |
| 模型自选结果 | 只作开发建议，另用官方测试和源码审查验收 | 不替代当前质量与预算门槛，不照搬finals-only选择池 |

##### 为什么不直接整体部署

[实际递归代码](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py)按每个任务安排`4k`次执行与`3k`个改进阶段，基础执行也在其中；`k=1`仍不是一次普通Agent执行，还需考虑选用、反思及重试开销。这不是总费用的简单七倍公式，但足以说明不能沿用单次五分钟预算就认定整批可行

本比赛全部任务共享12小时Agent执行额度，包含sandbox setup；当前预算设计约为五分钟乘约120题，已经只名义留出约两小时额外空间。本地A6000/TP1时间不能直接标定官方L4/TP4时间，更不能在隐藏题上无条件扩成四次完整求解

框架默认通过OpenCode、Codex及配置的外部模型通道执行，不是直接调用本比赛已安装的ADK/Gemma接口。完整移植需要新的BenchmarkAdapter与执行底座，还需将可编辑文件树约束到官方允许的agent.yaml、prompts、skills和相应配置；Codex hooks、任意plugins及外部API不能默认视为官方可迁移能力

[官方实验指南](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md)明确说明发布版不限制网络，Codex执行时关闭自身sandbox，并记录过任务执行读取公开rubric的情况。因此源码的关键词检查不是答案隔离证明；若未来适配，继续使用现有离线任务网络与只读官方输入，不让答案、评分文件或验证器结果进入策略改进上下文

##### 最小可测方向

优先借用方法，不立即安装整套依赖或启动新模型服务。已有论文与代码审阅不自动成为实验收益

- 先在旧30题真实失败轨迹中选一类通用问题，例如重复同形调用或未完成调用点检查；不使用两组已封存独立题及剩余未见题的结果调策略
- 提出一个小型提示或工具说明改动，记录预期改善的行为与可能代价；候选不能包含任务编号、特定题目答案或评分反馈
- 保持模型、采样、任务预算、环境和数据不变，完成同题配对；保留全部失败、超时、空补丁和完整耗时
- 若要组合通用与领域经验，分别测单独项和组合项，不把一次组合通过归因于其中任意单项
- 只有现有执行、依赖、原生/另一干净副本、JUnit及统一源码审核门槛通过，且修复或完整成本满足预定规则，才保存为候选经验；选择池始终保留原参考，允许明确拒绝
- 开发筛选后才另冻结一次与原已评分baseline的独立验收；经验库此时不再更新，避免把验收集变为在线训练流

##### 本次试投与本方法的关系

本次用户明确授权先试投一次的是既有deliberation-capacity候选，未加入Harness²代码、经验库或递归执行。它仍是官方31B、六个原生工具、五分钟/24动作/40轮、8192输出/4096思考的四文件配置

该试投是探索性官方反馈，不等于稳定性、独立验收或约0.14目标已经达成；提交回执保存在output/research/capacity-trial/submission.json，当前状态以该回执及官方查询为准
