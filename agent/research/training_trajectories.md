##### 2026-11-06收尾补充：从Harness转向权重研究

Harness审计已完成，入口harness_closeout.md与execution_alignment.md。已验证0.17 ZIP继续冻结，本轮没有训练、改权重、重新导出轨迹或制作新的训练数据集

下文60条／30题的研究包及false就绪标记保持原值。新完成的19配对／38侧诊断另属K=4差异子集，只覆盖7题，不能直接合并为独立训练样本；需先统一任务／seed／补丁身份与曝光分组

未来第一个训练Goal应先确认训练底座与精确比赛CT部署链，验证tokenizer模板、角色／工具边界、assistant loss mask、adapter保存重载和实际输出变化，再在固定0.17 Harness／共同预算下比较base与adapter

训练checkpoint、量化路径、模块映射与GPU资源尚未在本轮验证；“可训练”类属性或LoRA加载日志不能代替真实兼容性与效果测量。本轮不授权启动后续训练

公开训练仓库不在隐藏测试中，旧熟题率不能作泛化估计。模型正样本／奖励必须区分有限需求支持、完整修复、协议违规、验证不稳和未知；工具输出／人工审查／独立verifier不混入assistant训练目标，解析后ATIF不冒充原始生成token

以下保留原始研究包说明与证据范围，不回写旧质量标签

##### 自有轨迹研究交接

此包供另一个训练研究session做数据检查与方案设计，不执行SFT／RL、不改权重，也不等于可直接训练的数据。数据、代码和原始证据都留在Linux

固定工作区为/mnt/data/haoyang/workspace/gemma4-developer-agent，解释器为/mnt/data/haoyang/miniconda3/envs/agent/bin/python

| 文件 | 内容 |
| --- | --- |
| output/research/four-directions/trajectories.jsonl.gz | 60条完整解析后ATIF、自生成最终补丁、实际配置、来源和质量标签 |
| output/research/four-directions/trajectory-manifest.json | 数量、分组、去重、范围及所有包文件SHA |
| output/research/four-directions/tool-schemas.json | 当前安装的六个原生工具声明，不是逐请求捕获的OpenAI／vLLM线格式 |
| output/research/four-directions/quality-corrections.json | 原封签审核的一处更正及其源码证据，原始封签文件未改 |
| output/research/four-directions/failure-focus.json | 7份失败焦点，各自patch／trace／双JUnit／依赖及原源码绑定 |
| output/research/minimal-policy | 全部60项原始执行、测试、依赖和成本，交接记录的证据引用指向这里 |

##### 分母与质量

60条是30道旧开发题各候选／对照一次，不是60道独立题，来自4个仓库，全部反复暴露。当前15条原生及独立测试阳性经源码审查后，13条支持有限修复，2条有明确需求缺口；另7条失败完成有限语义焦点，38条失败仍只做端点／错误盘点

13条源码支持也不等于13条可直接SFT的完整成功轨迹：部分修改过测试、留下临时脚本、重复提交、缺少最终响应或使用仅打印的检查。quality和training_use分开保存，所有sft_ready、rl_ready与train_targets_verified均为false。失败不自动标记每一步都错误，未审查的失败不伪造根因

原封签warning审核只扫描11处关键字category，漏掉openapi/utils.py和utils.py的2处位置参数调用。新AST审核找到13处，最终候选未修改后两文件，故从未定更正为明确缺口。原selection／closure／annotations保持原样，当前标签以quality-corrections覆盖；支持5对8和拒绝结论不变

##### 来源与去重

episode_id唯一绑定研究、条件、任务和seed。provenance绑定原trace、源码快照、实际配置与protocol；source_atif保留完整原始解析对象，gzip／JSON往返后与原对象逐条比较。它不声称保留了模型原始token或原始函数调用字符串

task_group将同题两个条件、所有步骤、探针、seed和补丁放在同组；repository_group供跨仓库隔离研究。所有30题只能标记development_exposed_not_evaluation，不能随机按步骤切出验证集，也不能将本批任何一半称独立验收

patch_dedup_group只对非空最终patch使用SHA；无patch按episode分别保留。当前2组非空patch各重复2次，保留全部执行和成本，不能借同patch另一条轨迹的JUnit。保留评估题重叠为0，没有读取保留题问题正文或gold字段

##### 训练输入与审核证据分开

source_atif中的系统／用户／Agent内容、tool_calls和observation是任务轨迹。函数调用与回应必须按原顺序、调用身份关联，工具输出只能作为上下文，不能误当assistant目标。ATIF里的call_id不保证就是模型原始线协议ID

quality中的人工观察、outcome中的独立验证结果、依赖回执、最终审核和failure-focus只供数据筛选与审计，禁止混进solver提示、用户任务或assistant目标。不能用独立verifier来给同一个Agent选择候选答案

代理message可能混有思考和最终回答，后台摘要／压缩不保证全在ATIF中；当前工具声明为GenAI对象导出，尚未证明与训练框架所需JSON schema或原始请求逐字一致。不要直接把此gzip当TRL可训练messages

##### 后续训练session应先完成的工作

先按manifest核对SHA与原始证据，选择有限源码支持且工作流符合要求的片段，单独记录选择理由，不把整条成功轨迹全部当正确动作

核对要训练的模型版本与量化／adapter兼容性，原31B compressed-tensors评分基座并不是已验证的训练底座。本包未下载或转换新权重

用实际tokenizer／chat template核对角色、工具schema、调用／回应及思考边界，验证assistant loss mask覆盖了哪些token，确保工具输出、人工审核和独立验证结果不参与错误的目标损失

按任务和仓库隔离训练与评估，保留暴露来源，不触碰封存题做调参；先做自造样本的模板与mask资格，再另行获得训练授权。RL需要真实环境、合法预算和可复现reward，已有离线trace不是已验证的RL训练环境

本包只完成研究交接、质量及结构核对，未训练、未验证adapter、未证明训练会提分
