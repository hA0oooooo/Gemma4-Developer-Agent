##### 最小 baseline 配置

submission/ 使用官方声明式 schema，配置如下

| 项目 | 值 |
| --- | --- |
| 模型 | gemma-4-31b-it-qat-w4a16-ct |
| Agent | 单 Agent，无 sub-agent、无 adapter |
| 工具 | run_command、read_file、edit_file、write_file、submit_patch |
| 时间 / 工具调用 / turns | 10 分钟 / 8 / 20 |
| 单条命令超时 | 60 秒 |
| sampling | temperature 0.2、top_p 0.95 |
| 输出 / thinking tokens | 1024 / 256 |

提示要求最多 3 次探索调用后开始修改，使用短输出，最后调用 submit_patch，相关文件和参数可直接编辑

这是面向基础流程的精简 baseline，不是原样官方 sample，也不承诺任务修复分数

##### 提交与模型评测

打包 Notebook 仅将 submission/ 内容写到 /kaggle/working/submission.zip，agent.yaml 位于 ZIP 根目录

正式提交后，官方评分服务解包配置、启动指定模型、生成 patch 与 submission.parquet，再验证测试

开发 Notebook 产出提交包、正式评分接受提交、任务 resolved 是三个独立状态，不能互相替代

run_baseline.py 可在 Linux GPU 环境读取相同 submission/ 与预算调用官方 Evaluator，用于可选的单任务开发检查

##### 已验证

- 本地 SDK 校验目录与指定模型通过
- 精简配置在官方编译器和本地模拟 Agent loop 中执行完成
- 模拟链路产出 273 字节补丁并进入 pytest，test_exit_code=2、resolved=False、error=None；模拟模型仅检查链路
- 打包仅含 agent.yaml、eval_config.yaml、configs/sampling.yaml、prompts/system.md，原始官方输入未修改

2026-10-07 CPU Notebook 在 Kaggle 成功完成，根目录产出 1315 字节 submission.zip，下载到 output/deployment 后逐文件核对与本地 submission 一致

提交包的构建、部署与回收已验证

2026-10-07 20:51（北京时间）用户授权正式提交后，Kaggle 已接受 submission.zip，提交记录 ref=56911231

2026-10-09 05:15（北京时间）官方 API 确认此前 CPU 打包提交 ref=56911231 已从 ERROR 变为 COMPLETE，公榜分数为 0.05

这条提交已验证构建→部署→提交→官方评分返回闭环；尚未取得评分日志，不能逐项核实模型轨迹、补丁应用与 pytest，也不能据此断言后续提交均会成功。此前平台系统错误没有持续，CPU 打包并非必然导致评分失败

用户于 2026-10-08 授权将打包 Notebook 改为 T4×2 GPU 并重新提交一次，baseline 配置与 ZIP 文件内容保持一致，用于检验 Notebook GPU 设置这一差异

当前结果：T4×2 打包 Notebook 已 COMPLETE，CLI 回读确认 enable_gpu=true、machine_shape=NvidiaTeslaT4、Internet=false、private=true；下载 ZIP 完整且逐文件与 submission/ 一致

2026-10-09 23:27（北京时间）官方 API 与提交详情均确认 GPU 打包提交 ref=56933910 为 COMPLETE / Succeeded，公榜分数为 0.05，描述为 Minimal baseline: GPU packaging, unchanged agent configuration

CPU 与 GPU 打包的相同 baseline 均已获得 0.05，构建→部署→正式提交→官方评分返回闭环已跑通，未发现必须使用 GPU 打包才能评分的证据。提交详情仅提供分数与 submission.zip 下载，没有评分日志入口，尚不能逐项审核模型推理、补丁应用与 pytest。评分监控已结束，不追加提交

##### 参考流程

官方 [Getting Started](https://www.kaggle.com/code/ryanholbrook/getting-started-gemma-4-developer-agent) 使用根目录 submission.zip 并在评分时运行配置

公开 [Working Baseline](https://www.kaggle.com/code/leoprovorov/gemma-4-agent-working-baseline) 展示配置校验与打包入口，未复制其策略或以其成绩作为本项目结论

官方 [提交说明](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/743683) 提醒先完成 Notebook 并生成 submission.zip，再提交评分
