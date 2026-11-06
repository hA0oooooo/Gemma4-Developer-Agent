##### 两阶段评测

每个 issue 独立评测：Container A 用于 Agent 修改仓库，Container B 重新建立干净 snapshot，应用 agent_patch 与正式 test_patch 后验证

模型文本回答或 submit_patch 返回成功不等于 issue resolved

guide 中 resolved=True 的必要条件：pytest exit code 为 0；JUnit XML 存在且至少有一个 passed test，没有 failure/error；所需 FAIL_TO_PASS / PASS_TO_PASS 或 test_patch 提取的测试节点确实通过而未跳过

##### 检查完成与测试通过分开判读

check_patch.py、audit_patches.py和辅助回归检查器的进程退出0，只表示检查流程正常完成、产物已生成，不保证pytest通过。实际看summary.json中的test_exit_code与resolved；辅助扩展检查改用secondary_tests_passed，并核对JUnit的failure/error及真实passed数

批量作业的completed_normally或CLI的COMPLETE也不是修复率。前者看执行完整性，后者看平台终态；任务是否修复仍读各项测试证据，官方分数只认评分结果。不得把“脚本结束”写成“所有测试通过”

指定测试通过与源码需求完整性也要区分。附加既有回归或可见行为探针发现明确缺口时，保留原评分产物、另列质量结论，不在判分后替模型改patch，也不拿局部通过数当完整修复数

官方 §8 定义 Resolution Rate

$$
\mathrm{Resolution\ Rate}=\frac{\mathrm{Number\ of\ Resolved\ Tasks}}{\mathrm{Total\ Tasks\ in\ Evaluation\ Split}}\in[0,1]
$$

##### Patch 与提交链路

submit_patch 使用 git add -N .，随后提取相对 _swegemma_baseline 的 binary diff，必要时回退 HEAD

超时或未显式提交时 harness 可回收非空 diff；仍应验证后显式 submit_patch

当前安装的swegemma 0.2.11源码与data/wheelhouse同名官方wheel逐字节相同：agent_runner.py第1054—1078行在未提交时收集工作区diff；verification.py第697行在resolved=True时将error设为None。因此最终error为空、非空patch和测试通过不能倒推出Agent没有预算终止或已主动提交，显式提交、结束状态与修复判定应分列，不据此修改原始resolved

五工具研究的fastapi_5624候选就是当前实例：完整trace未见submit_patch，记录仍有2090字节补丁、指定测试及另一干净副本各一项通过。这与本地SDK的回收行为相容，不是本项目另加自动修补，也不证明隐藏评分环境当前使用完全相同版本。核实的agent_runner.py源码SHA256为4d7eccabd203c26f7c39e882684d2fd851f383f6a5c76c4a75b0e559cd5d6a18，原始trace及结果保留在output/research/edit-first-menu/development

开发 reproduction 临时脚本应放 sandbox 的 /tmp，避免意外进入 patch

验证阶段会重置被 Agent 修改的受保护测试/runner 配置，再应用正式 test_patch；应修复目标代码，不靠篡改测试获得结果

上传物为 submission.zip；guide 描述官方 inference.py 将 Agent 输出转成 [id, prediction] 的 submission.parquet，prediction 为 patch，metric.py 再执行验证

##### 预算

总体时限见 [比赛说明](../competition/competition.md)；单 issue 的 Agent time budget 在 sandbox setup 后开始，二者不能混同

evaluation.timeout_seconds 是单条命令时限；max_time_minutes 是 Agent 会话预算；max_tool_calls、max_turns 分别约束工具次数与 reasoning turns

官方 guide 的 sample 配置示例为单任务 1 分钟、10 个 tool calls、50 turns，用途是演示，不将其当作合理研究预算

submit_patch 和 get_status 不计 tool_calls，但仍受时间预算约束

SDK结果中的tool_calls是预算计数；trace逐次请求数还可包含不计费工具、参数校验失败或预算被拒绝的调用。报告实际尝试次数时不能直接把它当已计费次数，也不能仅因超过24条trace调用就宣称预算配置失效

##### 耗时字段的边界

本地批量报告的agent_seconds来自SDK TaskResult.duration_seconds，是原生单任务两阶段耗时，不是纯Agent推理或会话时间。源码核实：swegemma 0.2.11的evaluate.py在Phase 1前设置start_time，并将其传给Phase 2的verify_task；verification.py在测试后才计算duration_seconds。因此，补丁验证超时也会增加这个字段，不能用它直接推算官方不含补丁验证的整批Agent额度

case_wall_seconds另含本地执行包装和额外干净副本审核。trace_elapsed_seconds只是已记录事件的最大elapsed_s；没有完整计时边界时，也不能冒充SDK独立记录的agent_elapsed_seconds，更不是纯GPU时间。正式平台与TP1本地服务的硬件、setup和负载不同，不以这些数值承诺官方一定不超时

冻结研究仍保留原始字段、结果和事先规定的成本选择条件，不事后换口径救回候选；报告中的“原生总任务时间”和“完整case时间”按上述范围理解。2026-10-22核对的SDK源码SHA256分别为evaluate.py的96a46f49267ffcf861f7f90b98efbe828d03f27553ceefce745819028589de1e、verification.py的99e2a5fdab2be2b5e0388de29080da9d6e7003cf8b53299cda790464f4ecd2aa

##### 本地验证与产物

官方文档提供 swegemma eval --tasks tasks.jsonl --snapshots-dir snapshots --submission-dir sample_submission --results-dir results --sandbox docker 的入口；支持 --task-id 和 --sandbox subprocess 等参数

开发检查在 Linux 服务器的 agent 环境运行，正式评分仍由 Kaggle 执行，配置与判读见 [baseline 说明](../workflow/baseline.md)

产物包括 summary.json、task_results.jsonl、patches/*.patch、test_output/*.log、traces/trace_<instance_id>.json 与 logs/*.log，统一收集到 output/baseline

当前已取得真实模型、非空补丁与独立干净副本测试通过的完整轨迹；public/private split 及隐藏集表现仍以官方为准。提交限制见 [比赛说明](../competition/competition.md)，SDK 来源见 [Harness 配置](harness.md)，不重复维护

##### 可操作的本地验证

在 baojian 的 /mnt/data/haoyang/workspace/gemma4-developer-agent 执行，环境 conda activate agent，使用已有官方 31B 与四张 A6000；输出目录应尚无需要保留的结果

```bash
python src/run_baseline.py --data data/competition --model data/models/31b --model-name gemma-4-31b-it-qat-w4a16-ct --tensor-parallel-size 4 --agent-dir output/research/budget-matched-control/config --task-id requests_7205 --seed 17 --output output/manual-validation/requests_7205
python src/check_patch.py --task-id requests_7205 --patch output/manual-validation/requests_7205/evaluation/patches/requests_7205.patch --output output/manual-validation/requests_7205/audit
```

第一步只把所选配置复制到输出目录，不修改 submission；第二步在另一干净副本复核。没有非空 patch 时先检查原始结果，不把缺失补丁硬塞给验证器；需要空补丁对照时不传 --patch

验收看 evaluation/task_results.jsonl、traces、patches 和 audit/summary.json、audit/junit.xml、audit/test_output.log，并核实 test_deps.json 的实际 task_venv 安装状态。修复通过要求补丁有效、pytest exit 0、JUnit 无 failure/error、必要测试没有被跳过，与官方 resolved 一致

当前采用官方 subprocess sandbox 的本地适配：已修复 src 布局导入，依赖装入各任务 venv，但没有 Docker daemon 权限，不宣称与 Kaggle 容器完全等价。该方法适合快速排错与比较策略，最终泛化成绩仍需官方评分

批量研究使用 src/run_experiments.py，参数与分类研究计划见 [优化台账](../research/optimizations.md)；不需要启动 Notebook 或正式提交即可获得本地反馈

来源：agent/harness/official_guide.md §7–9，下载日期 2026-10-01

##### 无需 GPU 的批量补丁复核

已有模型补丁可以直接复核，不必每次重新运行模型；清单包含 label、task_id、patch 路径，已有四份真实补丁的示例保存在 output/research/audit-throughput/plan.json

```bash
python src/audit_patches.py --plan output/research/audit-throughput/plan.json --output output/manual-patch-audits --workers 4
```

每项都在不同干净副本使用官方 verify_task，保留原生 JUnit 与 task_venv 依赖记录；该入口不生成新补丁，不启动模型，不消耗 Kaggle 提交次数。输出目录不能已有需保留的同名结果，默认 workers=1，服务器空闲时可并行

当前同四份补丁按两次串行、两次四路并行复核，16 次结论一致，验证墙钟吞吐约 3.47 倍；范围与原始证据见 [开发验证效率](../research/evaluation_efficiency.md)，不能将其描述为 Agent 修复率或官方分数提高

##### 可选的共享服务运行保护

已观察到一个本地 API 进程持续占用 CPU、健康接口无响应，后续任务没有取得模型回复却继续逐项超时。`run_experiments.py --check-service-health` 为此增加可选保护，默认关闭，不默改已经冻结的模型配置或旧运行 profile

开启时，每个 case 开始前最多检查两次健康接口，各有 8 秒上限；两次失败就记录 server-health-error.json、停止后续 case，不重发模型请求。当前 case 仍服从原有任务上限，这不是持续轮询或新的定时监控；不完整的批次不能计为策略质量结果

退出前先保存原服务日志，再调用 SDK 原有 stop，并只终止该 API 已捕获的工作进程后代，必要时强制结束；不向共享进程组发送信号，不扫描或结束其他用户作业。后台任务可能继承忽略 SIGINT，发出信号不等于已退出，须核对实际进程和 GPU 释放

六项无模型检查、原有三种调度检查及十六项比较门禁通过，包含真实自造 CPU 父子进程清理和现有本地健康接口请求；没有人为破坏真实 GPU 任务来冒称已完成自动 GPU 故障恢复验收。该功能只保护开发执行，不修改官方 SDK、任务、测试或计分规则，也不计正向策略因素
