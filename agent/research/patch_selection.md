##### 自动隔离双草稿：完整结案，不采用

isolated-proposals已完整60/60结案封签，不采用：旧30熟题×自动隔离双草稿／精确0.17，严格阳性0/30对9/30，9份阳性全部按自身源码／patch／trace／双JUnit及三sandbox依赖审核，27个阳性sandbox身份互异。源码支持0/30对7/30，对照另1份uncertain计上界8、1份HTTPX需求缺口排除；原生／完整wall含全部失败成本增加4.55%／4.21%，原执行／配置／seed／预算及预定覆盖门禁有效。候选30份最终patch全空，selector已记录工具调用和轨迹步骤均0；17份仅有草稿写入／编辑回执（含临时探针），不得计为最终修复。原21份会话超时、9份TaskGroup错误、缺失原生JUnit及全部成本保留；机制链0。selection SHA256=8410635d53e1749ba13a04809159dc34f56772a3e6c84d01fb6205bb51353e2f，closure SHA256=fd7d09125b0393affb7d8550397cf6ff9e272bbef8e43555ba03d89524930210。自有owner／CLI／三API退出，终态四卡各1MiB／0%，未见匹配自有任务cwd的残留进程，冻结输入和模型元数据未变。正式请求0、0.17包保留、0.24尚未达到；不重跑封签collector／notes／report／seal／finalize，不补跑／换seed／用余12题救回。当前无新的模型计划或可提交候选，后续先做不同机制的失败证据及既有负结果去重。

本批源为output/research/isolated-proposals/sampling-candidate/agent-config，10文件；ZIP9137字节、SHA256=5a4ad4982596cb16227d4ad4f18270cde811ed66bfe29e1298e79365ab7e0e54，freeze SHA256=395ded93fd840de97039c79a7ca1cfcb021d62e84bf60d5f631a93c37dbe589e。它是共享五分钟／24动作／40轮下的普通源码双副本、角色、工具及选择联合干预；不是纯并行消融、独立随机采样或CodeMonkeys成绩复现。所有案例保持seed20261022及31B CT无adapter，GPU0/1/2同题同卡、每卡先后各5/5，只启动一次；熟题不是独立验收。

| 指标 | 隔离双草稿候选 | 精确0.17对照 |
| --- | --- | --- |
| 严格双验证阳性 | 0/30 | 9/30 |
| 源码支持 | 0/30 | 7/30，另1份uncertain计上界8 |
| 最终空patch | 30/30 | 5/30 |
| 原生任务总秒，含原生验证 | 8625.51 | 8250.13 |
| 完整case wall总秒，含独立复核 | 9100.86 | 8733.51 |

HTTPX对照自己的双24过仍漏_pool.complete真实调用及退出时关闭active streams，排除源码支持；Requests6644的path_url修复覆盖HTTP路径及重定向，但扩大到non-HTTP/custom-scheme属性的契约边界未验证，保守uncertain，不宣称已证明回归。其余七份有限支持均绑定自己的原源码、实际补丁、完整轨迹和双方JUnit，不借历史同名修复或另一侧验证。原matching_junit_identities与既定允许范围以selection.raw_pair_coverage为准；门禁有效不等于所有原始JUnit逐字相同。

全部60端点与失败成本在failure-analysis.json；source-annotations.complete=true、source-review完整60审核且无漏审阳性。候选已记录selector步骤／工具均0，17份有绑定的草稿编辑／写入回执，其中可包括探针脚本，不能当17份正确修复。Requests7433的B草稿曾写入公开要求的条件，完整文件SHA与自身原始源码精确替换一致，但最终canonical仍空；这是一个特定时点的草稿证据，不是最终修复或“被丢失的已验证成功”。A的read属性打印探针没有检验流式头／分类；不使用其exit0认定通过。9份TaskGroup错误的根因未穷尽，完整失败语义审核仍为部分，不把所有错误归给同一个阶段预算问题。

CPU／核心环境资格、原include_contents短历史失败、初始子进程残留／后处理错误、fork基线／副本导入／链接及实际seed修正均保留。后置16反例事件绑定、15项准确文件回放及14规则／7终态／11人审门禁资格只证明有限审核路径；没有新增模型／pytest／verifier重跑。读取负例源码的诊断曾误认_encode_params只有一个定义，原错误与重载修正回执独立保存，未改变模型结果或门槛。

封签seal／finalize均返回0；研究ZIP不采用、不正式提交、不替换0.17或正式配置。所有已记录自有进程身份退出，terminal-resources.json保存终态资源样本；不修改训练作业、权重、官方输入／测试或SDK。旧ref57681438仍以原正式回执及下一次到点认证核查为准，本批没有查询／重发它；例行官方检查不早于2026-10-27T11:57:39.350897UTC。没有官方逐题日志，也未达到我方有效公榜0.24目标。

本实现结案后不重跑collect_review.py、record_notes.py、report、audit.py seal／finalize，不补跑或换题／seed／门槛救回；不把另一种近义软交接重新登记为新机制。后续须先查实际失败、已有负结果和真实可提交边界，有实质不同且可验证的机制再写独立模型前计划。没有合格新包就不提交。

下文旧CPU快照及已封签模型结论保留其当时范围，不是新的待执行清单。

##### 当前接续：自动双副本尚未模型验证

新isolated-proposals已从设计推进到限定CPU执行路径审核，采用现有原生自动流程与普通源码副本。当前正确源为cleanup-check/agent-config，19项组件／5种脚本流程及13份sandbox身份核对通过；尚缺core task-profile依赖接线与模型前冻结，真实模型／GPU／正式请求均0。已发现并修正短历史压缩配对及子进程deadline两处原型问题，原失败保留；详见[控制流](control_flow.md)和cpu-runtime-review.json。下文旧paired-trial全30未使用选择Skill的负结果保持，不把新CPU夹具当模型选择收益。

##### 隔离双补丁选择：完整负结果

output/research/paired-trial 的固定旧30熟题×候选／精确0.17共60项已完整结案，不采用或提交。十五份严格阳性全部统一源码审核封签，原执行与预定覆盖门禁通过，但源码支持5/30对6/30，对照另1份uncertain计上界7，两类完整成本增加4.02%／3.79%，有效选择链0。保留已评分0.17，不计提分点；这不是独立验收或CodeMonkeys性能复现

动机来自[CodeMonkeys固定实现](https://github.com/ScalingIntelligence/codemonkeys/tree/7c35e1a79f4ebe40f94e5d0052f4daa7681412a5)：候选覆盖率之外，还必须解决实际选中哪份补丁。本原型只研究同一检查对两份修复的反事实区分，不复现论文的大量独立采样、测试投票、训练或性能，也不假定共享工作区的ParallelAgent提供仓库隔离

##### 执行机制与边界

paired-trial Skill只接收两个具名编辑列表的Python字面量字符串及一段短Python断言检查，不生成候选，不读取隐藏verifier或gold，不调用第二个模型。两个候选可能来自同一上下文，不能称独立采样或投票证据

从同一个当前工作树取得Git已追踪及未忽略文件，在任何检查开始前分别建立original／first／second三个临时副本；不复制.git、venv及缓存，拒绝外部或绝对符号链接。候选编辑沿用literal-batch已资格的精确锚点与最终Python语法预检，不将旧编辑器重复登记为新机制。该旧模型研究的负结果仍有效

原始副本必须导入自身项目实现并真实抛AssertionError，导入错误、无项目模块、原始已通过或检查改写副本源码均不作为有效校准。两个候选使用完全相同的检查，只有一个通过时才在再次确认真实工作树未变后应用对应编辑列表；两个都通过、两个都失败、预检错误或超时均不应用。相同最终实现的两个列表不当作不同候选

子解释器使用-I并将副本src／根目录放到导入路径前面，回执记录实际副本内模块路径，避免直接继承外层PYTHONPATH把检查误跑到原工作树。每次检查默认5秒、最多三次，另有复制开销；超时终止自身检查进程组。不是完整依赖隔离、OS安全沙箱、任意进程树／父进程硬终止资格，也不保证每个传递导入均来自副本

正确的断言退出码仍可能检查了错误需求，import存在也可能与断言无关；相关性、两种真实修复假设、所有要求及最终实现保留须人审。脚本只对已观察检查做选择，不把绿测试、较短补丁或status标签当修复真值；不把一次Skill计费等同仅做一次逻辑检查或免费算力

##### 直接CPU组件证据

15项自造Git小仓库检查通过：唯一首选／次选、双通过拒绝、双失败拒绝、原始已通过拒绝、导入失败／无项目导入拒绝、语法错误不落盘、相同候选拒绝、检查改写副本拒绝、真实检查超时、两文件新helper、绝对链接拒绝、内部相对链接与CLI下诱饵PYTHONPATH隔离。临时夹具清理，不使用官方题目或参考修复

组件回执component-check.json SHA256=11376475d0b73a819e8dd87cee96b15b3e4a686981bf75ce9952dff6746187ca，工具SHA256=802ff8503621c8851eaf5de24a2903a0686f15477d4bfc0210671d9abb7cf583。回执的native_harness_qualified=false保留当时范围，不追改历史快照

##### 真实SDK接线，不是模型收益

native-qualification/receipt.json SHA256=1c0e5a96743e8a1195b13cc9eb7fd8c6d86b370d29435488bbd2df6128633bac。使用既有自造calculator夹具、typed脚本模型及官方Evaluator；复制精确0.17配置，仅注册新Skill，实际六原生加四Skill工具，8192输出／4096思考、零温与5分钟／24动作／40轮保持，未加入新的模型路由提示

正常分支：真实原实现断言失败，两个独立副本一个通过一个失败，工具仅应用正确单文件实现；随后实际工作区断言通过，原生／独立干净副本pytest各3过，状态计费1→2→3

歧义分支：同一正数检查不能区分带符号／取绝对值两种实现，两份均过，工具拒绝应用，实际工作区仍为原源码的断言通过。夹具随后刻意用原生编辑写入错误的绝对值实现，双方各3项1失败；这是预设负分支，不把原生后续错误算成工具选错。状态1→2→4

共享cap1分支：夹具先原生写入同一错误实现用尽1次动作，Skill被预算阻断，未执行试验／修正；双方各3项1失败，计费始终1。实际Skill把BudgetExceeded JSON放在stderr字符串内而非响应顶层；原审查器误认顶层字段，补核器又过度解码界面转义，均在新verifier前失败，源与日志保留。最终按实际字段正常解析一次，仅补缺失的第三份独立验证，未重跑任何已完成脚本模型分支或修改预期

九份sandbox ID均在start返回前持久化，全部互异；六份JUnit的classname／name／file及失败／无skip身份逐项匹配，原始任务／快照／SDK／核心／原骨架与原型输入hash保持。qualification original_driver_completed=false保留控制器失败事实，完整三分支后置核查complete=true；这些不是Gemma生成、32k真实上下文、完整期限或官方Docker等价证据

##### 实际路由、冻结与执行状态

candidate只在原0.17 CHECK前加PAIRED TRIALS及新Skill注册，六原生＋四Skill工具，31B CT无adapter、8192／4096、零温及5分钟／24动作／40轮／命令60秒不变；这是选择／路由／菜单联合干预。规定只在两个真正合理且可用公开契约区分的修复间试验一次，不制造坏候选或为强迫通过改预期，剩余60秒内不用；明确的小修复保留直接原生编辑

实际路由另完成一条原生正常闭环：编译后完整路由、十工具、预算、同一检查失败→唯一通过→实际实现保留与另一干净副本均核对，自己的双方JUnit各3过、三个sandbox互异。qualification/receipt.json SHA256=a2b78aeb1054e3cf2d2df847795232e21702bb364a29a92ab382db67c77044e1；原型负分支与工具文件未变，绑定原回执而不重跑。它仍是typed脚本，不是Gemma主动选择Skill的证据

55单元／16元数据／12选择公式和60项计划通过后模型前冻结，study-freeze.json SHA256=71233bec251ddb0f5e3a8584adbc24f5d2e6e753a3bc1c21ff23c4f141a9f23e；研究ZIP SHA256=940fc133982b752d7a033cad54c1fb2179a4e1705d21f2c67604e78f43ded8f9，未正式提交或覆盖原包。固定旧30熟题×候选／新鲜精确0.17共60项、seed20261022，GPU0／1／2端口8410—8412，每卡先后各5次，余12题不用

2026-10-25T20:30:18 UTC仅启动一次，owner1281625／1792960218.29、CLI1281626／1792960218.37按PID及创建时间确认存活。首次启动观察于20:36:16 UTC完成1/60，三个自有API均有真实startup／health200／推理POST200，startup-observation SHA256=904f7331a50064a6ed384b49d6d24359ec698d9c5fd3386f052f42c6ae7ecf48；这不是整题／整批结论或连续健康保证。瞬时GPU0／1／2各39510MiB、81%／86%／82%，第四卡1MiB／0%，不抢其他session资源，不重复启动或补跑，不在运行中改核心／SDK／输入／规则

只读trial_events索引已资格通过：以已有原生正常／歧义／预算三个分支核对唯一call／author／参数／check SHA／各自试验与最终编辑回执，拒绝30个合成错误绑定反例；另三个参数传输别名是合成解析检查，不冒充额外原生调用。event-index-qualification SHA256=d4d18d26167b896fe011fa3b77d702af4ddc106cd33ed69a55d40a9c675dbeb8，没有重跑模型或verifier，indexed不自动证明候选合理、检查相关或最终保留

##### 完整模型结果与判定

全部60项终态、CLI退出0、保护输入未变，自有owner／CLI／三个API均退出；15份严格阳性均按自身源码／patch／trace／双JUnit／干净副本、三个sandbox及依赖清单审核，annotations complete=true。原始matching_junit_identities=false保留，预定junit_identity_check_passed=true与metadata_and_coverage_gate=true，不说原始JUnit逐字相同

| 指标 | 候选 | 精确0.17对照 |
| --- | --- | --- |
| 严格双验证阳性 | 7/30 | 8/30 |
| 有限源码支持 | 5/30 | 6/30，另1份uncertain计上界7 |
| 原生任务总秒，含全部失败与原生验证 | 8829.14 | 8488.05 |
| 完整case wall之和，含独立复核 | 9310.60 | 8970.27 |
| 原始run_skill_script调用 | 0 | 0 |

候选原生／完整成本分别增加4.02%／3.79%，有效最终保留选择链0，质量、效率与机制门槛均失败。保守配对候选独有支持0、对照可能独有2，描述性p=1.0不预测公榜。development_selected=false、independent_acceptance=false、promotion_allowed=false，selection SHA256=8fd9b20e42f8bd4083723c0fcdea73215b91529c5372e62d78336829090fee12，不采用／提交／补跑

双方HTTPX窄测试阳性仍漏真实complete调用者与明确server要求，均排除；候选FastAPI9425的typed-annotation要求与对照Requests6644较宽路径归一化边界uncertain，后者保留在对照上界，不人为制造候选净增。Rich3067双方各自82过、Rich4077双方各自4过，原生自检／复制函数／只打印／真实失败状态与assert的区别逐份记录，相同语义或patch不借用对方JUnit。全组未执行新脚本，所以无法估计正确使用反事实选择后的收益；不能由这份联合干预的负结果宣称选择工具一般无效

Requests自己的双JUnit均339项／337过／原有两项skip与xfail，FastAPI14361各自2过、FastAPI9425各自1过，HTTPX各自24过；相同补丁也分别绑定自身JUnit，不借历史同名结果。scratch、吞异常、无post-edit检查、重复submit等轨迹限制单独保留，不能用编译、打印或脚本退出0代替需求行为断言

后置展示脚本inspect.py曾遮蔽标准库，collect在导入阶段失败；改名display_artifacts.py后同一collector成功更新19/60并确认冻结输入不变、旧阳性身份不变。没有修改原collector／核心／SDK、运行策略或规则，没有重启模型或补跑验证。该审核工具故障与运行中的模型结果分开记录

后置终态分析器analyze.py已通过8项readiness、12项冻结公式、现有正常原生CPU选择及24个错误绑定／原生歧义和cap拒绝、6项自身patch／双JUnit绑定资格。analysis-qualification SHA256=7007ee956ee50da0e8c6929dcd08f8ce573c46f9ac1d2ebd7872d4dd83b01a8c，新增模型／verifier／GPU／正式请求均0，未运行seal或finalize。它核对人审字段、选择对应的原始参数和回执、所有选中编辑在最终patch中的人工保留说明；不以字段齐全自动判真，也不把自造signed／unsigned夹具当成模型提出两种真实合理修复的证据

##### 完成失败的焦点审核，不是全量根因

failure-focus.json SHA256=78f5df7848064fe2b15447c89f29e108f7926a8e5e71630600e7591f42dc8638绑定三份自己的patch、原始源码、trace、双方JUnit、三sandbox依赖成功记录与实际原生异常，未跑新模型或verifier，full_failure_review_complete=false，成本与失败仍留在全部60项分母中

候选FastAPI15030只加流响应wrapper，自己的generator预先提供data格式，真实自检最终通过；原生与独立各一份收集错误，因最终项目未提供验证所需导出。对照同题有另一个wrapper，但缺另一个项目模块，双方亦各一份收集错误；trace七步完全相同的缺old_string调用后记录五分钟超时。公开需求只说新增SSE支持，不能据验证器透露的API给未来Agent补指定名称或预制修复，也不能把一次窄自检通过等同完整feature

候选Rich3676先用20次导航动作，再做三次原生编辑；最后保留源码外反斜线引号，双方各一份SyntaxError收集错误。原生edit status=ok不证明语法；超时前未观察到修改后编译／行为检查或submit。notes类型和显示还可能有其他问题，但当前未进入可执行功能检查，不冒称全部语义根因已确认

这三份均零paired-trial尝试，不能当作新工具选错的证据；重复参数步骤也不等于计费动作。compact结果用error记录Agent超时，独立summary.error为空不代表Agent无超时；完整SDK模型的error_message与compact schema分开读取。本轮初次只读概览字段误读已纠正，不改原始产物／规则或补跑

failure-analysis.json SHA256=aaf9b5e47ce683d98491752e4dcc57707a14481ebc9dbe95069c0eb55fc26fea已完整盘点60项端点、原生异常、空patch、调用重复和成本；候选session超时16对12，对照另1份turn超限；空patch6对3，参数错误步骤8对32，重复调用75对74。更少参数错误并未带来更多修复或更低总成本，步骤／重复计数不是计费动作，三份语义焦点不冒称全部失败根因

seal／finalize已成功，所有封签引用保持，不再运行record_notes／collector／report／seal／finalize，不使用余12题或换seed救回。无新正式请求，原0.17及正式目录未改。下一步先核查合法仓库指引的实际覆盖和信息价值，不直接启动新GPU或给同一编辑路由近义改名；Goal仍未达到。offline_network的OS namespace边界与本地非官方Docker等价限制继续保留

真实模型接纳依模型前plan.md：完整双方原执行、干净副本、自己的JUnit、配置／覆盖及全部严格阳性源码审查；支持下界≥对照含uncertain上界，且净增至少2份、含全部失败／空patch／超时的两类总成本比各≤1.10，或质量不降且两类比均≤0.80。另至少两份支持修复须有需求相关且语义不同的有效实现试验、同一检查原始真实AssertionError／唯一通过选择及最终实现保留；错误导入、坏语法、常量／无关断言、相同实现或只出场不凑链。熟题不是独立验收，不换题／seed／阈值救回，最后仍须正式新分数验证

##### 四方向Goal的本轮去重复核

2026-11-01复核当前源码和原始回执，局部至多双候选并非未实现的新方向：paired-trial/development/selection.json是实际结论位置，根目录没有同名selection。自动原生异常回调受当前官方compile入口限制，不能靠声明回调名启动；完整范围、源码SHA、CPU回执及不重跑裁决见[four_directions.md](four_directions.md)，原始证据output/research/four-directions/mechanism-screen.json。本轮新增模型／验证器／正式请求均0
