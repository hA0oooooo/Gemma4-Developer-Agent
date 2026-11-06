##### 研究入口

Harness研究已收束，后续在固定0.17配置上讨论模型训练，当前不恢复历史实验或Goal

| 文件 | 唯一职责 |
| --- | --- |
| [harness_closeout.md](harness_closeout.md) | 最终Harness结论、公开方案比较与正式评分边界 |
| [execution_alignment.md](execution_alignment.md) | 本地与公开官方执行环境的一致、差异及未知项 |
| [training_handoff.md](training_handoff.md) | bad case、数据资产、训练转换与奖励要求 |
| [history.md](history.md) | 主要历史结论与整理前原文固定链接 |

##### 固定题集

development_set.json、confirmation_set.json、replication_set.json、remaining_acceptance_set.json保留原路径
它们是历史抽样／划分元数据，运行入口和测试依赖这些身份，不代表题目仍未见
原始patch、轨迹、JUnit、冻结协议与正式回执留在Linux output/research，不随Git分发

旧文档已合并，完整原文通过history中的固定Git版本查阅，不在当前目录重复保存运行流水
