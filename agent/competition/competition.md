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

2026-10-26新核对[官方模型公告](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/748287)及[现行规则](https://www.kaggle.com/competitions/gemma-4-developer-agent/overview/prizes)：现允许gemma-4-31b-it-qat-w4a16-ct、gemma-4-12b-it-qat-w4a16-ct、gemma-4-e4b-it-qat-w4a16-ct、gemma-4-e2b-it-qat-w4a16-ct，同一提交所有Agent必须同一基座，不能大小模型混用。早期“只能31B”的说明是当时规则，不再作为当前全赛限制；当前冻结本地研究仍固定31B、不变更运行中SDK或模型

小模型可探索单步能力与更多推理轮次的取舍，不代表更快即提分。公告评论曾反馈12B加载及ParallelAgent兼容问题，工作人员回复最新wheelhouse已修复前者；该回复不是本机资格或评分端日志，不以它为理由原地升级冻结环境，也不直接移植未经核实的并发方案

提交 submission.zip，其根目录必须有 agent.yaml；完整格式与限制见 [Harness 配置](../harness/harness.md)

官方总体 Agent 执行上限 12 小时，含 sandbox setup，不含 patch 验证；单任务预算另见 [评测说明](../harness/evaluation.md)

2026-10-25北京时间以官方ListCompetitionPages只读接口复核：Evaluation正文仍为整批12小时、含sandbox setup／不含patch validation，data-description仍写约120题且public／private均分，模型与工具页仍要求同一基座并列出九个原生工具，L4说明仍为四卡96GB、Internet关闭。原始正文及UTC读取时间在`output/research/behavioral-check/official-pages.json`，请求脚本为同目录`read_official_pages.py`；这是规则正文读取，不是新提交、额度或上传权限检查。普通网页工具本次只有空壳，未据此宣称刷新成功；SDK的is_published输出为false，不将其当作已独立证明的前端发布状态

2026-10-19 重新核对[官方 Evaluation](https://www.kaggle.com/competitions/gemma-4-developer-agent/overview)与[Data](https://www.kaggle.com/competitions/gemma-4-developer-agent/data)：隐藏测试约120题，public/private各约一半，来自私有仓库；不是只对公榜一半分配整批时限。eval_config中的max_time_minutes只约束每题Agent会话，不含该题setup，因此不能简单设6分钟并宣称120题必在12小时完成

官方评测 sandbox 离线，指定模型、硬件与上下文限制见 [Harness 配置](../harness/harness.md)；开发 Notebook 的 GPU 资源不能直接当作官方评测硬件

##### TODO

- [ ] 蒸馏的具体边界需主办方进一步澄清，不能把一般外部模型规则理解为无限制许可
- [ ] 核实 Notebook 开发 runtime、Internet 与 accelerator 约束；不把总体评测时限当作 Notebook 限额
- [x] 隐藏测试约120题、public/private各约一半；官方给的是约数，不据此推断具体题目或保证未来数量

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
- 公榜使用 public 测试，最终名次依据 private 测试；当前Data给出约120题且两部分均分
- Foundational Rules 在发生冲突时优先于 competition-specific rules

此前认证 API 核验 numToday=0、numAllowedNow=1；这是当时快照，不是永久余额
