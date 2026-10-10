##### 官方来源

访问日期均为 2026-10-01

| Title | URL | Purpose | Access Date |
| --- | --- | --- | --- |
| Competition / Overview | https://www.kaggle.com/competitions/gemma-4-developer-agent | 名称、timeline、模型约束、提交格式与奖金 | 2026-10-01 |
| Competition Data | https://www.kaggle.com/competitions/gemma-4-developer-agent/data | 认证 CLI 已列出 524 个官方文件，包含 guide 与 sample_submission | 2026-10-01 |
| Harness & Competitor Guide | https://www.kaggle.com/competitions/gemma-4-developer-agent/data | 官方 HARNESS_README.md，完整原文保存 agent/harness/official_guide.md | 2026-10-01 |
| Competition Rules | https://www.kaggle.com/competitions/gemma-4-developer-agent/rules | 登录浏览器完整核验，提交次数、外部资源与 winner obligations | 2026-10-01 |
| Competition Code | https://www.kaggle.com/competitions/gemma-4-developer-agent/code | 官方入口，仅登记 URL，当前不调研或下载社区 Notebook | 2026-10-01 |
| Paper Track | https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/overview | 独立论文赛道入口 | 2026-10-01 |
| Official SDK Wheelhouse | https://www.kaggle.com/datasets/metric/gemma-4-developer-agent-wheelhouse | 官方固定 Python 包及模型 runtime wheels | 2026-10-01 |
| Host SDK clarification | https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/743800 | Kaggle Staff 确认 wheelhouse 为准，不支持 ADK 2.x | 2026-10-01 |
| Required model | https://www.kaggle.com/models/google/gemma-4/Other/gemma-4-31b-it-qat-w4a16-ct | 官方指定模型，实际 Kaggle framework 为 Other | 2026-10-01 |

##### 下载记录

使用此前已认证的 Kaggle CLI 下载官方 HARNESS_README.md，账号可访问该文件，无需提供新 token

保留下载原文，不修改官方内容；文档中具体字段和默认值需在后续安装官方 SDK 后交叉检查

已下载官方 guide、完整 sample_submission、tasks.jsonl、fastapi_15661 snapshot 和五个核心 SDK wheels；未下载第三方 Notebook 或 clone GitHub 仓库

Notebook 开发状态和安装排障记录见 agent/workflow/baseline.md，包存在或导入成功不等于完整 issue 已评测

Google / DeepMind 的一般 ADK 文档不能自动替代本比赛受限配置 schema，当前以比赛 guide 为准
