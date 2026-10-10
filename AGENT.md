##### 项目目标

保留一个精简的声明式 baseline 和清晰的提交、评测流程，本文件作为导航；README 暂不创建，后续用于对外介绍

##### 目录职责

- agent：全部参考文档，按 competition、harness、workflow 分类
- data：数据与运行依赖，data/competition 保留官方任务、仓库快照、sample_submission 和 SDK，输入只读
- output：全部生成结果，kaggle 为部署文件，deployment 为回收提交包，baseline 为真实评测产物，local-check 为模拟产物
- submission：唯一可编辑的最终提交配置，直接打包到 ZIP 根目录；configs 与 prompts 保留配置引用所需结构
- src：核心脚本，直接放在此目录，不另设单一 agent 子目录

##### 文档导航

- [比赛与规则](agent/competition/competition.md)
- [来源索引](agent/competition/references.md)
- [Harness 配置与工具](agent/harness/harness.md)
- [评测与结果判读](agent/harness/evaluation.md)
- [官方 Harness 原文](agent/harness/official_guide.md)
- [Baseline 配置与当前结果](agent/workflow/baseline.md)
- [本地模拟检查](agent/workflow/local_check.md)

##### 操作入口

在仓库根目录执行，所需环境见本地检查文档

- 校验并打包：`.venv-harness/bin/python src/build_submission.py`
- 生成部署 Notebook：`.venv/bin/python src/build_notebook.py`
- 回收并核对部署包：`.venv/bin/python src/collect_run.py`
- 本地模拟检查：`.venv-harness/bin/python src/run_local_mock.py`
- Linux GPU 单任务评测：`src/run_baseline.py`，通过 `--data`、`--model`、`--output` 指定输入与输出

##### 工作约定

- 官方 sample 保持只读，当前精简配置维护在 submission
- 使用固定语义路径，不建立编号实现副本或逐次运行历史
- 不修改 data/competition，不将解答字段传给 Agent
- 当前只做低预算 baseline 和基础流程，不训练；已有正式提交完成评分，监控已停止，不自动追加提交
- 本地模拟仅检查 harness 逻辑，真实模型与测试结论以 Kaggle 产物为准
- 改动后执行 `.venv-harness/bin/python -m pyflakes src/*.py`
- 本地安装包使用清华或阿里镜像
- 打包 Notebook 只生成提交包，无需模型挂载；CPU 与 T4 GPU 均已取得成绩，当前生成器保留已验证的 T4 配置，目录整理不改变运行策略
- 浏览器不得修改 Notebook 标题，持久入口为 haoimba/gemma4-developer-agent
- 不因排队或暂未完成重复部署
- 不在仓库或输出中保存凭据
