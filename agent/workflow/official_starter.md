##### 当前入口

本文保留官方入门示例的适配快照，历史12B示例不代表当前31B开发基线
当前环境差异见[执行审计](../research/execution_alignment.md)，当前配置与安全打包命令见[基线工作流](baseline.md)

##### 来源与用途

已于 2026-10-13 使用 Kaggle CLI 拉取并完整阅读官方 [Getting Started — Gemma 4 Developer Agent](https://www.kaggle.com/code/ryanholbrook/getting-started-gemma-4-developer-agent/notebook) 的 Markdown、代码和输入 metadata

官方源码保存于 [getting_started.ipynb](../competition/getting_started.ipynb)，作为参考，不作为本项目可编辑的提交配置；源码 SHA256 为 `8e7d84a326acae509fb596163ba085831961b588b86d51af31e037c5319b917c`

它提供从环境配置、代码检索、模型服务、Agent 执行、测试验证到 ZIP 打包的开发示例，已适配到 Linux；运行入口为 src/run_baseline.py，官方 Notebook 保留作参考

##### 官方 Notebook 的六个阶段

| 阶段 | 关键内容 | 在本项目中的位置或用途 |
| --- | --- | --- |
| 环境 | 设置离线 vLLM / LiteLLM 环境，从官方 wheelhouse 安装包 | data/wheelhouse、requirements.txt 与 Conda agent 环境 |
| 数据与 Agent | load_tasks；将只读 sample_submission 复制到可写目录 | data/competition 是输入，submission 是当前策略，output/baseline/agent-config 是开发副本 |
| 代码图示例 | get_graph、get_neighbor、get_similar_nodes、get_induced_subgraph | 理解 graphs / embeddings 和检索工具；图示例本身不产生修复 |
| 模型服务 | VllmServer；gemma4 工具与推理 parser；模型和 LoRA 注册 | src/run_baseline.py 的模型服务部分 |
| 两阶段评测 | Evaluator.evaluate_task；默认检查 tasks[:2] | Agent 生成 patch，再在干净副本验证；查看 patch、pytest、resolved 和 trace |
| 打包 | validate_directory；agent.yaml 放在 submission.zip 根目录 | src/build_submission.py；正式上传仍使用 src/submit.py |

Notebook 中的 DataFrame 只是开发结果展示，正式上传的文件仍为 submission.zip；执行 Notebook 的前两项任务不是官方隐藏测试评分

##### 本次发现的重要变化

当前官方 Notebook 默认 `gemma-4-12b-it-qat-w4a16-ct`；最新官方 guide 也明确允许 31B、12B、E4B、E2B 四个量化模型，已更新本项目模型校验

切换离开 31B 时，Notebook 会同步修改根 Agent 与所有 sub-agent YAML 的 model，删除 adapter 引用及 sample 中的 31B 形状 LoRA；这些 sample adapter 是示例占位，不应当作有效训练策略

Notebook metadata 为 L4×4、Internet=false，挂载 competition、官方 wheelhouse 与四种模型输入；代码实际只启动配置所声明的一个模型，挂载四种模型不代表同时推理四种模型

12B 启动额外传入 `--hf-overrides '{"architectures": ["Gemma4ForCausalLM"], "model_type": "gemma4"}'`，不能只更换模型目录而忽略这一参数

模型服务使用 32768 上下文、自动按可见 GPU 数量选择 TP=4/2/1、按实际 adapter 数量和 rank 配置 LoRA，并通过 `create_model_registry` 注册模型别名

这些是官方示例配置，不能仅根据模型较小或 GPU 可见推断当前服务器已经能完成真实评测

##### Linux 适配边界

服务器仓库：`/mnt/data/haoyang/workspace/gemma4-developer-agent`，环境：`/mnt/data/haoyang/miniconda3/envs/agent`

| Kaggle 路径或机制 | Linux 对应 |
| --- | --- |
| /kaggle/input/competitions/gemma-4-developer-agent | data/competition，保持只读 |
| /kaggle/input/models/google/gemma-4/other/<model>/2 | 实际下载或挂载的模型目录，含 config.json、权重、tokenizer 等文件 |
| 官方 wheelhouse dataset | 官方下载或挂载的运行依赖；与 competition/wheels 的任务测试依赖用途不同 |
| /kaggle/working | output/baseline |
| Notebook 事件循环 run_sync | 普通 Python 脚本可用 asyncio.run，不需要线程包装 |
| display(submission_df) | task_results.jsonl / summary.json 与补丁文件 |
| Copy & Edit / Submit Prediction | Linux 的 build_submission.py 与 submit.py |

Conda 环境已安装所需官方 wheels，没有执行 Notebook 中删除系统 cutlass hooks 的操作

设置 `LITELLM_LOCAL_MODEL_COST_MAP=True` 等环境变量应发生在导入 SDK 之前，本次服务器接口检查曾因远程 cost map 查询超时产生等待

##### SDK 兼容性检查

当前服务器实际安装：swegemma 0.2.11、adk-submission 0.2.13、adk-eval-core 0.1.0、google-adk 1.36.1、google-genai 2.11.0、官方 patched vLLM 0.19.1、transformers 5.13.1、tokenizers 0.22.2、PyTorch 2.10.0

以后安装时先通过 prepare_inputs.py 下载官方依赖，再执行 `python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt`；官方 vLLM wheel 内容带补丁，同名已安装版本需使用 `python -m pip install --no-deps --force-reinstall data/wheelhouse/vllm-0.19.1-cp38-abi3-manylinux_2_31_x86_64.whl` 保证采用该文件

2026-10-13 查询官方 wheelhouse，发现 swegemma 0.2.11、adk-submission 0.2.13、transformers 5.13.1；vLLM 的文件版本仍为 0.19.1，但同名文件也可能包含官方补丁，版本号相同不保证内容相同

已确认 EvalConfig 支持 verification_timeout_seconds；修正旧的模型发现与 registry 导入，使用当前 adk_submission 接口，并将模型服务别名与请求模型名一致绑定

环境 pip check 和源码 pyflakes 通过，原有 Conda agent 环境继续使用，不新建重复环境

Linux HTTP 服务固定使用 FastAPI 0.136.0、Starlette 0.52.1、prometheus-fastapi-instrumentator 7.1.0，避免新版 FastAPI 的 _IncludedRouter 与旧统计插件不兼容而导致 HTTP 500，问题记录见 [vLLM issue](https://github.com/vllm-project/vllm/issues/45597)

官方 wheelhouse 的统计插件 8.1.0 虽修复路由问题，但声明要求 Starlette>=1，而官方 google-adk 1.36.1 要求 Starlette<1；本机采用兼容的 HTTP 依赖组合，保留官方核心 SDK、模型 parser 与 patched vLLM，未修改包元数据来掩盖冲突

全部官方 Notebook 代码单元已通过 Python AST 解析，这仅验证语法，不证明模型服务或任务测试运行成功

##### 上下文缓存与压缩

Notebook 显式传入 ContextCacheConfig 和 EventsCompactionConfig，包括 compaction_interval=15、overlap_size=2、token_threshold=14336、event_retention_size=5

最新 HARNESS_README.md §7.2 明确评分端也使用相同参数，本地 runner 已显式对齐并写入 protocol.json；这些 Python 参数不靠打包 Notebook 写入 submission.zip

后续实验先保持这些官方 runtime 设置，只修改 submission 中的策略，避免把评测器配置差异当作策略收益

主办方已公开确认并修复部分 ADK / vLLM reasoning 兼容问题，参考 [官方答复](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/744354)，旧依赖上的失败轨迹不应直接视为最新 runtime 的表现

##### 后续修改入口

| 想修改的内容 | 本项目入口 |
| --- | --- |
| 系统提示、探索与提交策略 | submission/prompts/system.md |
| 工具列表、Agent 架构、模型或 adapter 引用 | submission/agent.yaml；增加 sub-agent 时沿用官方 schema |
| temperature、输出与 thinking token 预算 | submission/configs/sampling.yaml |
| 工具、turn、时间预算 | submission/eval_config.yaml |
| 模型服务、检索输入、缓存或压缩开发实验 | src/run_baseline.py；harness 设置需核对正式评分一致性 |
| ZIP 格式校验与上传 | src/build_submission.py、src/submit.py |

build_submission.py 已支持四个允许模型，run_baseline.py 根据声明模型设置服务名；12B 的 hf-overrides 和 adapter 清理已实现，model-name 参数只作用于开发副本

##### 运行和结果检查

当前使用 12B、单张 A6000 做开发检查，保留 32768 上下文与当前提交的工具、时间预算

```bash
ssh baojian
conda activate agent
cd /mnt/data/haoyang/workspace/gemma4-developer-agent
python src/prepare_inputs.py
python src/run_baseline.py --data data/competition --model data/models/12b --model-name gemma-4-12b-it-qat-w4a16-ct --output output/baseline --task-id fastapi_15661 --tensor-parallel-size 1
```

data/models/12b 已有完整官方 12B 权重与 tokenizer，data/competition 已有 sandbox/setup.py、全部 124 个测试 wheels 及 fastapi_15661 的 snapshot、graph、embedding；更换任务通过 prepare_inputs.py --task-id <ID> --task-only 增量下载

更换模型需要准备对应权重并让 --model 指向该目录，--model-name 只修改 Agent 配置，不转换权重；权重统一存放 data/models/<模型规格>

既有输入准备完成后，prepare_inputs.py 不重复访问 Kaggle；只有下载新的输入时需要有效登录。遇到 API 401 时，缓存的已登录提示不能证明凭据仍有效，应执行 kaggle auth login --force 后用数据接口核验，不在聊天中传凭据

移植时先跑一个固定任务，核对 agent_patch 非空、干净副本成功应用补丁、pytest 实际执行、test_exit_code 和 resolved，再逐步扩大任务集；原 Notebook 的前两个任务示例不能作为稳健分数估计

正式打包与提交仍沿用以下入口；阅读和整理文档不会自动执行正式提交

```bash
python src/build_submission.py --output output/packages/review.zip
# 正式提交另外显式指定 --file 与 --message，并先取得当轮授权
```

##### 本机 NVML 兼容

服务器已加载 NVIDIA 内核模块 580.159.03，系统管理库为 580.178.04；CUDA 运算可用，但 vLLM 会在通过 NVML 自动识别 GPU 时失败

已从 [NVIDIA 官方驱动包](https://download.nvidia.com/XFree86/Linux-x86_64/580.159.03/) 提取并校验匹配版本的 NVML，存放 data/nvidia；没有安装系统驱动或重启服务器

runner 仅在库版本与当前加载内核一致时，将该目录传入 VllmConfig.nvidia_lib_dir；该设置只影响本项目模型服务子进程

恢复当前兼容库的命令为 `python src/prepare_inputs.py --nvml-driver 580.159.03`，可用 `LD_LIBRARY_PATH="$PWD/data/nvidia" nvidia-smi` 查看显卡

若服务器以后更新并重启驱动，先核对 /proc/driver/nvidia/version 与系统 nvidia-smi，不盲目继续使用旧的兼容库

##### 实际验证

最新结果见 [baseline.md](baseline.md)；最终结论需要真实模型工具轨迹、补丁、pytest 与 resolved 证据，不能仅凭下载完成或模型启动判断
