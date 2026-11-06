##### 资源与训练边界

模型运行前实时检查GPU显存、占用进程和进程创建时间，瞬时0%利用率不代表空闲
只清理本次作业已记录的自有进程，不抢占其他用户或其他session的GPU
当前没有本轮模型／训练作业，不根据旧文档PID推断实时状态

本地历史评测使用A6000、TP1和eager，公开示例使用4张L4及不同服务配置
环境差异见[执行审计](../research/execution_alignment.md)，不把卡数或理论吞吐当实际修复收益

训练是下一阶段待设计事项，先核验训练checkpoint与比赛CT部署侧adapter兼容，再定数据与资源
现有SFT／RL数据就绪标记均为false，详见[训练交接](../research/training_handoff.md)
不因文档存在自动训练、改权重、扩权或购买资源

旧通用硬件备忘录保留在Linux output/archive/review-ready-baseline/agent/workflow/gpu_training_guide.md
