##### 官方目录契约

官方约束的是 submission.zip 的内容，不规定整个本地研究仓库的布局

submission 目录维护当前精简 baseline，只对其内容打包，不能额外包一层 submission 文件夹

```text
submission/
├── agent.yaml                 # 必需，位于 archive 根目录
├── eval_config.yaml           # 可选，单任务预算
├── configs/sampling.yaml      # 可选
├── prompts/system.md          # 可选
├── sub_agents/*.yaml           # 可选
├── adapters/<name>/            # 可选 PEFT LoRA
│   ├── adapter_config.json
│   └── adapter_model.safetensors
└── skills/<name>/SKILL.md      # 可选 skill manifest
```

Overview 明确要求 agent.yaml；官方 guide 还接受 agent.yml / root_agent.yaml / root_agent.yml 且只许一个 root config，本项目固定使用 agent.yaml

当前只使用 agent.yaml、eval_config.yaml、configs/sampling.yaml 和 prompts/system.md

##### Model 与 Harness 的边界

Gemma 生成推理与工具请求，harness 编译配置、绑定允许的工具、管理预算/上下文、创建 workspace、提取 patch 并验证

官方三层包：adk-submission 负责 validate_directory / compile_submission 与推理服务；adk-eval-core 提供 sandbox、预算与 SessionTrace；swegemma 负责 SWE 任务运行与评分

提交使用声明式 YAML，没有 agent.py / agent_fn Python entrypoint；custom 逻辑应走允许的 tools、AgentTool 或 sandbox skill scripts

##### Agent Config

SandboxedAgentConfig 支持 LlmAgent、SequentialAgent、ParallelAgent 与 LoopAgent

LlmAgent 主要字段：name、model、instruction、tools、skills、sub_agents、adapter、generate_content_config、output_key、include_contents

AgentTool 声明为 tools 下的 agent_tool，config_path 指向 sub-agent YAML，可设置 skip_summarization

instruction 可引用 session state 的 {problem_description} 等；!include 相对包含它的文件解析，文本读作字符串、YAML 递归解析，不允许路径越界或外部 symlink

eval_config.yaml 使用 evaluation 下的 timeout_seconds、max_tool_calls、max_time_minutes、max_turns；含义见 evaluation.md

skill 目录必须有 SKILL.md，frontmatter 包含 name；run_skill_script 在持久 sandbox 中执行，load_skill_resource 读取资源

##### 模型与运行限制

所有主 Agent 和 sub-agent 使用 gemma-4-31b-it-qat-w4a16-ct；可选不同 LoRA adapter，完整 base weights 不是当前必需提交内容

官方 guide 描述评测使用 4×NVIDIA L4、tensor_parallel_size=4、max_model_len=32768；combined prompt / reasoning / output 共用上下文

guide 要求总解包体积小于 3 GiB，含 adapters；其表格列 max_total_size_bytes=3,221,225,472，临界值严格性需后续源码核验，本项目不贴边打包

允许扩展名为 .yaml、.yml、.md、.txt、.py、.json、.safetensors，禁止 pickle 权重与额外 archive 格式

##### 官方工具

| Tool | 作用 |
| --- | --- |
| run_command | 在 workspace 执行命令 |
| submit_patch | 提取修复 diff 并标记完成 |
| get_status | 查询剩余预算与 patch 状态 |
| read_file | 分行读取文件 |
| edit_file | 替换文件内内容 |
| write_file | 创建或覆盖文件 |
| get_code_neighbors | 查询符号邻居 |
| search_similar_code | 基于预计算符号 embeddings 找近邻 |
| get_code_subgraph | 提取指定符号的子图 |

search_similar_code 的离线 query 按符号键或后缀解析，guide 建议传类/函数/模块名，而非任意自然语言句子

默认 run_command 输出上限 5000 字符；read_file 上限 150 行且 10000 字符，研究时必须注意截断

##### Context 与待核验项

guide 描述自动 compaction_interval=5、overlap_size=2、token_threshold=14336、event_retention_size=5；实际版本后续以安装的官方包为准

官方 SDK 来源为 metric/gemma-4-developer-agent-wheelhouse，Kaggle Staff 确认其为固定评分包，不支持 ADK 2.x

核心包版本：swegemma 0.2.7、adk-submission 0.2.12、adk-eval-core 0.1.0、google-adk 1.36.1、google-genai 2.11.0；swegemma 要求 Python >=3.12

模型 runtime：vllm 0.19.1、transformers 5.13.1；Linux GPU runtime 不安装到 Mac 根环境

TODO：实际编译 sample 与完成模型服务、Agent、验证链路；安装证据见 agent/workflow/baseline.md

来源：[官方指南](official_guide.md) §1–3、§5–7；比赛 Overview URL 见 [来源索引](../competition/references.md)，访问日期 2026-10-01
