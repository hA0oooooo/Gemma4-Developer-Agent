##### 历史结论如何使用

当前有效结论统一见[harness_closeout.md](harness_closeout.md)，本页用于查找旧研究，不再维护逐轮进度
旧文档的“当前／Goal继续／授权／运行中”均是当时快照，不能作为恢复作业、提交或训练的指令

##### 主要结论

| 方向 | 保留结论 |
| --- | --- |
| 正式评分 | 我方保留0.17，接口预算融合0.13，公开0.22原样包在我方0.15，事后行为检查0.15 |
| 工具与提示 | 调用错误减少、组件可运行和单题成功没有稳定转化为整体晋级，不叠加为有效提分项 |
| 延长预算 | 5→8分钟K=4候选24/120、对照35/120窄阳性，原生成本+20.53%，拒绝 |
| 缩减思考与采样 | 已有完整负结果或稳定性未通过，不用新增seed救回 |
| 补丁回退 | 19差异配对／7题未验证到至少两道合格的先正确后改坏机会，未准入新模型试验 |
| 自建benchmark | 8题／47检查，双方源码支持8/8，存在饱和，只作机制诊断 |
| 读取与测试设计 | 两批同12题三条件共72端点，读取修正支持2对4，测试器思考支持3对3，均拒绝 |
| 验证与环境 | 窄测试不覆盖完整需求；本地配对与公开SDK审计不等于隐藏环境或公榜预测 |

部分早期试验曾有局部正差值、后续未晋级；本页没有将所有历史试验归为同一统计结论
同题重复数、窄阳性、源码支持与正式成绩按各自原协议解释，不能横向拼接

##### 旧文档固定版本

以下链接固定到整理前已推送的d75693b，完整原文、失败、阶段更正与来源仍可追溯
当前工作树删除重复过程文档，不改Git历史，也不改Linux output/research中的冻结产物
论文摘要、旧网页状态与实验数据没有在本次文档去重中逐条重新核验，不能将“保留历史”理解为重新认证全部结论

| 原文 | 内容 |
| --- | --- |
| [action_budget.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/action_budget.md) | 时钟反馈、动作上限及完整失败成本 |
| [atomic_edits.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/atomic_edits.md) | 完整片段编辑、行为检查融合及独立验收缺口 |
| [benchmark_evolution.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/benchmark_evolution.md) | 8道自建诊断题与通过率饱和问题 |
| [context_and_tools.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/context_and_tools.md) | 导航、工具菜单、调用格式与多轮接口研究 |
| [control_flow.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/control_flow.md) | 阶段控制、双草稿、共享预算与并行资格 |
| [decoding.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/decoding.md) | 采样重复、精简政策及稳定性复核 |
| [development.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/development.md) | 开发集抽样、环境资格与失败诊断 |
| [evaluation_efficiency.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/evaluation_efficiency.md) | 共享服务、命令时限、CPU审计吞吐 |
| [execution_feedback.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/execution_feedback.md) | 行为检查、断言反馈与迁移复核 |
| [four_directions.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/four_directions.md) | 四方向阶段交付与机制去重 |
| [generalization.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/generalization.md) | 题目暴露、早期局部信号与泛化边界 |
| [harness2.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/harness2.md) | Harness²固定源码及迁移条件 |
| [harness_goal.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/harness_goal.md) | 旧目标导航，已由当前入口替代 |
| [history.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/history.md) | 早期实验流水与阶段目标 |
| [literature.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/literature.md) | 论文机制、固定源码与适配边界 |
| [navigation_merge.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/navigation_merge.md) | 公开0.22与我方0.17的导航融合 |
| [optimizations.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/optimizations.md) | 早期20项局部因素及后续K=4统计复核 |
| [patch_selection.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/patch_selection.md) | 隔离双补丁选择及未调用机制 |
| [public_budget.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/public_budget.md) | 公开Notebook版本、复现与成绩身份 |
| [qualified_test_repair.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/qualified_test_repair.md) | 真实API门禁及正确性优先修复研究 |
| [read_contract.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/read_contract.md) | 读取接口与参数传输的组件资格 |
| [read_window_repair.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/read_window_repair.md) | 读取修正与测试器思考的两批完整比较 |
| [references.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/references.md) | 研究补充来源，官方目录另见competition |
| [scripted_edits.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/scripted_edits.md) | 精确脚本、成组编辑及统一diff路由 |
| [single_agent_reliability.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/single_agent_reliability.md) | 提交预检原型与共享轮数资格失败 |
| [test_context.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/test_context.md) | 已有测试导航及作用链审核 |
| [test_first.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/test_first.md) | 测试优先双阶段的完整负结果 |
| [thinking_balance.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/thinking_balance.md) | 思考预算缩减与跨题复核 |
| [training_trajectories.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/training_trajectories.md) | 已并入训练交接：轨迹包、身份与转换 |
| [trajectory_diagnosis.md](https://github.com/hA0oooooo/Gemma4-Developer-Agent/blob/d75693be80c6a6b15d1af23c271f03b7a9297d37/agent/research/trajectory_diagnosis.md) | 已并入训练交接：19配对的逐题审核 |

##### 合并范围

research从34份Markdown收敛为5份：导航、最终结论、环境审计、训练交接与本历史索引
训练材料中的重复结果说明去重，保留逐题分母、调用错误证据、轨迹质量、更正覆盖层、分组和loss mask要求
4份JSON是运行／测试使用的固定题集元数据，本次不改内容或路径
