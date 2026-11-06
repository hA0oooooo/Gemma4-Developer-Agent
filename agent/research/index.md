##### 当前阅读顺序

[Harness结论](harness_closeout.md) → [执行环境审计](execution_alignment.md) → [训练交接](training_handoff.md) → [轨迹规范](training_trajectories.md)

Harness搜索已结束，当前基线0.17，历史文档中的运行状态、授权和目标均是当时快照
历史负结果保留原路径以维持冻结研究引用，不据旧文档重启实验或提交

##### 按问题查阅

| 问题 | 文档 |
| --- | --- |
| 需求与轨迹难点 | [trajectory_diagnosis.md](trajectory_diagnosis.md) |
| 开发题集与泛化 | [development.md](development.md)、[generalization.md](generalization.md)、[benchmark_evolution.md](benchmark_evolution.md) |
| 工具参数与读取 | [context_and_tools.md](context_and_tools.md)、[read_contract.md](read_contract.md)、[read_window_repair.md](read_window_repair.md) |
| 执行反馈与验证 | [execution_feedback.md](execution_feedback.md)、[qualified_test_repair.md](qualified_test_repair.md) |
| 控制流与补丁选择 | [control_flow.md](control_flow.md)、[patch_selection.md](patch_selection.md) |
| 编辑原型 | [atomic_edits.md](atomic_edits.md)、[scripted_edits.md](scripted_edits.md) |
| 采样与预算 | [decoding.md](decoding.md)、[thinking_balance.md](thinking_balance.md)、[action_budget.md](action_budget.md) |
| 公开版本与论文 | [public_budget.md](public_budget.md)、[references.md](references.md)、[literature.md](literature.md) |
| 优化台账 | [optimizations.md](optimizations.md)、[history.md](history.md) |

##### 固定清单

development_set.json、confirmation_set.json、replication_set.json、remaining_acceptance_set.json是历史抽样与划分清单
它们不含参考修复；题目暴露状态以研究记录为准，清单文件存在不自动证明独立验收

##### 原始证据

Linux output/research保留规则、输入锁、owner身份、完整失败、patch、轨迹、JUnit与正式回执
此次清理前的长导航、长目标、旧工作流及未采用Skill原型保存在output/archive/review-ready-baseline，archive-manifest.json绑定原字节
不修改或重放任何已封存研究producer
