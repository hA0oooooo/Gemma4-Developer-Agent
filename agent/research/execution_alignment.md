##### 审计结论

2026-11-06只读审计完成，未发现检查范围内官方公开SDK／Gemma4解析源码与本地漂移，但不能认证本地与隐藏评分器完全等价，也没有证据把官方0.17停滞全部归因环境

审计对象分三层：当天获取的公开Wheelhouse V31、固定官方入门源码357794271、我方K=4真实240个有效端点的protocol／依赖回执。公开示例和SDK都不等于拿到了隐藏评分器镜像

##### 已核实一致

| 项目 | 证据 | 范围 |
| --- | --- | --- |
| adk-eval-core0.1.0 | 官方／本地轮包相同，44份.py成员一致 | Python源码 |
| adk-submission0.2.13 | 轮包相同，20份.py成员一致 | Python源码 |
| google-adk1.36.1 | 轮包相同，542份.py成员一致 | Python源码 |
| swegemma0.2.11 | 轮包相同，34份.py成员一致 | Python源码 |
| vLLM0.19.1 | 10份Gemma4模型／工具／思考／chat／LoRA相关源码一致 | 不是整个433MB轮包、二进制或GPU内核 |
| 上下文配置 | 32768，cache2048／1800秒／10，compaction15／overlap2／14336／retention5 | 配置一致，不是实际摘要内容一致 |

公开V31当前元数据仍为2026-10-12更新。四个小轮包只下载审计未安装；vLLM通过合法公共HTTP206读取中央目录和选中源码，共10次请求、1,250,464字节，没有下载整个轮包或启动模型

模型本地source记录指向Google31B CT／2，config是4-bit compressed-tensors、bfloat16；小配置、tokenizer与chat_template已指纹化。本轮没有全权重hash或独立官方tokenizer下载，不宣称完整字节一致

##### 已知差异与未知项

| 维度 | 本地已记录状态 | 公开参考／隐藏端边界 |
| --- | --- | --- |
| 硬件与并行 | K=4全部A6000、每任务TP1、concurrency1，两分片严格串行协议 | 官方L4x4，入门源码有4卡时选TP4；未做GPU速度对照 |
| 服务 | 全240端点eager=true、max_num_seqs16；代码util0.80 | 入门源码util0.90、未显式eager／maxseq；隐藏实际命令未知 |
| 精度 | dtype=auto，模型config为bfloat16 | 入门按硬件选择bfloat16／auto；不声称有效dtype必然不同 |
| seed | 四固定seed注入编译Agent，不强制后台摘要seed | 示例未固定seed，隐藏未知；零温不保证完全确定 |
| 依赖 | 全240端点隔离profile7f285409…、system_site_packages=false、补充轮包、pip0 | 公开示例不调用我们的依赖修正；隐藏依赖库存未知 |
| 导入 | 本地每条命令加checkout src／root的PYTHONPATH并保留JUnit | 是本地适配，不是SDK本身字节修改；不能称原样官方环境 |
| Python／隔离 | 本地驱动3.12.15、子进程及私有网络scope | 示例是subprocess；归档Docker设计的3.13不证明隐藏后端是Docker |
| 验证／计时 | 原生再加独立干净副本；全case含失败和验证成本 | 官方12小时含setup、不含补丁验证；两种成本不能直接换算 |
| 依赖请求链 | 本地LiteLLM1.104.2、transformers5.13.1等版本有记录 | 隐藏全依赖锁、容器digest和原始请求未取得 |

一个真实FastAPI回执使用pydantic2.14.0，官方公开轮目录提供2.13.4，还存在补充测试依赖与导入位置差异。这是为了让公开验证可靠的本地适配，不可据此推断隐藏生产环境也缺包，或事后改旧分数

当前SDK验证默认与单命令超时分开；eval_config.timeout_seconds60／240不等于统一把官方补丁验证改成60／240。归档官方说明的phase2默认300秒与官方总12小时边界分别记录

此前“本地不是官方Docker”的说法需收紧为“未证明与隐藏环境等价”：官方当前示例本身就使用subprocess，实际隐藏后端未独立核实

##### 有限CPU行为校准

通过安装的FunctionTool实际分派四个自造调用：正确参数保留；带引号的错误可选键被过滤并回到1／150默认；缺filepath回报必填错误；合法参数加无关键不会改变有效值

4项全部通过，没有真实read_file、仓库、模型、verifier或生成token解析执行。结合对应官方源码一致，只证明该分派行为不是本地特有的版本漂移；历史畸形参数缺原始生成文本，不能唯一判模型或parser责任

共享动作／轮数、回调注入等既有资格不重跑也不扩大结论；新增Skill或辅助Agent仍须自己的端到端预算资格，不能借本审计声明可提交

##### 对本地benchmark和训练的影响

[工作人员原帖](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/747248)确认公开训练仓库与测试仓库不重合、隐藏测试在参考修复下均可通过；本轮仅引用官方说明，没有运行或利用gold。参与者关于公开题失败的统计不当作我们新实验或隐藏缺陷证明

本地同环境配对仍能诊断自己的行为和成本，但任务熟悉、仓库分布、依赖、验证噪声与推理后端差异使其不能直接预测公榜。训练前应冻结可信验证和任务暴露记录，不能把高分标题、公共题依赖补齐或一个绿色reward当泛化能力

本审计没有找到足以撤销既有K=4 REJECT的证据，没有建立“环境对齐后会突破0.17”的预测。未知生产细节保留，不通过修改官方SDK、重交旧包或持续试分补齐

##### 原始证据

output/research/harness-closeout/execution-alignment.json包含13项矩阵、来源和SHA；package-alignment.json为640／10源码比较；frozen-runtime-inventory.json覆盖240有效端点；argument-calibration.json保留4项调用和实际返回

官方来源为Wheelhouse V31、官方入门固定版本，以及[模型更新讨论](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/748287)。完整轮包下载、选中源码范围、CPU校准与未知项分别记录，没有将公开参考提升为隐藏环境认证
