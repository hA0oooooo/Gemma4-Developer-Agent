##### 目录职责

| 目录 | 职责 |
| --- | --- |
| submission | 已评分0.17的四份文本配置，实验不要堆在这里 |
| src | 维护中的执行器、审计、打包、提交与CPU测试 |
| tests/fixtures | 不含issue、gold或测试补丁的身份元数据 |
| agent/research | 研究结论、训练交接、固定清单与历史专题 |
| agent/workflow | 环境与执行方法 |
| data | 官方下载、任务依赖与模型，不入Git |
| output/research | 冻结实验、原始日志、patch、轨迹、回执，不入Git |
| output/archive/review-ready-baseline | 本轮清理前文档、旧Skill原型及专用脚本，不入Git |

历史专题按[研究索引](../research/index.md)查阅，不把其中旧运行记录当当前任务
维护代码与小型元数据夹具随Git分发，原始证据按固定Linux路径查询
官方输入与输出已取消Git跟踪，实际数据不删除，本轮不重写已有Git历史
