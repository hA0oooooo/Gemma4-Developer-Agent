##### 两阶段评测

每个 issue 独立评测：Container A 用于 Agent 修改仓库，Container B 重新建立干净 snapshot，应用 agent_patch 与正式 test_patch 后验证

模型文本回答或 submit_patch 返回成功不等于 issue resolved

guide 中 resolved=True 的必要条件：pytest exit code 为 0；JUnit XML 存在且至少有一个 passed test，没有 failure/error；所需 FAIL_TO_PASS / PASS_TO_PASS 或 test_patch 提取的测试节点确实通过而未跳过

官方 §8 定义 Resolution Rate

$$
\mathrm{Resolution\ Rate}=\frac{\mathrm{Number\ of\ Resolved\ Tasks}}{\mathrm{Total\ Tasks\ in\ Evaluation\ Split}}\in[0,1]
$$

##### Patch 与提交链路

submit_patch 使用 git add -N .，随后提取相对 _swegemma_baseline 的 binary diff，必要时回退 HEAD

超时或未显式提交时 harness 可回收非空 diff；仍应验证后显式 submit_patch

开发 reproduction 临时脚本应放 sandbox 的 /tmp，避免意外进入 patch

验证阶段会重置被 Agent 修改的受保护测试/runner 配置，再应用正式 test_patch；应修复目标代码，不靠篡改测试获得结果

上传物为 submission.zip；guide 描述官方 inference.py 将 Agent 输出转成 [id, prediction] 的 submission.parquet，prediction 为 patch，metric.py 再执行验证

##### 预算

总体时限见 [比赛说明](../competition/competition.md)；单 issue 的 Agent time budget 在 sandbox setup 后开始，二者不能混同

evaluation.timeout_seconds 是单条命令时限；max_time_minutes 是 Agent 会话预算；max_tool_calls、max_turns 分别约束工具次数与 reasoning turns

官方 guide 的 sample 配置示例为单任务 1 分钟、10 个 tool calls、50 turns，用途是演示，不将其当作合理研究预算

submit_patch 和 get_status 不计 tool_calls，但仍受时间预算约束

##### 本地验证与产物

官方文档提供 swegemma eval --tasks tasks.jsonl --snapshots-dir snapshots --submission-dir sample_submission --results-dir results --sandbox docker 的入口；支持 --task-id 和 --sandbox subprocess 等参数

真实模型在 Kaggle 运行，Mac 用于代码维护和本地模拟检查，配置与判读见 agent/workflow/baseline.md

产物包括 summary.json、task_results.jsonl、patches/*.patch、test_output/*.log、traces/trace_<instance_id>.json 与 logs/*.log，统一收集到 output/baseline

TODO：核实 public/private split 的具体划分，取得完整一次验证轨迹；提交限制见 [比赛说明](../competition/competition.md)，SDK 来源见 [Harness 配置](harness.md)，不重复维护

来源：agent/harness/official_guide.md §7–9，下载日期 2026-10-01
