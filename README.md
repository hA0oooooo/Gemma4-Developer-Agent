# Gemma 4 Developer Agent

用 Gemma 4 在真实代码仓库中定位问题、生成补丁，并通过独立测试核验修复的竞赛研究项目

这个仓库保留了一套可继续开发的 Harness、已评分的0.17配置，以及面向后续 SFT／RL 的失败分析与数据要求

##### 当前结果

| 方案 | 我方有效公榜成绩 | 结论 |
| --- | --- | --- |
| 单 Agent、六原生工具、31B | 0.17 | 当前开发基线 |
| 接口约定与预算融合 | 0.13 | 不采用 |
| 公开0.22方案原样包 | 0.15 | 保留复现证据，不替换基线 |

成绩来自既有正式回执，本次仓库整理没有新增提交或刷新榜单

后续多轮局部优化没有形成可接纳的整体收益：减少工具参数错误、增加工具或延长会话，都不能直接等同于完整修复提升
5→8分钟的 K=4 配对研究中，候选与对照分别为24/120、35/120窄测试阳性，原生成本增加20.53%，因此保留5分钟基线
每侧120项由同30道题重复构成，不是120道独立题

研究结论支持将下一阶段重点转到模型：固定 Harness，先补定位、接口语义、跨模块修改和真实验证轨迹，再讨论 SFT 与 RL
详细依据见[Harness结论](agent/research/harness_closeout.md)与[训练交接](agent/research/training_handoff.md)

##### 从这里开始

| 目的 | 入口 |
| --- | --- |
| 理解最终结论、公开0.18比较 | [Harness收尾](agent/research/harness_closeout.md) |
| 选择训练数据与分析 bad case | [训练交接](agent/research/training_handoff.md) |
| 理解本地与公开官方环境差异 | [执行环境审计](agent/research/execution_alignment.md) |
| 构建训练轨迹与奖励 | [轨迹规范](agent/research/training_trajectories.md) |
| 修改 Agent 配置 | [submission](submission/) |
| 查看开发、复核和提交入口 | [基线工作流](agent/workflow/baseline.md) |
| 查找历史研究与负结果 | [研究索引](agent/research/index.md) |

##### 方案如何运行

官方评分端读取声明式 Agent 配置，由模型调用工具浏览仓库、编辑实现和提交补丁，然后在干净副本上应用补丁、执行测试

本项目默认配置与已评分0.17包的四份文本逐字节相同

| 配置 | 内容 |
| --- | --- |
| 模型 | Gemma 4 31B CT，无 adapter |
| 工具 | run_command、read_file、edit_file、write_file、get_status、submit_patch |
| 生成 | temperature 0、输出8192、思考4096 |
| 单题预算 | 5分钟、24次工具调用、40轮 |
| 单命令超时 | 60秒 |

系统提示、采样和预算分别位于 `submission/prompts/system.md`、`submission/configs/sampling.yaml` 和 `submission/eval_config.yaml`
增加 adapter 或切换模型前，先验证训练底座、部署格式和官方加载链的兼容性

##### 本地检查

当前 Linux 工作区位于 `/mnt/data/haoyang/workspace/gemma4-developer-agent`，通过 `ssh baojian` 进入，使用现有 `agent` 环境

```bash
conda activate agent
export LITELLM_LOCAL_MODEL_COST_MAP=True
cd /mnt/data/haoyang/workspace/gemma4-developer-agent
python -m pyflakes src/*.py
python -m unittest discover -s src -p 'test_*.py'
python src/build_submission.py --output output/packages/review.zip
```

这些命令检查代码、回归与声明式打包，不启动 Gemma 或正式评分
测试夹具只含题目身份与划分元数据，单元测试不依赖私有研究输出或官方任务下载

新机器需要先准备官方 SDK 与依赖，参考[环境准备](agent/workflow/official_starter.md)
`requirements.txt` 引用的官方 wheelhouse、任务快照和模型权重均在 `data/`，通过官方渠道获取，不随 Git 分发

真实模型评测使用 `src/run_baseline.py`，配对比较使用 `src/evaluate_development.py`，独立补丁复核使用 `src/check_patch.py`
运行前固定题目、模型、依赖、seed、预算和验收条件，并确认有空闲资源

打包与正式提交是两个独立动作，正式提交入口 `src/submit.py` 必须显式提供新包与描述，不会因运行上述检查而提交

##### 仓库结构

| 路径 | 内容 |
| --- | --- |
| `submission/` | 精确0.17开发基线，四份声明式配置 |
| `src/` | 运行、比较、独立审计、打包和提交逻辑，以及 CPU 回归 |
| `tests/fixtures/` | 可入库的纯元数据夹具 |
| `agent/research/` | 当前结论、训练交接、固定题集清单与历史研究 |
| `agent/workflow/` | 环境与执行说明 |
| `agent/competition/`、`agent/harness/` | 官方资料与接口说明 |
| `data/` | 本地官方输入、依赖和权重，Git 忽略 |
| `output/` | 运行产物、冻结包、回执和历史原型归档，Git 忽略 |

旧实验的原始补丁、轨迹、失败和封存结果保留在 Linux 的 `output/research/`
精确0.17原包位于 `output/research/capacity-trial/submission.zip`，SHA256 为 `baea5d6b2c006d4ac758f79b5cfb2c500eefa84e08b37cc1f220e2a72ccf7563`
重新打包后的 ZIP 容器字节可能不同，应分别核对原包身份和内部配置身份

##### 来源

[比赛页面](https://www.kaggle.com/competitions/gemma-4-developer-agent) · [官方入门 Notebook](https://www.kaggle.com/code/ryanholbrook/getting-started-gemma-4-developer-agent/notebook)

本次说明按 [anti-defensive-writing](https://github.com/Adkid-Zephyr/anti-defensive-writing-Skill) 的问题、方法、证据顺序组织，完整负结果与判定边界保留在研究文档中
