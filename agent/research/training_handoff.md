##### 下一阶段做什么

固定已评分0.17 Harness，优先补全模型在真实仓库中的定位、编辑、错误恢复与验证轨迹，再比较base与训练后模型
现有数据完成了研究交接，尚未达到SFT／RL直接训练条件；没有已验证adapter或训练收益
Harness结果与公开实现比较统一见[研究结论](harness_closeout.md)，环境资格见[执行审计](execution_alignment.md)

##### Bad case与数据选择

最近诊断覆盖19个差异配对、38侧轨迹、7道不同issue，候选独有4个配对、失分15个配对
其中12个失分配对集中在前三道题，不是19种独立失败，也不是0.17所有失败的频率估计

| 题目 | 配对数 | 实际观察 | 优先补的数据 |
| --- | ---: | --- | --- |
| rich_4077 | 4 | 首次实现就把isatty代理到console状态，控制代理到底层file；候选四次在5分钟前结束 | API契约、代理对象语义、能否从可见需求得出结论 |
| fastapi_9425 | 4 | 候选24次动作耗在导航，完整序列没有实现写入；控制处理字符串None | issue→符号→调用者→首次有效编辑，高信息量检索与停止导航 |
| fastapi_14430 | 4 | 候选改序列判断层，遗漏v2序列化的UnionType入口 | typing与版本分支的实际消费路径，修改正确层次 |
| rich_3676 | 1 | notes字段、存储和renderer未完整接通，末次自测被预算拒绝 | 跨模块功能接入、渲染与真实需求覆盖 |
| fastapi_5077 | 2 | 一次连续十次write_file缺filepath后只留repro；另一次真实跨模块断言红→修复→绿并最终保留 | 参数错误反馈后的下一步纠正；包装函数参数与返回注解一起修复 |
| fastapi_5624 | 2 | 候选修复兄弟Security scope污染并保留，控制超时仅留repro | 状态隔离与高效完整修复，保留同批失败成本 |
| requests_7433 | 2 | 一次两侧整份patch相同而原生结果不同；另一次实现相同但候选另留scratch | 验证噪声、额外文件与模型能力差异分别标注 |

既有HTTPX3672还暴露了修改parser却遗漏pool调用者的问题，可作为跨模块传播数据的补充来源，不混入上述19配对的分母

38侧中30侧有实现补丁、4侧仅scratch、4侧最终空补丁
30侧最终实现与可重建的最后一次原生直接编辑一致，没有验证到“完整修好后又改坏”的合格回退机会，未达到至少两道不同题的机制准入门槛
重建依赖自身最终diff、原始Python快照与实际观察到的edit／write内容；任意shell副作用、后来删除的文件和未执行中间态不作完整保证

##### 标注边界

- FastAPI5077某重复step7–16的write_file只有content，filepath片段落在content末尾，反馈明确提示缺必填字段；这证明解析后调用错误，缺原始token时不能唯一归责模型或parser
- Rich4077可见issue只有简短代理要求与离线链接，输入信息缺口单列，不向评测题补入外部答案
- Rich3676补丁引用但未定义traceback.notes，是源码风险；轨迹未执行末次渲染，不声称观察到MissingStyle
- 一个故意未捕获的复现异常可能在输出正确渲染后退出1，不能把所有非零退出认作退化
- 自测打印Success可能在未修复原版也通过，真实断言必须校准原版失败、修复后通过，并覆盖公开API与回归路径

完整诊断在Linux的output/research/trajectory-diagnosis/{case-ledger.json,manual-review.json,completion-audit.json}
case-ledger保留采集时pending，最终人工覆盖层以manual-review为准
next-validation-protocol.json是未准入的设计稿，不能据其启动模型

##### 已有轨迹包

| 路径 | 内容 |
| --- | --- |
| output/research/four-directions/trajectories.jsonl.gz | 60条解析后ATIF、自生成最终补丁、配置、来源及质量标签 |
| output/research/four-directions/trajectory-manifest.json | 数量、分组、去重、范围与包文件SHA |
| output/research/four-directions/tool-schemas.json | 安装版六工具声明，非逐请求捕获的OpenAI／vLLM线格式 |
| output/research/four-directions/quality-corrections.json | 一处人工审核更正与源码证据，不改原封签 |
| output/research/four-directions/failure-focus.json | 7份失败焦点的patch／trace／双JUnit／依赖与原源码绑定 |
| output/research/minimal-policy | 上述包对应的60项原始执行、测试、依赖与完整成本 |

60条来自30道旧开发题的候选／对照，覆盖4个仓库，全部已暴露
15条原生及独立测试阳性中，13条支持有限修复，2条有明确需求缺口；7条失败完成有限语义焦点，其余38条失败只有端点／错误盘点
13条支持不等于13条完整SFT成功轨迹，部分存在修改测试、临时脚本、重复提交、缺最终响应或仅打印检查
quality与training_use分开，现有sft_ready、rl_ready、train_targets_verified全部为false

warning更正来自旧审核漏掉两处位置参数调用，AST复核从11处补到13处，最终候选遗漏对应文件
旧selection／closure／annotations保持原样，当前标签由quality-corrections覆盖，支持5对8及拒绝结论不变

这60条包与上述19配对不是同一批样本，不能直接合并为独立训练集

##### 数据身份、去重与转换

episode_id绑定研究、条件、任务与seed；provenance绑定原trace、源码快照、实际配置与protocol
source_atif保留完整解析对象，已做gzip／JSON往返比较，不声称保留模型原始token或原始调用字符串

task_group将同题全部条件、步骤、探针、seed与补丁放在同组，repository_group支持跨仓库隔离
当前30题只能标记development_exposed_not_evaluation，不按步骤随机切出验证集
patch_dedup_group只对非空最终patch使用SHA，无patch逐episode保留；已有两组非空patch各重复两次，执行与成本均保留，不能借另一条轨迹的JUnit

函数调用和回应按顺序、调用身份关联；ATIF的call_id不保证是原始线协议ID
系统／用户／Agent内容、tool_calls与observation是轨迹；工具输出作上下文，不当assistant训练目标
quality人工观察、outcome独立验证、依赖回执和failure-focus用于筛选及审计，不注入solver提示或目标回答
不能用独立verifier为同一个Agent挑选候选答案

代理message可能混有思考和最终回答，后台摘要／压缩不保证全在ATIF中
工具声明尚未证明与训练框架所需JSON schema或逐请求格式一致，不能直接把gzip当作TRL训练messages

##### SFT与RL的进入条件

SFT优先选择审核通过且工作流合规的定位→编辑→真实验证片段，单独记录选择理由，不把整条成功轨迹的每一步都当正确动作
负轨迹可用于错误恢复或偏好比较，但未审查失败不伪造根因，也不直接作为成功示范

RL奖励以可信环境中的最终补丁行为为核心，结合原生测试、独立副本、需求覆盖和回归
自写测试绿、退出0、无参数错误、patch非空不能单独作修复奖励；保留空patch、超时、依赖失败、skip、验证不一致与全部成本
公开训练仓库与隐藏测试仓库不同，既有115/129暴露清单只是历史盘点，未重扫后续记录；12题保留与2题同提交排除记录不构成今天未见集认证

进入训练前完成三个检查
1. 核验训练checkpoint与比赛CT部署侧adapter兼容，保存、重载后在精确部署链中实际改变输出
2. 用实际tokenizer／chat template核对角色、工具调用、思考边界与assistant loss mask，先用自造样本做转换资格
3. 固定0.17 Harness、共同预算、分组划分与可信行为奖励，先做小规模base对adapter比较

compressed-tensors评分基座不是已验证训练底座，离线trace不是已验证RL交互环境
模型、数据量与资源由用户后续决定，本轮不启动训练
