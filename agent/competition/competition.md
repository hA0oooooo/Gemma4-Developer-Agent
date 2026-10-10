##### 比赛信息

官方名称：Google - The Gemma 4 Developer Agent Competition

主办方：Google DeepMind；Kaggle Featured Prediction Competition，主赛道授予 points / medals

[官方 Overview](https://www.kaggle.com/competitions/gemma-4-developer-agent)，访问日期 2026-10-01

任务是让 Agent 在真实仓库中解决 issue 并产出修复 patch，重点包含仓库探索、连续工具操作与测试反馈

##### Timeline

| 事项 | 官方 UTC 日期 |
| --- | --- |
| 开赛 | 2026-09-23 |
| 可选论文提交 | 2026-11-12 |
| 报名与队伍合并截止 | 2026-11-25 |
| 最终提交截止 | 2026-12-02 |

截止时刻为对应日期 23:59 UTC，北京时间为次日 07:59；正式提交前重新检查官方是否更新

主赛奖金 $65,000，前三名分别 $37,000 / $18,000 / $10,000；独立 Paper Track 奖金 $35,000

##### 提交与资源

提交 submission.zip，其根目录必须有 agent.yaml；完整格式与限制见 [Harness 配置](../harness/harness.md)

官方总体 Agent 执行上限 12 小时，含 sandbox setup，不含 patch 验证；单任务预算另见 [评测说明](../harness/evaluation.md)

官方评测 sandbox 离线，指定模型、硬件与上下文限制见 [Harness 配置](../harness/harness.md)；开发 Notebook 的 GPU 资源不能直接当作官方评测硬件

##### TODO

- [ ] 蒸馏的具体边界需主办方进一步澄清，不能把一般外部模型规则理解为无限制许可
- [ ] 核实 Notebook 开发 runtime、Internet 与 accelerator 约束；不把总体评测时限当作 Notebook 限额
- [ ] 核实 public/private split 与排行榜评测规模

Paper Track 为独立报名入口，不能把论文提交替代主赛 submission，来源见 references.md

##### Rules 核验 — 2026-10-01

已通过登录浏览器读取完整 [Rules](https://www.kaggle.com/competitions/gemma-4-developer-agent/rules)，页面显示账户已接受规则

- 每日最多 1 次正式 submission，可选择最多 2 个 Final Submissions；Notebook 开发运行不等于正式 submission
- 队伍最多 5 人，使用一个账户且只能加入一个队伍
- 外部数据必须可由所有参赛者公开、免费或合理低成本获取；外部模型的一般许可不豁免指定运行模型约束
- 比赛数据不得分发给未接受规则的非参赛者；禁止队伍之外的私下代码或数据共享
- 公开共享代码应通过比赛论坛或 Notebook，使用允许商业使用的 OSI 许可
- 不得人工标注或人工生成验证／测试样本预测
- winner license 为 Apache 2.0，获奖者需要交付训练／推理代码、运行环境及可复现说明
- 公榜使用 public 测试，最终名次依据 private 测试；数量与比例尚未确认
- Foundational Rules 在发生冲突时优先于 competition-specific rules

此前认证 API 核验 numToday=0、numAllowedNow=1；这是当时快照，不是永久余额
