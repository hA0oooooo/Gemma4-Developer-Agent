##### Windows接手入口

开发与实验统一在Linux执行，Windows只作为SSH和Git客户端
使用已有安全通道配置ssh baojian，不复制其他机器私钥、不把凭据写入仓库

进入 /mnt/data/haoyang/workspace/gemma4-developer-agent，解释器 /mnt/data/haoyang/miniconda3/envs/agent/bin/python
先读根README、AGENT.md、研究收尾与训练交接，不根据旧会话恢复作业或创建监控
当前默认submission是精确0.17，Harness搜索已收束；下一轮训练由用户另行选择目标

Windows不下载权重、任务快照或研究原始输出，不建立重复运行环境
代码同步使用既有分支，先fetch再按实际分叉状态处理，不覆盖Linux脏改动或force push
