##### 当前状态

Harness研究已收束，当前开发基线是已评分0.17的单31B／六原生工具配置
先读 README.md、agent/research/harness_closeout.md、training_handoff.md 与 execution_alignment.md
训练是下一阶段方向，目前没有训练就绪数据、已验证adapter或训练启动授权

本轮用户授权整理README、清理冗余、提交并推送仓库；不启动模型、训练、Kaggle提交或监控，不恢复历史Goal与定时任务
旧文档中的“当前／运行／授权”是当时快照，不据其恢复任务
旧根导航与目标全文、未采用Skill原型留在 output/archive/review-ready-baseline，原始结果仍在 output/research

##### 工作区

主机 ssh baojian
仓库 /mnt/data/haoyang/workspace/gemma4-developer-agent
解释器 /mnt/data/haoyang/miniconda3/envs/agent/bin/python

submission/仅保留精确0.17四文件开发基线，实验候选另建到output/research/<机制>/，不要混入默认打包目录
src/维护共享运行逻辑，tests/fixtures/只保留纯元数据，agent/记录结论与规范，data/与output/均不入库
研究脚本及历史原型不混入维护代码；新README已获用户明确授权

##### 证据与执行纪律

- 只报告已验证、部分、待办与受阻的确切状态，区分工程资格、本地质量与实际官方成绩
- 官方任务、测试和计分器只读，不读gold设计策略，不向Agent注入参考修复
- 保留所有失败、空patch、超时、skip、JUnit身份例外和全部成本；不回写旧结案或重放封存producer
- 旧开发题已反复暴露，同题多seed不是新独立任务；预留题不自动解封
- 未来新实验按当轮授权设置有限目标，预先固定候选、精确对照、题／seed、依赖、预算与准入规则；运行中不改输入或放宽门槛，不因SSH中断重复启动
- 单批模型实验，仅用空闲资源，不停止或抢占其他session作业；不擅自改权重、训练数据、权限或购买资源
- 实际补丁须绑定自身源码、原生与独立干净副本测试及行为需求；退出0、窄测试绿、非空patch均不等于完整修复
- 正式提交须有当轮明确授权及完整依据，核对官方预算、账户、额度、待评分、包身份与防重回执；请求不明先查记录，不自动重发
- 所有操作使用CLI，不用computer use或VPN界面；凭据不进聊天、日志或Git
- 不覆盖无关脏改动，不擅自推送或改历史；阶段提交按用户当轮授权执行

##### 代码检查与保护对象

代码修改后运行 python -m pyflakes src/*.py 与受影响CPU测试
完整回归 python -m unittest discover -s src -p 'test_*.py'
打包必须显式 --output 指向新路径，不重建受保护包

以下文件永久保留原字节
- output/research/capacity-trial/submission.zip
- output/submission.zip
- 已封存实验的规则、输入、结果、人工标注与原始回执

旧冻结研究绑定旧执行器身份，后续维护改动不回写它们
SSH或权限阻塞仅做少量安全核查后请用户协助，观察失败不等于进程停止
