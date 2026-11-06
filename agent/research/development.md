##### 当前状态：五题旧开发诊断已完整审核，Goal继续

anchor-legacy-diagnostic已单次完成5/5原样0.17诊断并逐题审核自身源码、patch、轨迹及双JUnit：严格阳性1（Requests7315的方法级源码支持），但该轨迹曾在沙箱改测试，最终patch已过滤测试且三独立sandbox验证使用干净测试；合规问题保留。另4题分别为无实现编辑、弃用类别及打包需求不完整、多文件要求只做两处、超时无patch。依赖缺失／ANSI差异等归因边界单列，不救回或重评分。全部均为已暴露旧开发题，不是新候选对照、独立验收或提分证据。

含全部失败原生成本1319.71秒、case wall1388.66秒、并行owner含启动清理854.961540秒，各口径不可混用。5903份保护输入及权重元数据未变；owner／两个worker／两个API／collector均按PID创建时间确认退出，端口8670／8671无监听，14个已知sandbox目录均不存在，四卡终态各1MiB／0%。初版closure的sandbox计数0是路径提取未覆盖ID字段，已保存纠正补充，原记录未覆盖。conclusion SHA256=7511398a3f2526bed7fde058f87fa0d4a1346c9e371aa47bb6248df9c4136120；closure SHA256=03ffaf224e4c48792d93e4fa9366734a4fe9ff54becc5fee09cb16d570a449d2，须同时读取sandbox-closure-supplement.json。原始产物在output/research/anchor-legacy-diagnostic。

当前无新模型计划或Harness模型作业。下一步按真实失败做跨分类机制去重及公开一手核查；不重跑本诊断／封签分析器，不补题换seed，72道既有验收及余12封存题不用作调参。Windows为唯一Harness执行方，Goal active，0.24未达到、0.17回退包身份未变。旧探索ref57681438最近官方回执仍为2026-10-27T12:09:29UTC的PENDING，下次常规检查不早于2026-10-28T00:09:29.877702UTC；待评分不叠加、同包不重发。下方旧“当前／下一步”仅追溯，不据此重开研究。

##### 固定五题的真实暴露记录与本次停止结案

五题pytest-dev__pytest-10081、7324、7236、7432、10356在atomic-cross-repository早已完成10项真实模型对照（seed20261024、精确0.17与完整小片段候选），selection及源码审核均complete、不采用；参见[原完整结论](atomic_edits.md)和output/research/atomic-cross-repository/{freeze.json,selection.json}。问题投影及CPU资格回执中的model_requests=0只陈述各准备阶段，不能据此认定这些题后来没有跑模型。之前开发导航未连接该后续证据，接手核对又未跨分类去重，导致本次错误的“首次模型诊断”判断。

本次baseline-diagnostic改用seed20261022并有当前编译seed传播，但不是预先设计的seed实验，也不能据事后差异重定义为研究收益。发现历史后于2026-10-27T16:36:00UTC停止：10081、7324、7236完成原生及独立端点，7432中断，10356未启动，保持原五题计划不补跑。完整冻结SHA256=1548397b5ef21322507257f6b837be2682bc31680a2285eb77bcd5e77d2e4222仍原样、21557项输入检查保持；一次SIGINT精确送至本批owner，真实清理finally完成，owner／API／已知子进程按PID及创建时间均退出，10份实际sandbox全局身份互异且目录已清理、四卡各1MiB／0%。

三份完整端点中的唯一严格阳性10081已按自身原源码、patch、trace、干净应用与双JUnit审核：类级skip谓词使显式tearDown保持unset，有限源码支持该任务要求；两份JUnit各64通过及9个原有非required跳过，最终单文件补丁在三工作区源码hash一致。Agent会话仍超时，最后一次自检没有完整回执，不声称模型自行确认成功。7324失败焦点显示字面常量替代名称改变matcher语义；模型已读到并正确复述自身测试的真实失败，不能归因“错误信息没送达”。7236及中断题未完成全部语义审核，当前3／4／5均不被重新定义为独立样本或用于质量率／效率推断。

结案output/research/cross-repository-qualification/pytest-self/cohort/baseline-diagnostic/closure.json，SHA256=0742058c3912681934413efd11cddb78d99e1efc51d03faa0508735c1a95032f。whole owner creation→ended为1284.169214秒；原始1273.10秒owner计时以及完整case子总数分别保留，case内all_costs_included标记不能代表包含准备、启动和中断任务的整批成本；SDK total_tokens=0与trace实际token指标分开保留，不解释为零token。所有原始、部分、资格／日志误纳入冻结及人工计数纠正原件保留，没有新模型验证／正式请求、没有救回旧研究或改其封签结果。

下一步任何模型计划必须先核对跨分类机制及全部题ID／实际包身份历史，明确重用理由，不再从单个准备回执推断全局未暴露。当前无新模型计划或GPU任务；0.17回退保留，0.24未达到，Goal继续。

##### 最近21份失败的产物审核，不改变冻结端点

isolated-proposals精确0.17对照的21份严格非阳性现均完成公开需求、当前最终patch、已保存轨迹动作与自身测试日志的人工产物审查：11份含实现文件、5份只有根目录探针、5份最终空patch。此覆盖不等于21份完整源码语义／因果根因审核，后者仍false；只见打印／编译不计完整行为验证，缺参响应不归因原始模型或parser，保护文件导致的空提交不绕过。证据failure-semantics/post-isolated-artifact-review.json，SHA256=ec56d692385ba5d048038dec249f13648a5bf9b424446b96a784102e71c69ead。

Requests6589、Rich3296、Rich3130当前自身原生／独立完整节点状态一致，也均与旧辅助CPU诊断状态及五类环境字段匹配；但三份当前完整patch均没有逐字相同的旧诊断patch，不把相同测试签名／环境记录当作完整源码等价、借旧修复标签替当前补丁证明需求或全部回归。没有再跑CPU verifier、改skip、重评分或修改sealed selection；其有限修复价值与遗留失败保持分开。

本次另据已有effective-seed-finding.json和实际核心源码修正本地seed传播缺口，见[本地检查](../workflow/local_check.md)：旧执行器仅重写configs/*.yaml，可能漏掉inline；新入口在保留SDK限制下统一编译seed，六项新增回归、76全src／16元数据门禁与pyflakes通过。它改善后续对照可审核性，不是新的可提交Harness机制、独立验收或公榜提升；Gemma与正式请求0，保留0.17，继续寻找有自身证据且未重复的修复质量机制。

##### 当前失败与旧诊断的身份绑定，不追加执行

`output/research/failure-semantics/pairs.json`只读收集paired-trial中Requests6589与Rich3130的候选／对照共四份当前失败，SHA256=320034b732d859087cf41391ad4be58d5d2d8bd7c4982b665d3973895f7c7e7e；补丁、trace、原生／独立JUnit及原结果都核对自身hash。两组是按“小patch、无Agent异常却测试失败”有目的选择的诊断焦点，不是新验证集，不是四道独立题或完整失败语义审核

最初假设它们可代表尚未诊断的逻辑缺口，阅读既有分类后发现两个失败家族已经记录，因此停止重复原始／补丁CPU测试，改为只读对应。`inherited-bindings.json` SHA256=6f64e89fa7d30c065038cd446687b9efcb639ddfd5b5cf8d040005707077b014：四份自身原生与独立完整节点状态一致，也与相应旧补丁执行一致；requested_packages、official_dedup_wheels、任务profile名／hash及system_site_packages五类记录字段均匹配。依赖记录一致不是全部安装文件或官方环境逐字相同

Requests两侧当前各324个节点，只剩同一无效端口重定向失败，与旧辅助诊断的持续失败相符；Rich两侧当前各六节点、四过二败，遗留整体渲染及inline-code颜色断言。当前Requests对照与旧scripted-edit对照patch完全相同，当前两份Rich与旧test-context对照patch完全相同；Requests候选patch没有逐字相同的旧诊断，不借旧通过／源码判断替它证明语义完整，也不以相同失败签名替代自己的JUnit

这里只确认当前结果与既有诊断的对应关系，不计四个新根因、不把遗留失败全归为环境、不改写原始resolved或封签5/30对6/30结果。原snapshot／核心代码身份未在这一步重新资格，不冒称所有历史上下文等价；没有新增模型、verifier、GPU或正式请求，paired-trial selection hash不变。今后先检索既有分类及精确证据身份，再选择未覆盖的失败做语义审查，避免重复执行已诊断家族

##### 固定开发与独立验收

日常开发集已从10题扩为30题，独立验收集从6题扩为24题；清单分别为 development_set.json 与 confirmation_set.json。公开题的本地修复率用于筛选，不称为Kaggle分数或隐藏集准确率

严格全绿端点还可能漏记有限目标修复：最新Rich3130原始／当前对照／候选三份CPU干净副本各六个相同JUnit节点、pip均0，原五项失败在双方均变为两项，三项表格行为修好、无新增失败，遗留相同整体渲染及inline-code失败。结合此前Requests6589与Rich3296同类对照，不能把全套未绿都归于策略；也不能据此认定完全环境所致、改写冻结主结果或换算公榜。证据test-context/auxiliary/inherited-failure-review/review.json及test-context/failure-analysis.json；本批7对7不变，未动测试、skip、官方数据或计分器

当前另一次replication_set的24题也已完整使用，两个独立组均封存。最新组源码支持8/24对4/24、p=0.0625，未达预定晋级门槛；随后适度采样及12B替换两项旧30题完整比较均被拒绝，不重复独立题、不自动提交。完整结果与当前运行身份见文末

旧30题联合生成容量首次完整比较源码支持9/30对6/30，对照另1份不确定，两类总时间增加17.33%/16.22%，仅通过开发筛选。随后单次反向顺序稳定性60项也已完整结束：源码支持8/30对6/30，对照另1份不确定，但rich_4077的对照补丁关闭底层流，引起pytest重复错误记录，冻结覆盖门禁未过，因此未晋级、不进入新独立题、不抽更多seed。候选两类总时间增加18.49%/17.32%，完整审核与预算见generalization文末；两次仍是相同30题，不能合并成60道独立题

##### 首次冻结的分组与来源

| 仓库 | 日常开发 | 独立验收 |
| --- | --- | --- |
| FastAPI | 15 | 13 |
| Rich | 10 | 8 |
| Requests | 4 | 3 |
| HTTPX | 1 | 0 |
| 合计 | 30 | 24 |

30题保留原来已使用的10题，再从未进入既有计划或执行的公开任务中增抽20题；24题保留原六题，再增抽18题。唯一HTTPX公开题已经用于开发，不能冒称有该仓库的独立验收

选择只使用任务身份、仓库、base_commit与需求元数据，按固定SHA256种子分层无放回抽取，不看参考修复、验证测试、已有成绩、问题长度或外链来挑题。开发与验收不但任务ID不重叠，base_commit也不重叠；旧六题清单及hash未修改

选择程序与冻结回执为output/research/generalization/select_cohorts.py、selection.json，原十题清单另存original-development.json；旧实验内的cohort.json及原始结果不修改。开发含熟悉的十题，不能把30题宣传为全新随机验证集

##### 日常工作流

在/mnt/data/haoyang/workspace/gemma4-developer-agent，使用conda的agent环境

```bash
python src/evaluate_development.py prepare
python src/evaluate_development.py run --agent-dir output/research/generalization/candidates/staged-localization --control-dir output/research/official-scoring/baseline --reference-dir submission --environment-review output/research/generalization/input-check-with-dependencies/review.json --gpu 0,1,2,3 --port 8070 --output output/research/generalization/development
python src/evaluate_development.py report --output output/research/generalization/development
```

prepare只增量下载官方输入，不下载新模型、不运行Agent；正式配置与ZIP只读。run复制并冻结配置，各题/条件新建会话、源码与测试环境，调用官方Evaluator后再在另一干净副本独立验证，保存pytest与完整JUnit

四个GPU是四个独立TP1本地服务，不是四个协作子Agent；同题的所有条件分配给同一服务，条件顺序交替，三条件按六种顺序轮转。每个服务串行，异常后不重试模型或换题；根报告必须汇总全部分片，不能拿较快结束的分片冒充完整成绩

默认执行seed固定为20261020，零温seed不代表多份独立答案。完整筛选后才选一个候选，再以新seed复核稳定性；输入准备与无模型环境检查不算模型修复实验

##### 独立验收

候选及接受条件必须在首次运行24题前冻结，只比较一个选定候选和一个预先指定对照，命令使用 --manifest agent/research/confirmation_set.json 与 --control-dir，不使用 --reference-dir

候选至少净增加2个独立修复，单侧精确McNemar检验p不大于0.05，全部计划完成、配置/模型/seed有效、原生和独立验证一致、同题完整JUnit身份可比，才具有本地晋级资格。小幅单题增加或降低失败时间不直接晋级

在首次独立模型执行前固定质量判读：SDK指定测试阳性与源码/附加验证支持的修复分别报告，候选和对照使用同一审查标准。明确的新回归或主要需求缺口不计完整修复，分母仍是全部24题，原始评分产物不改。推荐还需质量支持的配对净增与显著性成立，不能靠窄测试的错误阳性跨过门槛；有实质不确定性时按候选未通过、对照可能通过作保守检查，不把未知偏向候选。原生/独立一致性门禁仍保留，不以这个附加检查替代

24题只能作为本轮首次独立验收，不能读其具体失败修复继续调参后仍称为未见数据；反复使用只算验证。正式提分还必须有官方成绩，局部通过与统计门槛都不能保证隐藏集一定上涨

##### 报告指标

主报告包含完整修复数/计划数、Wilson区间、按仓库修复数、候选独有修复/对照独有修复/净增、空补丁、Agent错误、原生任务时间、Trace时钟与记录token。原生task_seconds包含验证，不是纯推理时间；Trace token也不是完整HTTP账单

任意条件缺题、配置/模型/seed不一致、重复结果、原生/独立判定冲突或执行完整性失败时，不显示完整通过率或晋级资格。失败、空补丁和超时始终留在分母，不换题、不删困难题或放宽官方测试

--environment-review冻结模型运行前的干净环境审核。正常缺陷可能因题目要新增的API尚不存在而阻断测试收集；只对预审明确的源码缺失符号题，并且实际出现collection error，允许失败侧与修复侧JUnit身份不同，原因在报告中单列

两侧均独立失败、都有真实JUnit、模型前环境已审核且实际有collection error时，将测试身份变化单列为“双失败收集差异”，不再否决其他题的配对；两侧仍失败，不改分母、胜负或成本。任一侧修复、缺JUnit、没有预审或没有collection error时不适用该新例外，成功侧仍须完整指定测试与独立审核。此规则在独立24题首次运行前冻结，旧研究报告不覆盖，源码及正反例在method-review

指定测试通过还要与补丁质量分开报告。对已识别覆盖盲区，先在干净基线确认既有回归测试可执行，再复核原始模型补丁，比较同一测试身份下的新回归；同时检查需求契约及明显缺失的调用点。附加检查单列，不替换官方结果，不因补丁有问题而判分后替模型修补。存在已证实新回归或未解决契约遗漏的候选，不仅凭原测试通过数推荐进入正式提交

同时看质量与效率：修复数增加才讨论能力，只有相同或更高修复质量才讨论时间/token收益，另列总消耗与每个有效修复的摊销。零修复时该摊销不定义，不能写成成本优势

30题每题约3.33个百分点，24题每题约4.17个百分点，仍不足以估计隐藏私有仓库的精确表现。仓库重加权只是诊断，不能消除熟悉题、选择偏差和本地环境差异

##### 既有结果与当前失败

旧固定十题在10分钟/32calls/60turns、4096输出/1024思考下为3/10独立修复，执行完整性通过；缩紧到5分钟/24calls/40turns、2048输出并增加收尾提示后为0/10，9题为空补丁、9题有Agent error。原始结果保留development-baseline与runtime-budget/development

本轮官方新包已COMPLETE、publicScore=0.00且无错误字段；这与旧两次Notebook Timeout没有分数不同。旧正式baseline最高0.06仍是当前已知成绩锚点，不把本地3/10或原两道熟题的成功称为官方进步

扩大测试集解决筛选盲区，不自动修复Agent。当前研究方向和来源、候选与已知局限见[泛化与开源节流](generalization.md)

##### 首轮验收与后续保留题

首轮24题现已完成并封存：候选5份源码/指定测试支持产物，对照2份，单侧配对p=0.1875，预定身份门禁与试投门槛未通过，不推荐据此声称具备冲击0.14的可靠证据。该题组不再称为未见集，也不用于继续调整本轮提示；原始失败、验证、配置与完整成本均保留

在未查看新生成策略的开发结果前，只按任务身份、仓库和base_commit，从尚未使用的60题中另保留24题，清单为replication_set.json：FastAPI 13、Rich 10、Requests 1；任务及base_commit均不与历史使用重叠。Requests余量仅1题，无HTTPX，构成不同，不将两轮比例直接合并或外推隐藏集

这是一份探索性延续的预留题，不是对首轮失败的替换或通过证明。新生成策略须完成开发筛选，且质量支持数不低于参考、优于控制，并增加修复或在质量不降时将两类完整时间至少降低20%，才考虑冻结候选。该生成候选现已完整执行并被拒绝：源码支持6/30，低于参考已确认7/30，未使用预留题

混合编辑提示hybrid-edit-recovery也已完整执行并被拒绝：源码支持6/30、另1份不确定，参考8/30；其上界仍不及参考，原覆盖门禁也未通过，预留题未使用

职责分工focused-native-editor已完整执行并被拒绝：源码支持6/30、参考8/30，实际候选总时间更高；虽然参数错误降为0，但9题未进入编辑流程。该执行信号不能代替质量收益，预留题仍未使用

在读取预留24题任何环境资格或模型结果前，登记下一项direct-native-worker直接交接架构的选择条件：同一30题完整90项比较、所有配置/执行/原生独立判定及预定JUnit门禁通过，逐份同标准审核全部阳性；候选源码支持下界须不低于参考上界、严格高于原baseline，并且相对参考增加支持修复数，或在质量不降时将含失败的原生总时间与含独立审核的完整case总时间均降低至少20%。不确定产物候选按未支持、参考按可能支持处理；不把更快失败、个别分片、无参数错误或工作角色调用率直接当修复收益

直接交接组现已完整结束并被拒绝：源码支持候选6/30、参考6/30、原baseline 1/30；两类完整时间分别降低6.04%与5.73%，不满足质量增加或20%效率条件。实际调用工作角色30/30、参数错误减少，不计新增有效修复或预留验收通过

在任何预留题资格或模型执行前，登记reasoning-budget的下一项选择规则：只将六工具契约参考思考预算1024改为256，其他内容与任务预算完全相同，固定开发30题的两条件60项完整比较，seed=20261030。运行器control标签明确指契约参考，本组不重新执行原0.06 baseline，也不声称已有新同seed原baseline配对收益

必须满足全部配置/种子/原生独立判定及预定覆盖门禁、全部阳性同标准源码审核；候选支持下界不低于契约参考上界，并且增加支持修复数，或质量不降且含失败的原生总时间及含独立审核的完整case总时间都降低至少20%。不确定候选按未支持、参考按可能支持处理。减少开发对照条件只节约研究成本，不降低候选质量/效率门槛，也不修改直接交接或旧研究的拒绝结论

该60项现已完整结束，全部执行/覆盖门禁通过，源码支持候选8/30、契约参考7/30，候选独有1题、参考独有0题，p=0.5。候选因支持修复数增加而达开发选择条件，不是因为两类时间降低17.42%/16.53%满足20%门槛，也不是已证明统计提分；记录token增加19.48%、参数错误步数4→11的代价一并保留

在首次准备新输入前，已将单一候选与原0.06 baseline配置复制冻结，记录replication-freeze.json及原24题manifest hash，seed=20261031，后续只能执行这对配置的48项首次独立比较。对照保留原五工具、温度0.2、1024输出/256思考、8calls/20turns/10分钟；候选是六工具契约策略、温度0、2048输出/256思考、24calls/40turns/5分钟，因此独立比较针对完整策略包，不把所有差异归因于思考预算

上述为模型前登记的准备边界；该24题现已完整执行一次并封存，结果见末节。条件先后在全部24题中交替，但每卡首条件固定，不称为完全逐卡随机交叉；其影响和硬件/仓库构成局限与完整成本共同报告

只有符合开发选择条件，才冻结一次候选与现有预留清单，准备环境并首次运行该24题；若未达标则保留题组未用，不为该候选启动独立评测。预留24题仍与原0.06 baseline直接配对，接受条件仍为至少7份源码/选定验证支持产物、净增至少2题、单侧p≤0.025、原生/独立判定和预定覆盖门禁均有效；同时披露两轮结果、名义与双比较调整p值和多重探索局限，不宣称事先控制了整体5%误报率。首轮失败不改写，不能在看到本预留题结果后再调候选并称其独立复核

预留过程未下载新输入或运行模型；receipt中的model_started=false仅描述这份预留题在抽取时尚未运行，并不否认同时在开发30题上执行的generation-development。题目不是按难易、原答案或结果筛选，不反复抽题直至通过

##### 后续实验的坏源码收集身份规则

混合编辑组发现，模型自己引入语法/缩进错误会使失败侧JUnit只记录collection error，而成功侧仍执行完整测试。旧组的预定门禁不改，原report和执行时分析源码封存，不把该诊断追认为旧候选通过

后续组在模型启动前，可从既有干净环境审核的原JUnit提取并绑定完整测试身份与skip清单。仅当失败侧原生及独立判定均失败、收集错误逐份明确定位到实际补丁中的Python实现文件、错误为SyntaxError/IndentationError/TabError、且未改测试或验证文件，而成功侧完整测试身份等于事先冻结的干净JUnit、没有新增skip时，将其单列为已预审的坏源码收集差异。失败仍计失败，胜负/成本不改；缺依赖、没有源码证据、缺JUnit、减少测试、新增skip或未预审的研究仍不豁免

这是覆盖可比性的保守工程规则，不是Agent优化、修复正确性证明或降低评分标准；新原始统计与源码审核都应用相同规则。单元正反例覆盖同一失败保留、交换候选/对照、缺审核、缺覆盖、skip、依赖错误、验证冲突及测试改动

##### 独立模型执行前的环境修订

新24题无模型资格检查确认宿主包污染与声明依赖漏读后，候选、对照、题组、种子和接受门槛继续冻结，仅修正可选本地任务环境：不继承宿主site-packages，固定既有根依赖版本，补读Poetry与requirements-dev，并保留实际安装版本。不能强制所有宿主传递依赖，因为宿主SQLAlchemy与任务sqlmodel要求已发生真实冲突；只约束声明根包，由pip求兼容闭包，原失败探测保留

完整CPU资格同时检查全部24份干净源码及开发比较的全部60份既有产物，不只重验阳性，也不重跑模型；环境、源码、wheel缓存、原冻结文件和正式ZIP身份绑定在isolation-qualification-owner及method-amendment。旧开发和首轮验收不重算；新环境敏感性结果单列，不能把旧模型产物复验当作新环境下重新推理的成绩

本次在独立模型执行前另明确两种失败语义，原始resolved、error、JUnit和分母全部保留。原本已绿的题，只有事先记录已绿、零补丁、SDK明确预算错误、原生test_exit_code=-1而独立原源码审核通过时，视为原生未进入验证与清洁审核不直接可比，两边仍不计修复；非空补丁或一般执行异常不适用

原源码自身超时的题，另做只收集测试的诊断，保留完整身份和原有skip标记，不改动、删除或重排测试。超时仍失败；只有实际审核exit124且无JUnit的一侧，才可与另一侧事先收集身份完全相同、无新增skip的完整审核比较。缺少预审、缺少用例、额外skip、测试改动、一般异常或原生独立判定冲突仍不适用。该规则与正反例在新模型前冻结，53项单元测试及16项元数据检查通过，不追认旧报告或降低阳性标准

随后补齐旧setup.py的静态运行依赖声明读取，并整批复验全部24份原始任务及60份旧产物，不执行setup.py、不重跑模型。最终源码支持与完整覆盖仍为候选8/30、参考7/30，无新增skip或未审查阳性；55项脚本测试、16项元数据检查通过。初次漏依赖时的失败、旧源码与敏感性报告均保留，不用缺依赖结果评价补丁质量

该统一环境资格完成后，已一次性完成预定48项首次独立模型比较，入口launch_replication.py、运行身份independent-replication-owner.json，配置、种子、分母与原接受门槛不改。该次比较针对完整策略包对原0.06 baseline，不把运行器control标签与此前思考预算消融中的契约参考混淆

##### 当前独立验收结论与使用边界

48/48完成、四分片退出0、整组约63.7分钟；正式ZIP、输入、核心及环境身份不变。指定测试严格阳性候选11/24、对照5/24，候选独有6题、丢失0题，p=0.015625，预定执行/覆盖门禁通过。原始matching_junit_identities=false仍保留：实际可比性依赖模型前冻结的同名snapshot teardown与原源码超时两项元数据规则，而非所有原JUnit逐字相同

统一审核全部16份严格阳性后，源码与选定回归支持候选8/24、对照4/24；候选另2份明确需求缺口、1份不确定，对照另1份缺口。保守配对独有4题、丢失0题、p=0.0625，未达到事先p≤0.025的接受门槛。唯一不确定即使算支持，p=0.03125仍不足，因此不推荐替换正式包，不将11/24或8/24换算为官方0.14

原始结果见independent-replication/report.json，完整源码证据见source-review.json、辅助干净/补丁比较及quality-report.json，成本见budget-report.json。源码支持是完整任务需求和选定检查下的有限证据，不是全库证明；16份产物及原生/独立JUnit不改，不根据结果清理模型留下的脚本

候选原生总时间含全部失败约103.5分钟，对照56.4分钟，记录token约483万对189万，六份会话超时仍留在分母。每份质量支持产物原生摊销12.94对14.09分钟、含独立审核case摊销14.35对16.93分钟；不等同减少总算力或官方12小时预算已经满足

replication_set现已使用，不能继续按其具体失败调策略再称独立；首轮confirmation_set也继续封存。后续先回固定30题，以旧开发缺陷或公开机制提出新候选，完整配对与同标准源码/预算审核后才考虑剩余未用题。该独立组结束后GPU已退出，正式包和Kaggle提交未变

##### 当前开发：适度采样的单因素比较

moderate-sampling只将已选六工具策略temperature从0变为0.2，256思考及其余文件/工具/预算相同，对照就是temperature=0的reasoning-budget，不重新执行原0.06。假设来自独立组结果前已记录的旧30题连续同形失败与公开预算帖机制，不采用两组独立题的具体修复线索

固定原30题、seed20261101、60项一次性配对，单一候选与参考同任务同服务，条件顺序交替；不得拿部分结果比较。选择条件为全部门禁、统一源码审查下候选支持下界不低于参考上界，并增加修复数，或质量不降且两类含全部失败的完整时间均至少减少20%；该开发结果不冒充独立验收

隔离环境中30份原源码已全部资格审核，原生接口模拟、实际HTTP参数、55项脚本测试、16项元数据门禁、4项原有fixture缺陷资格测试及plan/report检查通过后，该60项真实GPU比较一次性完成，终态见moderate-sampling-development-owner.json及该研究目录selection.json。两个独立题组仍封存，正式配置和ZIP不变，无新Kaggle提交

两侧指定测试均7/30，14份阳性统一审核后源码支持均6/30；候选1份明确需求缺口、对照1份不确定，保守候选下界6低于参考上界7。原生总时间及含独立审核case总时间分别增加4.69%/4.31%，参数错误51对15，因此未通过预先冻结的质量/效率条件，明确拒绝，不换seed或补跑失败项

##### 当前下一项：原生策略的12B对31B完整比较

三个合成参数请求和真实12B服务启动仅证明兼容，不计任务修复。native-model-development在同一旧30题、seed20261102冻结60项配对，唯一配置差异为模型名，仍用六工具、零温、256思考、2048输出及五分钟预算；四张GPU两波交叉，每道题两个条件用同一物理卡，阶段与共享启动分别保存

环境使用上一轮已冻结且输入身份未变的隔离profile，预先规则仍是完整门禁、统一源码支持质量不降，并增加修复或两类完整时间均少至少20%。模型身份报告新增显式映射与冻结配置核对，旧31B默认限制不变，55项核心、16项元数据与5项新正反例通过；不改旧报告、不用独立题调参、不自动正式提交，实际进度见native-model-development-owner.json

该60项现已完整结束，八个分片均退出0、整组73.41分钟，165个独立环境实例与全部30对依赖版本审核一致。指定测试12B为5/30、31B为9/30，统一源码支持为4/30对7/30；两侧各1份共同不确定补丁，31B另1份明确需求缺口。候选两类完整时间增加6.83%/6.49%，参数错误虽降为0，但空补丁17对5，未满足原质量/效率门槛，selection.json明确拒绝

预定覆盖门禁通过不表示全部JUnit记录完全相同：fastapi_14605的原源码收集差异、fastapi_14455的既有snapshot teardown例外原样保留。原始结果、完整源码/成本与依赖/运行身份审核均保存，不把小模型格式兼容当提分，不因此消耗剩余未见题；正式包未变、GPU已退出

##### 用已有官方成绩回查本地筛选方向

2026-10-23北京时间00:15只读核对完整官方记录，精确原包ref57485865为COMPLETE／0.17，第一融合ref57506355为COMPLETE／0.13，错误字段均为空。两份ZIP逐文件对应同轮本地对照的冻结源码，未用作者分数或其他提交代替；详细身份回执为output/research/contract-budget/local-official-alignment.json

| 精确方案 | 我方官方公榜 | 同轮30题指定测试通过 | 全部阳性统一源码审核后支持 |
| --- | --- | --- | --- |
| 原六工具骨架 | 0.17 | 10 | 9 |
| 第一融合 | 0.13 | 4 | 3 |

源码支持修复中，融合保留3题、丢失6题、没有独有修复；本地拒绝融合的方向与后来官方下降一致。30题／60项完整、冻结执行与覆盖门禁通过，原始matching_junit_identities=false及事前已资格的收集例外保留，不能写成原始JUnit全部逐字相同。回查未重新运行模型、换题、改门槛或改旧报告

这只能支持“该轮本地筛选识别了这次明显退化”，不能据两个已选策略证明普遍排名可靠性或数值校准。9/30不能当官方0.30，3/30也不等于0.13；本地题反复暴露、仓库配额为FastAPI15／Rich10／Requests4／HTTPX1，隐藏私有仓库分布未知，A6000／TP1／Subprocess与官方L4／TP4／Docker也不等价。此前相同配置在不同轮次还有波动，单轮差一两题尤其不能直接认作提分

因此旧30题继续作配对淘汰与失败诊断，不按已见公榜重挑题或调权重，余12题仍未使用。公开原样包ref57542842于2026-10-23北京时间23:14:27核实COMPLETE／0.15／无错误，3713字节ZIP与原样SHA256身份不变，终态回执public-navigation-reproduction/scoring-latest.json。这是新增一个真实外部核对点，不是作者页面0.22；我方最高锚点仍0.17。其本地源码支持8/30，原先对照是0.13融合而非同轮精确0.17，且八分钟与五分钟预算不同，不能拼成三个同预算配对、拟合0.24分数预测器或冒称新的独立验证。没有官方逐题日志，不能靠总分确定错题互补或分差原因；当前issue-triage冻结60项也不因此换题、调权重或改规则

##### 精确原骨架的跨轮稳定性

只读复核四份已完整结束的30题对照，均逐文件匹配获公榜0.17的原包，并核实相同题集、seed20261022、模型、核心源码和记录的环境身份；全部旧门禁有效、阳性补丁与独立JUnit身份绑定不变。回执为output/research/generalization/anchor-repeatability.json，计算程序同目录audit_anchor_repeatability.py，无新模型、GPU或正式提交

| 对照所在的研究 | 指定测试通过 | 统一源码审核后支持 |
| --- | --- | --- |
| 精确接口融合 | 10/30 | 9/30 |
| 有界导航融合 | 10/30 | 9/30 |
| 完整片段编辑 | 7/30 | 5/30 |
| 单参数思考预算 | 7/30 | 7/30 |

这些是同一30题上的120份历史对照case，不是120道独立题。记录的配置和seed相同，修复支持数仍为5—9题；相邻候选、服务历史、条件顺序及运行负载可能不同，因此只能描述跨轮不稳定，不能从这四轮估计纯随机噪声分布或指定某个根因，也不能按结果放宽已经冻结的接受标准

本地集仍用于发现明显退化、工具失效与需求缺口；单轮净增一两题不能独立证明泛化提分。后续继续要求完整配对、统一源码审核、含失败成本和预先固定的跨题集验收，再与实际官方成绩交叉核对，不以单次熟题最高值挑选策略

##### 从平台下载反核已评分输入

2026-10-23北京时间06:01，因截图显示的文件大小与本地ZIP回执不同，使用官方DownloadSubmission只读获取我们自己的两个已评分输入，未发起提交或查询额度。0.17的ref57485865实际下载为2022字节，0.13的ref57506355为2495字节，二者均与本地冻结ZIP逐字节相同，四份文件也分别匹配对应研究的冻结配置源码

这两条记录的API total_bytes分别为90477和85734，不等于实际下载的输入ZIP长度。因此截图大小差异不能用来认定交错包；该平台字段的具体含义尚未核实，不猜测它是否指推理输出。下载字节比对给出了比描述或同名文件更直接的输入身份支持，但不新增模型、补丁、隐藏测试日志或提分证据

完整元数据、来源路径、字节数及身份在output/research/contract-budget/scored-input-download-audit.json。没有另存下载副本、检查隐藏任务内容或覆盖旧alignment报告；当前五工具研究的配置、选择规则和原始结果保持冻结

##### 公开环境讨论对本地集的进一步限制

2026-10-23重新检索同比赛[公开任务验证环境讨论](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/747248)，工作人员Ryan Holbrook明确回复：公开训练任务中的仓库不出现在隐藏测试中，并表示隐藏测试经其参考提交可全部验证通过。这是工作人员的范围说明，不是我们取得了隐藏测试日志或参考修复；没有下载／查看该帖子所链接社区Notebook的参考答案

因此当前四仓库本地集不只是隐藏题目未知，而是仓库域本身不重合。已观察到的0.17对0.13方向一致仅证明一次明显退化被识别，不能证明单轮净增两题会泛化，也不能用重复熟题估计0.24公榜。余12题即使保持未用，也仍来自相同公开仓库，不是跨仓库验收；不因这条新说明在正在运行的60项中换题、改权重或改晋级规则

同帖社区还报告公开依赖缺项与site-packages里的发行版遮蔽工作副本，导致依赖错误阴性或空补丁假阳性；这是其公开环境复现结果，不直接当成本轮故障。我们当前local_sandbox.py已有每任务依赖安装与/workspace/src、/workspace优先导入，原源码环境资格及干净副本JUnit另有冻结记录，但仍非官方Docker等价证明。后续保持核对源码导入来源、依赖、空补丁基线与全部测试身份，不为提高通过率改官方测试或计分器

另查到的[思考历史字段讨论](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/744354)不是新策略证据：既有本地字段／模板审计已在context_and_tools.md记录。当前只读源码核对仍显示vLLM0.19.1读取reasoning字段，本次没有重新抓取当前推理请求，不能仅凭版本号或旧字段负例就认定思考丢失，更不为此修改运行中的SDK／服务。公开搜索未找到本次新增且已核对固定源码与得分关联的更高方案，不据标题0.24启动新的重复实验
##### 原有失败与全绿端点的局限

2026-10-23对scripted-edit的Requests字符串字节长度与Rich语法padding两题另做六项CPU三侧复核：原代码／精确0.17补丁／脚本候选补丁使用相同冻结profile、独立干净副本、相同测试节点与skip。两侧补丁均把各自目标失败变成通过，无原先通过项转失败，但分别保留原代码已有的1项重定向失败与8项语法高亮快照失败。证据output/research/scripted-edit/auxiliary/inherited-failure-review/review.json；原始严格主结果及选择不重算，双方同获这两项局部改善不构成候选优势

因此环境就绪、pytest执行成功和测试节点覆盖一致仍不足以证明全绿端点完全反映修复能力；还需保留原代码对照与逐节点转移。不能为追求更高本地比例删失败、加skip、换依赖直到变绿或倒改预定计分器；后续实验仍报告冻结严格端点，任何新增辅助端点须在模型结果前固定、同标准覆盖双方，并明确不能换算隐藏公榜

##### 零温与相同seed不是在线服务的复现保证

当前安装vLLM0.19.1的[官方可复现性说明](https://docs.vllm.ai/en/v0.19.1/usage/reproducibility/)明确默认优先性能、不保证复现；离线模式可约束进程调度或使用batch invariance，在线Server模式则要求batch invariance。该保证即使开启也局限同硬件、同vLLM版本，不能把零温与相同seed当作A6000／TP1与官方另一硬件／TP配置输出必然一致的证明

该版本[batch invariance说明](https://docs.vllm.ai/en/v0.19.1/features/batch_invariance/)仍标记beta，要求NVIDIA计算能力至少9.0。只读查询确认本机四张RTX A6000均为8.6；当前三服务实际进程未设置VLLM_BATCH_INVARIANT，也未显式设置VLLM_ENABLE_V1_MULTIPROCESSING。不能把文档中的开关直接套到本机，更不能将仅适用于离线调度的设置冒充在线服务的确定性修复

这些官方边界与实际硬件状态为已有跨轮波动提供一种可能的机制背景，不是本批误差归因、噪声分布估计或新增提分点；尚未做实际batch大小／调度因果实验。当前48项的服务、SDK、seed、题、选择规则不改，不重跑挑结果。继续预先固定配对顺序、保留全部失败和成本、逐份审核源码与JUnit，并以实际官方有效成绩核实泛化；证据output/research/generalization/reproducibility-source-review.json，无新增模型调用或GPU作业

##### 跨仓库验证来源：仅完成第一步可行性检查

2026-10-24只读检查SWE-bench Verified发布方页面，其公开元数据显示500条、12个仓库，存在issue／base_commit与验证字段；尚未核实许可证、固定数据revision、投影下载元数据或选题，不能称已经补齐新的可靠验证集，也不假设它与Kaggle隐藏仓库同分布

[发布方评估指南](https://www.swebench.com/SWE-bench/guides/evaluation/)采用Docker隔离执行。[环境指南](https://www.swebench.com/SWE-bench/guides/docker_setup/)另列依赖与磁盘要求；当前只读查询确认haoyang仍无Docker socket访问权限，测试PATH也未发现Podman／Apptainer／Singularity。没有改组、提权、启动／拉取镜像或使用付费远端；沿用现有Subprocess可以做单独资格化的本地辅助检查，但不能把它改称发布方容器基准复现

本次服务器直接读取数据卡的单次HTTPS请求返回Network is unreachable，只证明该直连路径失败，不据此认定所有代理、Kaggle或SSH均不可用。SSH正常，既有本地Harness并未因此停止；不以此重启旧模型实验或要求用户重新处理已经拒绝的Docker权限

数据查看器在元数据页自动展示了前两条patch／test_patch预览，因此astropy__astropy-12907与astropy__astropy-13033记录为已暴露，后续不得列入未见验收候选。未复制预览到项目或喂给Agent、未据其设计策略；后续只取数据卡与许可字段投影，避免再次打开带答案的行视图

回执output/research/generalization/cross-repository-feasibility.json。当前新选任务、数据行下载、模型请求、GPU作业与正式提交均为零，旧30／已暴露24及余12题保持原状。下一步仍是有界的来源许可证／revision／无gold元数据核查，再决定环境资格，不跳过这一层直接声称本地比例能预测0.24

##### 跨仓库身份盘点与原生接口核查

后续已固定Verified数据revision为c104f840cc67f8b6eec6f759ebc8b2693d585d4a，核对发布方LFS的完整压缩文件SHA256，再通过可达的Mac网络路线在内存中传到Linux既有PyArrow。只投影repo、instance_id、base_commit、created_at、version、environment_setup_commit六列，没有解码patch、test_patch、hints、问题描述、测试列表或difficulty，也未保存原始Parquet；这不是继续打开答案行视图或迁回Mac开发

完整身份记录500条、12仓库；排除与官方公开仓库重复的8条Requests，再排除前次页面自动暴露的两条Astropy，剩余11仓库490条身份、489个不同repo／base_commit组合。后续分组还需避免同一repo／commit跨筛选和验收，不能把490条都当独立源码环境、已就绪任务或模型未见样本

| 仓库 | 身份池数量 |
| --- | --- |
| django/django | 231 |
| sympy/sympy | 75 |
| sphinx-doc/sphinx | 44 |
| matplotlib/matplotlib | 34 |
| scikit-learn/scikit-learn | 32 |
| pydata/xarray | 22 |
| astropy/astropy | 20 |
| pytest-dev/pytest | 19 |
| pylint-dev/pylint | 10 |
| mwaskom/seaborn | 2 |
| pallets/flask | 1 |

许可边界：发布方SWE-bench代码仓库README及License API明确MIT；但本次固定的Verified数据卡没有单独license项，不能据此宣称所有数据与各原仓库源码都已核实统一MIT。后续保留各来源许可，不将身份盘点变成重新发布数据集

只读SDK核查显示Task有相应身份／需求／验证字段，但原生verify_task实际对验证文件运行pytest；这不自动兼容其他仓库的专用runner、历史Python／依赖和完整回归判定。上游[FAQ](https://www.swebench.com/SWE-bench/faq/#can-i-run-evaluations-without-using-docker)明确其一致性评测需要Docker，目前该权限仍不可用；现有Subprocess不是上游SWE-bench容器基准的等价替代

因此本步没有选资格题／新验收题、创建Agent候选、调用模型、启动GPU或正式提交。下一步先设计有界CPU原生适配资格：仅用明确不进入未见验收的资格样题检查干净副本、历史依赖、原始失败与JUnit身份；如果无法保证任务和验证含义，不进入GPU或产生可与既有结果混合的通过率。测试／计分器及官方data不改，余12题不动

证据output/research/generalization/cross-repository-metadata.json与cross-repository-source-review.json，以及投影脚本project_cross_repository_metadata.py；元数据SHA256为cfd24676c4b1faad9cecb3d585715ed5d573502413133f2dadf4d92c8293deb9。真实官方锚点仍0.17，新增身份池不能用来宣称0.24已更有保证

##### 两题CPU资格预检：当前环境不通过

在读取验证规格、源码或执行结果之前，以固定身份seed在明确选择的SymPy／Sphinx两个纯Python仓库内各取SHA256排名第一题，冻结sympy__sympy-14531与sphinx-doc__sphinx-9367。它们是目的性适配资格题，不是全池代表性随机样本；此后排除于未见验收，原490条身份池还剩488条／487个repo-commit组合，仍不意味着这些身份已有可用环境

本次只为冻结两题的CPU验证取得test_patch与指定测试列表，Parquet库先投影这些验证列，再按已冻结ID过滤并仅保留两题；没有解码参考patch、hints或问题描述，Task的patch／hints_text／problem_statement均为空，没有Agent或模型。GitHub固定commit源码归档只去掉顶层目录前缀，原文件数据与许可保留，官方data与测试／计分器没有改动

预定初始四次原生verify_task已全部执行，两题各两个不同干净工作区。均为pytest退出4、测试收集前失败、无可用JUnit测试身份，因此没有观察到预期的目标缺陷断言，不能写成模型修复率0/2，也不能把空JUnit相等当测试覆盖一致

| 资格题 | 当前环境实证 | 判定 |
| --- | --- | --- |
| SymPy | 实际从任务checkout导入旧代码，在collections.Mapping处ImportError；现有运行时Python3.12 | 尚未到达题目缺陷测试，运行时不合格 |
| Sphinx | 任务tests/conftest.py导入docutils时ModuleNotFoundError | 当前依赖环境不合格，不能归因于Agent |

初始四次还出现原生基线git commit退出128，因为GitHub归档没有.git。另行在两次追加CPU诊断前固定仅增加临时工作区空Git初始化和非敏感本地提交身份，保留原输入与测试不变，两次原生基线提交均退出0，说明该输入适配办法有效；两题仍分别停在上述相同导入错误。该办法只在研究适配诊断中验证，没有偷偷修改核心执行器或把新调用替换原四次失败；源文件入口hash与固定snapshot一致，不冒称完整运行后全仓逐字审计

合计六次原生验证、六个不同且已清理的临时工作区，不是六道题或六次模型实验。初始四次原生累计9.87秒，Git适配追加两次6.17秒，均含验证／环境步骤，不是GPU推理时间或完整数据准备成本。没有安装依赖、降级全局包、改stdlib兼容代码、增加skip、换题或修改门槛；两个原始环境问题没有被解决，qualification_ready=false，model_repair_rate=null

完整审核见output/research/cross-repository-qualification/review.json，SHA256为887ef39d5e8403e61b855f67c59e9db8e81449e7ba13eb7e5e33dd6c1bdefe75；原始四次与追加Git诊断分开保留。审计器首次误读序列化字段error，核实实际为error_message后只修分析器，没有重跑验证或改原结果，过程在analysis-preflight-error.json。全部六份实际error_message为空也不能说明环境正常，必须结合退出码和真实stderr判读

pyflakes、55项现有单元和16项元数据检查通过，但不是模型修复证据。没有真实模型／GPU／正式请求，0.17配置、SDK、核心和官方输入保护hash不变。当前两题不进入GPU；若将来补历史运行时与声明依赖，需要另作明确隔离环境资格，而不是给Agent修测试环境或抽新的容易题救回本次结果

来源盘点不等于扩大验证已经完成；原生数据字段可对齐也不等于历史仓库在当前Python下可执行。本步只证明当前直接适配不成立，不推断全部490条都不可用、Docker是唯一研究路线或Harness不能继续改进。后续先核查可提交的自动编辑后诊断反馈机制，仍只在既有合格环境内做CPU组件验证，正式采纳需另行冻结配对而不能借旧熟题正差值背书

##### 历史运行时准备：隔离解释器已就绪，任务资格尚未通过

对同两份固定资格题只读核查原仓库setup／tox元数据，并查看SWE-bench[固定源码配方](https://github.com/SWE-bench/SWE-bench/blob/2f621d545de944b174bf81894d9d11936b5bb8ae/swebench/harness/constants/python.py)：SymPy1.1与Sphinx4.1均指定Python3.9。该固定配方是环境参考，不是当前Kaggle环境的等价证明；SymPy还使用自己的bin/test，Sphinx配方会改setup／tox文件，不能原样复制成“未改测试的原生pytest验证”

已在output/research/cross-repository-qualification/historical-runtime下新建项目私有Python3.9.25，不改agent、rl、hft、progen或系统解释器。先解析镜像元数据并冻结完整包URL／build／SHA256／显式锁文件，再安装；全部下载包SHA256通过，实际Python与pip命令均退出0，installation.json的runtime_ready=true。当前三路GPU实验的冻结输入仍逐项hash一致，没有新模型／GPU实验或正式提交

首次仅解析失败是镜像未收录指定pip24.3.1，不是服务器断网或任务验证失败；availability.json与原日志保留。改为在测试前解析Python3.9兼容pip后成功，结果为availability-compatible-pip.json，没有覆盖原失败或读取新模型结果调环境。安装只涉及解释器及基础包，尚未安装两仓库测试依赖，也未执行新增任务验证

下一步须另行冻结这两题各两份新干净副本的环境资格：固定依赖与解释器身份，保留此前六次失败，禁止修改原源码／测试或增加skip，检查原始目标断言确实失败、预期通过测试保留、真实checkout导入及非空JUnit身份一致。运行时可用不等于任务可用，更不等于模型修复率；qualification_ready=false、model_repair_rate=null，尚未扩大可用于模型评分的题集，也不把这两道已用于资格的题重新称为未见验收

##### 历史环境资格检查完整结果：执行修复，验证契约仍未通过

两个仓库分别建立了项目私有依赖环境，按原固定源码setup依赖、历史配方约束及声明的pytest7.4.4准备，没有执行上游sed改setup／tox，也没有改变agent环境。安装报告、完整依赖清单与源包导入hash均已保存。随后在新增用例执行前冻结同两题各两份干净副本、120秒上限和原始失败／保留通过／JUnit身份规则，十项自造门禁边界检查通过；不能将这些组件检查算成任务修复

四次原生verify_task均已执行、退出1，真实checkout导入通过，Python源文件在pytest前后hash一致，两份副本的完整测试身份与状态也一致。两题都已实际到达预期缺陷断言，不再是Python3.12或缺docutils导致收集失败；但仍未满足冻结的整个验证契约

| 资格题 | 每份实际JUnit | 未通过资格的原因 |
| --- | --- | --- |
| Sphinx | 41通过、1失败，目标单元素tuple断言确实失败 | 公开两个数字参数ID与当前pytest生成ID不一致；截断的P2P前缀还覆盖目标F2P，冻结规则不能证明无重叠的完整对应 |
| SymPy | 86通过、3失败，两个目标断言确实失败 | 多出原始@XFAIL函数的自有XFail异常，被原生pytest按失败处理；同名test_settings还跨两个模块，公开短ID不唯一 |

SymPy原始源码中的@XFAIL及其抛出自有XFail的包装器，已与两份真实JUnit的额外失败对应核查；这是旧仓库自有runner与当前原生pytest之间的语义差异，不是Agent引入的新回归，也不能通过新增skip或篡改测试消除。Sphinx公开ID的截断／参数后缀问题同样保留，没有在看到结果后删P2P、改映射门槛或重跑挑选结果

完整证据为historical-runtime/qualification-freeze.json、qualification-summary.json与review.json，qualification_ready=false、model_repair_rate=null；四份原始结果和此前六次环境失败都保留，不合并为十道任务。没有模型、GPU实验或正式请求，现有三路模型实验的输入及SDK保护hash保持不变；这一步尚未扩大模型可评分验证集，更没有官方提分证据

这里的源码保持仅指实际记录的Python文件前后字节比较，不冒称整个仓库所有文件已逐字审计；补环境成功与测试规格可迁移是两件事。后续若探索其他仓库，须基于事先声明的runner／环境适配边界另选资格样本，保留本次失败分母，不能把替换题、改名或放宽门槛称为本次验证通过

##### 原生pytest仓库的下一组资格输入与环境准备

前两道资格题的十次CPU检查及全部不通过结果保持。新的输入准备依据运行器边界，目的性选择固定SWE-bench配方使用pytest的Flask／Pylint两个纯Python仓库；不是寻找更容易修复的题来替换旧失败。读取新题验证规格与源码之前，使用seed gemma-native-pytest-cpu-qualification-20261024，分别在各仓库内按SHA256排名固定一题，没有用问题、hint、参考修复或模型结果挑选

| 仓库 | 固定资格ID | 发布方版本元数据 |
| --- | --- | --- |
| pallets/flask | pallets__flask-5014 | 2.3 |
| pylint-dev/pylint | pylint-dev__pylint-7277 | 2.15 |

身份与GitHub base_commit源码、许可文件、验证规格已保存到cross-repository-qualification/native-pytest。复用旧输入适配器的原始源字节，仅将其工作目录指向新阶段，未调用旧的环境执行协议、修改SDK或改写旧freeze。固定Parquet经内存转运，核对原完整SHA256后只投影资格验证列，Task的参考patch／hint／problem_statement均为空；原Parquet未落盘，没有解码参考修复列，更没有向Agent喂验证内容

随后已按固定配方及原仓库build／test元数据完成两套项目私有依赖环境：Flask使用新增私有Python3.11、原requirements/tests.txt锁定依赖及运行时版本约束；Pylint使用已有项目私有Python3.9另建venv、原requirements_test_min.txt及testutils／spelling依赖，仅将editable安装改为同源码的普通wheel安装。没有更改其他session环境、全局环境或源码；两套pip check通过、安装包导入的原始__init__字节一致，清华镜像与完整依赖回执保留

系统libenchant-2不存在，安装PyEnchant包装器不等于完整拼写能力；若实际指定测试受阻则保留失败，不加skip或自行扩大系统权限。依赖安装完成仍不是任务可评，尚未执行新增资格用例，qualification_ready=false

新增资格协议单独固定两题各两份干净副本、120秒上限、原生verify_task／pytest、原始目标确实失败及所有指定保留通过、无额外失败／错误／required skip、完整JUnit身份与状态重复一致、checkout导入和Python源码前后字节保持。新JUnit身份适配仅根据Task.test_files与pytest module/class结构保留类层级，28项自造正反检查通过；不修改此前SymPy／Sphinx的冻结程序或结果，也不为新题添加事后别名。先冻结再执行，不把环境准备或自造检查算模型修复

Flask源码为BSD-3-Clause、Pylint为GPL-2.0-or-later，各自许可保留，不宣称统一MIT，也不重新发布数据

四道累计资格ID及其repo／base_commit家族均排除于后续未见验收身份池，原490条在排除后余486条身份／485个repo-commit组合。这只是身份盘点，不是486道可用题、扩大验证已成功或隐藏集代表性证明；没有新模型、GPU作业或正式提交，当前三路研究输入不变，qualification_ready=false

##### 原生pytest仓库首次资格结果与明确的依赖缺口

冻结后以低CPU优先级执行四次原生verify_task，未新增模型／GPU作业或正式请求。两份Flask副本均为59项通过、仅目标test_empty_name_not_allowed失败，全部F2P／P2P无缺失、无额外失败或skip；完整身份／状态一致、实际checkout导入和Python源码前后字节核对通过。该固定资格题的环境与身份门禁通过，不等于其他Flask题全部就绪、模型修复成功或官方代表性已证明

两份Pylint副本均在收集前退出3、没有JUnit，实际错误为pytest-benchmark3.4.1调用py.io.TerminalWriter，而pytest7.4.4提供的py.py兼容模块没有io。实际插件Requires-Dist未声明py；[插件官方changelog](https://pytest-benchmark.readthedocs.io/en/stable/changelog.html)也明确旧版未正确声明该依赖。不是libenchant报错，也不是Agent修复失败或新JUnit类名适配导致的失败

原四次结果保留在native-pytest/qualification及qualification-summary.json，整体qualification_ready=false、model_repair_rate=null，原owner已终态completed_not_ready。不能把Flask资格通过说成两个仓库都已可用，也不靠禁用benchmark／增加skip救回Pylint

另行准备py-library-compatibility：复制项目私有Pylint环境，只补py==1.11.0，保留pytest／benchmark及其余包版本，原环境与四次结果冻结不动。后续仍须在新用例前冻结同一门禁、用新的干净副本实测；这是可追溯的依赖修复，不是改写首次失败、放宽标准或策略提分

依赖修复与另行冻结的四次新副本复核现已完整结束：实际包清单恰好多py1.11.0、其余版本未变，py.io已能导入，原冻结环境／源码／SDK保护hash不变。原生驱动与28项门禁检查逐字复用，仅切换新输出和新的私有Pylint依赖路径；原失败回执没有覆盖

Flask在新阶段的两份副本仍各59通过、1个目标失败，资格通过。Pylint已不再收集前崩溃，两份均达到目标modify_sys_path断言，但每份119通过、5失败、1个原始skip及1个原始xfail，仍未满足完整资格：两个指定P2P的本地目录导入测试失败、指定jobs_score按原needs_two_cores规则跳过、一个带动态绝对路径的stdin参数ID与发布规格不匹配，另有两个非目标TOMLKit配置失败。原JUnit将xfail记为skipped，不能混称两个主动跳过

已按原源码核查动态路径参数和needs_two_cores标记／收集钩子；此处不是宣称服务器只有一个CPU，更不通过移除标记、强改CPU报告、basename模糊匹配或追加skip让门禁转绿。即使继续修tomlkit也不能自动消除其他验证契约缺口，因此本阶段到此归档，不继续逐项改依赖／身份来救回这道资格题

证据为native-pytest/review.json及py-library-compatibility/qualification-summary.json；两个阶段共8次原生检查、实际仅2道资格题，Flask固定样本ready、Pylint固定样本not_ready、全组qualification_ready=false、model_repair_rate=null。前述历史环境的10次检查另外保留，不把全部CPU调用数当独立题数。尚无新模型或正式请求，不改当前90项研究；后续扩大Flask题组仍须先逐题检查原始运行契约，不能将这一题资格推广为整个仓库全部可评

##### 题池容量限制与pytest自身的资格输入

进一步核对固定500条身份元数据后，Flask在整个固定Verified人口中实际只有pallets__flask-5014这一题；它已用于资格检查，因此没有剩余未暴露Flask题组。此前“可继续扩大题组”仅是环境通过后的待核查方向，现在容量事实已排除这条具体路线，不把唯一资格题重复使用来凑验收数量

另行固定pytest仓库的两个版本层：元数据中最新7.2有3题，旧主版本里最多的5.4有4题，均采用发布方Python3.9／pytest配方、无C扩展编译前置。选择规则先取最新版本层及容量最大的旧主版本层，再用固定seed gemma-pytest-self-cpu-qualification-20261024在每层按身份SHA256选一题；在读取问题、hint、参考修复、验证规格或源码前，已冻结pytest-dev__pytest-7205和pytest-dev__pytest-10051。这是目的性的环境可行性检查，不是代表性随机样本，也不是替换或救回旧失败

pytest-self/freeze.json、验证列投影及两个base_commit源码归档已保存，Task的问题／hint／参考patch仍为空；原始Parquet仅内存转运并核对完整SHA，未解码参考修复列。新增两题及其repo／base_commit家族从后续未见验收排除，累计6个资格ID，当前仅身份池余484条／483个不同repo-commit组合，不称可用题数

开始准备两套私有依赖环境，但尚无新增资格用例或模型请求。源归档无Git描述信息，setuptools-scm的构建版本明确使用带版本层和commit短SHA的qualification标签，不冒称上游精确发布版本；生成的_version.py仅保存在临时构建与依赖产物，不改原归档／官方data。版本相关行为、原生驱动覆盖项目pytest配置等仍需实际资格检查，安装或导入成功不代替完整测试契约

两套环境随后准备完成，原始Python文件构建前后hash未变、各自pip check通过、安装包init字节与原commit一致；正常wheel构建确实生成了缺失的_version.py，并另存依赖产物。之后另行冻结同一28项身份门禁、120秒及每题两份新副本，并增加只读导入检查：实际pytest和_pytest.config必须来自当前checkout、核心字节必须等于固定commit，不能让已安装的pytest替代被测源码

四次原生检查现已完整结束、都在导入阶段退出1、没有JUnit，尚未到目标缺陷断言。栈路径明确指向本轮checkout的src/pytest和src/_pytest/assertion/rewrite.py，后者直接导入_pytest._version；源归档没有这个构建生成文件，先前wheel安装只在私有环境中生成它，并不会自动填回新的源码副本。current_core_imports_verified=false表示完整导入未完成，不是已证明偷偷换用了另一套pytest

pytest-self/qualification-summary.json及runtime-readiness.json均qualification_ready=false，model_repair_rate=null；本轮四次失败、原始源码和身份规则保留，没有向checkout塞文件或更改原生发现参数来将本轮改为通过。这不是模型0/2，也不是pytest题不可能修复，而是正常源码构建步骤尚未与新sandbox的装配衔接

后续若补该环境缺口，应另行预先固定仅构建生成元数据的装配方式，在新的干净副本中验证核心仍来自原commit、源文件不被改写、同一完整门禁不放宽；不能修改本轮freeze或将安装包导入成功替代checkout证据。当前没有新增可用于模型比较的跨库题、模型／GPU作业或正式提交，当前90项策略研究保持原输入

##### 源码构建装配复核与上游自测插件边界

archive-build阶段在新用例前另行冻结：只在原生归档解压成功后、baseline提交与验证补丁之前，核对全部原始src下Python文件字节，然后增加正常wheel构建已生成、仅含四个常量赋值的src/_pytest/_version.py，不覆盖既有文件。原归档和此前失败保持，完整28项门禁／四份新副本／120秒不变；源成员、生成元数据、实际核心和版本身份均有独立回执

四份新副本均完成，实际checkout的pytest与_pytest.config路径／核心hash及精确构建标签都验证通过，源码装配缺口已实证修复。完整资格仍不通过：7.2层每份8通过、1个目标失败、7个fixture错误；5.4层每份26个fixture错误。原Python源码前后hash保持，原生与追加导入门禁的结果分别保存，不能把“导入成功”升级为整个验证完成

错误指向pytest自身的pytester／testdir包装fixture递归。两份原始项目配置已核查：5.4的tox.ini、7.2的pyproject.toml都明确声明顶层-p pytester；原生宿主生成的pytest.ini没有保留该项，基础插件未加载时，项目包装fixture无法找到所包装的基础fixture。这是宿主启动配置与上游自测方式的差异，不是Agent引入的代码缺陷

另行固定self-test-plugin阶段，只对顶层原生pytest命令补回上游声明的-p pytester，保留题目文件、全部其他参数、超时、验证实现、测试与严格门禁；不设置会传给嵌套pytester用例的PYTEST_PLUGINS。实际执行参数另存pytest-startup.json，不能用原commands.json隐藏宿主适配差异，也不称为官方提交可控的策略或原argv完全未变。旧结果和freeze不改，未新增模型／GPU作业或正式请求

四份实际副本现已完整结束，原生完整身份／失败／保留通过门禁、源码核心导入／字节门禁、生成版本身份及实际启动回执均通过，plugin-runtime-readiness.json的qualification_ready=true。这里的通过是原始代码按预期保留缺陷，不是Agent将题目修复成功

| 固定资格样本 | 每份原始JUnit | 需求身份与源码检查 |
| --- | --- | --- |
| pytest-dev__pytest-10051，7.2层 | 15通过、仅1个目标失败，无error／skip | 16个指定要求全部对应；两份完整身份／状态一致，当前checkout核心与原commit字节一致，66个原始src Python成员核对后仅补生成元数据 |
| pytest-dev__pytest-7205，5.4层 | 16通过、10个指定目标失败，无error／skip | 26个指定要求全部对应；两份完整身份／状态一致，当前checkout核心与原commit字节一致，61个原始src Python成员核对后仅补生成元数据 |

前者真实失败为caplog.clear后调用阶段记录未清空；后者覆盖原发布规格列出的参数显示与bytes行为，不是靠缺fixture或收集失败假充F2P。四份原始patch均空、源码在pytest前后hash保持，未添加跳过／阈值例外或重映射测试ID，正式SDK和官方data的保护hash不变。构建标签仍为明示的qualification版本，不冒称精确发布标签

这两个样本跨三个环境阶段共12次CPU调用、实际仅2道已暴露资格题，首次缺版本文件和随后缺自测插件的失败全部保留，不拿最终通过覆盖它们。继承的前阶描述与后阶stage字段应结合看：本阶仅明确许可构建元数据与顶层自测插件这两项宿主装配例外，完整身份／源码／JUnit门禁未放宽；任何后续模型比较前须另写统一无歧义协议，不能借“验证函数未改”声称实际argv或上游Docker完全等价

对应两个版本层排除全部资格ID及base_commit家族后还剩5个未暴露身份，但尚未下载验证规格或执行它们，不能称已有5道可靠验证题或据此预测公榜。保留0.17锚点、余12题不用，当前三路模型研究不改输入、不重复启动、不正式提交；环境资格收益不计作Harness策略收益

##### 固定五题开发cohort：来源已齐，尚未取得运行资格

在读取新题验证规格与源码之前，已把上述两个版本层剩余的全部5个身份固定到pytest-self/cohort，不再从中挑“容易通过”的子集；仅用固定SHA顺序排列。五题都是开发／环境校准输入，不称独立验收题，所有成员及base_commit家族预先排除于后续未见验收。累计指定资格ID为11个，剩余仅身份人口479条／478个不同repo-commit组合，不称可用题数

| 版本元数据层 | 固定成员 | 验证规模 |
| --- | --- | --- |
| 7.2 | pytest-dev__pytest-10081、pytest-dev__pytest-10356 | 各1个F2P，分别63／79个P2P |
| 5.4 | pytest-dev__pytest-7324、pytest-dev__pytest-7236、pytest-dev__pytest-7432 | 分别3／1／1个F2P、58／51／77个P2P |

五份验证规格和五个base_commit源码归档已准备并核对hash，仍只投影公共验证列，原始Parquet未落盘、未解码参考修复／问题／hint列，Task中三者为空。没有执行新增资格用例或模型请求，也未把本轮输入提供给Agent

源码级启动检查发现，标为5.4的7432已把pytest配置移到pyproject.toml，因此不能仅按版本元数据决定读取tox.ini。后续统一装配应逐commit读取真实原始配置，只恢复其中实际声明的pytester启动项；依赖层与源码核心／构建元数据身份也须分别绑定，不能把旧资格样本的核心或commit标签复制到新题冒充当前源码

开始模型比较前，须另行冻结一个统一、无继承文案歧义的执行协议与实现：每题两份原始副本、120秒、10次固定CPU检查，正常生成当前commit的版本元数据、原始src成员不被覆盖、实际核心从当前checkout导入，完整F2P失败／P2P通过、无未列失败／错误／required skip、唯一JUnit身份及两份完整身份／状态一致。官方SDK／测试／计分实现不改，实际顶层启动适配另存回执，不能藏在原命令记录后面

全5题保留在资格分母，任何失败都保留且不能算Agent修复失败；未取得全cohort资格，不把通过的子集改称原5题全部就绪。不为救回结果换题／seed／门槛，不使用余12题；本阶段只扩大待验证开发输入，不替换正式0.17锚点、不启动第二批模型或正式提交

统一qualify_pytest_cohort.py现已实现并在用例前冻结：直接调用同一原生verify_task与28项身份门禁，另7项配置优先级／显式插件启用反例检查通过，未沿用多阶段继承的相反文案。对全部5个commit分别生成当前身份的常量版本元数据、保存原始src成员hash与真实配置出处；源码核心／init必须来自当前checkout并与当前commit一致，不能仅复用旧资格样本的源码或版本文件

执行协议与程序hash、全部输入与两套只读依赖环境hash已保存在cohort/qualification-freeze.json，固定10次原始副本检查只启动一次、以低CPU优先级运行，没有新模型／GPU或正式请求。实际命令日志同时保存原始与补回上游启动项后的参数；所有10次与5对都必须通过原始缺陷／保留通过／源码／唯一JUnit及双副本一致门禁，才称完整cohort资格就绪，仍不等于模型提分或独立验收

##### 五题cohort首次完整资格：10次已结束，0/5取得完整资格

全部10次已完整结束，原冻结输入／运行环境／SDK保护hash不变，owner为completed_not_ready。五题的两份副本结果分别一致，但都不满足完整资格；不能从前两道Pytest资格题通过推断同版本层其余题都可评

| 固定成员 | 每份原始结果 | 本轮未就绪的直接证据 |
| --- | --- | --- |
| pytest-dev__pytest-10081 | 57通过、7失败、9个非required跳过 | 6个指定P2P也失败；其中async示例文件按错误的根目录查找，尚有其他unittest检查失败 |
| pytest-dev__pytest-7324 | 导入阶段退出1、没有JUnit | 当前commit源码已依赖iniconfig，复用的5.4资格样本环境没有它 |
| pytest-dev__pytest-7236 | 46通过、6失败、9个非required跳过 | 5个指定P2P也失败，包含示例目录与unittest行为检查，不是仅保留目标缺陷 |
| pytest-dev__pytest-7432 | 导入阶段退出1、没有JUnit | 当前commit同样新增iniconfig依赖，粗版本标签不足以推断完整依赖 |
| pytest-dev__pytest-10356 | 87通过、2失败、1个原始xfail | 一个指定P2P因示例目录查找失败；不能只保留目标mark_mro失败而忽略它 |

三份能导入的源码均确认实际init／核心来自当前checkout、字节与commit一致、版本标签匹配；全部10份都没有覆盖原src成员，Python文件在pytest前后hash保持。9个非required skip及原始xfail完整保留，门禁本就允许非required跳过，它们不是拒绝本组的原因；真正阻塞的是导入缺依赖、指定P2P失败／非目标失败等完整契约缺口

这轮证明仅按粗版本层共享依赖环境、仅补pytester启动仍不足以扩大可用开发集。源码示例路径失败属于扩展外部仓库时的宿主装配问题，不推断Kaggle官方隐藏评测有相同故障；其他unittest失败只作有限定位，未冒称每项均完成完整语义归因。原始JUnit、命令、源码／版本／启动回执及全部失败保存在cohort/qualification和qualification-summary.json

qualification_ready=false、model_repair_rate=null，仍未新增可靠模型验证题，不把结果写成Agent 0/5。五题全部保留在资格分母，不删坏题、不重命名成功子集、不改原冻结门槛或原结果；没有模型／GPU作业或正式请求。若以后补齐逐commit依赖与上游完整自测配置，须作为新的环境协议明确记录，不能偷偷改变本轮规则或把宿主适配宣称为可提交Harness收益

##### 五题上游配置与逐commit依赖：新的环境协议

源码读取候选已完整60项结案且不采用之后，转而补齐上述固定五题的环境缺口，不再以同30道熟题的工具变体充当泛化证据。五题、原始F2P／P2P、两份干净副本、120秒及28项原身份门禁全部保留，不读参考修复或选“能通过”的子集，不使用余12道原比赛题

prepare_upstream_startup.py逐commit复制原私有Python3.9依赖环境，在临时构建副本中正常安装该commit声明的项目与testing extras；既有非pytest包版本由原inventory约束，新增声明依赖可以补齐。原环境和此前十次失败不改，原有Python源码逐字节核对，只保留正常构建产生的版本常量元数据，不将其合成qualification版本称为上游精确发布标签

新qualify_upstream_startup.py沿用同一原生verify_task／源码及完整JUnit身份门禁，改为以-c显式指定该commit完整原配置，而不是仅摘出-p pytester。原生显式CLI覆盖、指定测试文件和超时仍记录且不变，因此不是完全相同argv或官方Docker复现；源码配置hash在实际调用前核对，不能偷偷覆盖测试或改写上轮结果

[pytest7.2参数文档](https://pytest.org/en/7.2.x/reference/reference.html)明确-c选择配置、-o覆盖配置；[pytester文档](https://pytest.org/en/7.2.x/how-to/writing_plugins.html)明确copy_example依赖pytester_example_dir。逐commit源码实际声明了该目录及其他自测选项，完整使用原配置是环境适配，不是选手可提交的Harness优化或已证实的修复收益

pyflakes及28项身份／7项配置反例检查已通过；环境准备仅启动一次、低CPU优先级、owner PID928181／create_time1792801635.62，实际状态见pytest-self/cohort/upstream-startup/preparation-owner.json。依赖准备并不是运行资格通过；完整验证前还须冻结全部新环境／程序／原输入及十次调用协议，无模型／GPU／正式请求，不重启重复作业，原来0/5未就绪结论保留

该协议十次原始副本检查随后已完整结束，全部冻结输入及源码保持，10081与10356各两份通过完整资格；五题整体仍未通过。7324／7432不再缺依赖崩溃，已分别达到三个／一个目标断言失败，但旧pytest根目录落在testing，导致原始JUnit文件路径无法按预定规则绑定。7236同样根目录偏移，示例查找变为testing/testing/example_scripts，另外还保留目标teardown断言；不能将这些未绑定结果认定为模型失败或改计分器救回

固定7324的原始findpaths.py实际源码明确：传-c且没有--rootdir时，以测试参数共同祖先为根，而非配置目录。probe_upstream_root.py在五个已安装的精确commit上做十次配置解析、不收集或执行任务测试：三个旧commit的隐式根都偏移，五个显式根都正确，上游示例目录值保持。不能把这个探针说成十份任务资格

随后rooted-startup作为另一明确协议预先冻结，复用上一份已固定驱动、全部五套依赖和同一28项门禁，只给顶层命令增加--rootdir=/workspace。七项配置反例和十项真实解析检查通过；两份新干净副本／每份120秒、全部五题及原完整身份／F2P／P2P标准不变，不修改JUnit路径映射、测试、原生验证实现、SDK或嵌套pytester调用。旧十份结果保留，新十次调用另存rooted-startup；这仍是宿主装配资格，不是可提交策略、官方Docker等价或模型提分

##### 固定五题完整资格已取得：不是模型修复结果

rooted-startup的十次原始副本现已完整结束，五对全部通过，owner为completed_ready且实际进程已退出。冻结输入不变，每份都从自己的当前checkout导入原commit核心、精确绑定构建标签，原有src Python字节在测试前后保持；完整JUnit身份／状态两份一致，所有指定F2P仍失败、P2P均通过，没有未列错误／失败或required跳过，空Agent补丁、原生退出1及resolved=false均符合原代码资格预期

| 固定开发题 | 每份原代码JUnit | 发布规格中的目标失败／保留通过 |
| --- | --- | --- |
| pytest-dev__pytest-10081 | 63通过、1失败、9个非required跳过 | 1／63 |
| pytest-dev__pytest-7324 | 80通过、3失败 | 3／58 |
| pytest-dev__pytest-7236 | 51通过、1失败、9个非required跳过 | 1／51 |
| pytest-dev__pytest-7432 | 78通过、1失败 | 1／77 |
| pytest-dev__pytest-10356 | 88通过、1失败、1个原始xfail | 1／79 |

这次没有改JUnit绑定器或将required失败改为skip，也没有删去前三题来声称整组就绪。旧首轮0/5、随后完整原配置2/5、再补显式仓库根后5/5各自的十份结果和冻结协议均保留，不能覆盖为“最初一次就通过”。相对文件路径从testing根恢复为仓库根，是实际启动修正，不是事后字符串补前缀重计分

当前资格证据为pytest-self/cohort/rooted-startup/qualification-summary.json、readiness-review.json及十份原始JUnit／commands／phase-identities；冻结SHA256为23159c69fc0bfa9f2ade79b66b69ecbd159e72293932a65a7b2c30ee44bc09cb。新增模型／GPU／正式请求均为0，model_repair_rate=null，不称修复5题、已有稳定分数提升或隐藏集代表性已证明

五题均已作环境校准并暴露，不称独立验收，未改原资格选择、题、seed或阈值；全局剩余身份人口也不重新把它们计入未见池。后续真正模型比较须先冻结问题字段来源、统一的Agent工作区及验证装配、候选／精确对照和预算，不能只给独立验证端修环境而让Agent使用另一套配置，也不把这项宿主适配写入提交ZIP冒充Harness收益。0.17仍为正式锚点，0.24未达到，余12题未用

##### Agent与干净验证工作区的统一装配检查

qualify_agent_environment.py另行冻结五题的CPU原生Agent A→原生干净验证B→额外干净验证C，精确0.17工具／生成／五分钟预算保持，但实际模型替换为明确的脚本化假BaseLlm。输入只给通用环境检查说明，不给真实问题／hint／参考修复；假模型检查当前checkout导入与默认配置、pytest及py.test入口，再写无修复作用的qualification_marker.py并提交。预期非空标记补丁能应用到两份干净副本，但原始F2P仍失败、P2P保持，不称任务修复或Gemma推理

三个阶段统一Python3.9与当前commit的私有依赖，普通console入口按该commit安装元数据构建；正常生成的_version常量只作构建装配。SDK生成的pytest.ini在基线提交前移到本sandbox tmp中，原有tox.ini／pyproject.toml保留，Agent默认发现与验证显式-c／rootdir均使用同一上游配置，不向嵌套pytester注入PYTEST_ADDOPTS或PYTEST_PLUGINS，不修改SDK、正式数据、测试或计分器

首次CPU资格在第一题已生成标记补丁、A/B已分离后中止：原生B在应用测试补丁后再次调用配置初始化，旧适配器以同名备份仅出现一次为前提，第二次触发断言。实际只尝试一题、未完成独立C及统一case审核，不记作五题执行或模型0/5；原freeze、trace、patch、commands、phase-identities和失败日志保留在unified-runtime，failure.json及owner终态failed_native_setup_assertion真实记录

修正以另一明确冻结协议repeatable-startup执行：保留每一次SDK生成配置的独立tmp备份后继续原生初始化，不跳过SDK调用，不更改原题／预算／验证要求。三个自造组件检查验证无文件、第一代、第二代备份均不丢内容；pyflakes通过。相同五题、15份计划隔离工作区、10次计划原生干净验证仅启动一次；这仍是CPU工作流资格，真实模型／GPU／正式请求均为0，完整结束前不声称三阶段统一已通过

重复初始化修复后的首次检查完成首题全部A/B/C，但第二题在原生B正常取得预期退出1、无错误后，被观察检查的stdout专用断言中止。原始trace实证：两条console调用都退出0，新pytest将版本写stdout，旧pytest将版本写stderr并带rsyncdirs警告；这不是命令入口失败或模型修复失败。实际尝试2题、完成1份case审核、原生B两次、独立C一次，原始数据保留，repeatable-startup/failure.json及owner终态failed_console_observation_assertion明确记录，不称五题完整执行

当前qualify_task_runtime.py以agent-verifier-alignment另行冻结相同五题和完整标准，修正重复初始化装配及版本观察：只读两路真实输出共同确认两个精确commit版本与退出0，不修改原始stdout／stderr、工具轨迹或任务测试判定。六个输出通道正反例及三个重复初始化组件检查通过，旧两次中止的源码／冻结／日志／原始结果不改。计划仍为五题原生脚本化A、十次干净B/C、15份隔离工作区；非真实模型或独立策略验收

##### 五题Agent／双干净验证装配已完整通过

当前agent-verifier-alignment已完整完成五题，实际15个互不相同sandbox、五次原生干净B与五次额外干净C；owner终态completed_cpu_alignment_ready且进程已退出。每题实际六次假模型内部请求、共享工具动作计数3，既不是30次真实Gemma推理，也不是五道已修复软件问题

每个Agent真实调用当前checkout的Python3.9／pytest核心、默认上游配置和两个console入口，写出并submit一个252字节的通用标记补丁。每个B/C的基线树均无标记，应用后均有同一标记，原src成员字节不变，原生与独立验证各自的完整JUnit身份／状态逐条等于该题原代码资格记录。目标F2P仍失败、所有指定P2P保持通过，原非required跳过／xfail均保留，不把非空补丁或原生流程状态SUCCESS当成修复通过

调用计数的证据边界另见request-count-review.json：每题原生total_llm_calls与trace中llm_call_count之和均为6，但调用方持有的假模型prototype.requests及request-metadata.json为空，receipt中scripted_requests也因此为0。旧字段原样保留，不将它解释成零实际执行，也不声称已核实对象复制的具体原因；当前30次内部调用以原生／trace对应为证，不等同于HTTP或真实Gemma请求，生成参数与工具过程仍由实际脚本化执行和原始轨迹核对

同一环境装配函数覆盖A/B/C；原生B/C重复初始化的每代生成配置都保留在各自tmp，原tox.ini／pyproject.toml未被替换，SDK配置调用没有跳过。原生显式CLI覆盖和构建qualification标签仍是明示宿主适配，不称上游Docker或官方隐藏评测完全等价；本检查只证明这些实际调用，不证明Agent任意命令都自动等价

全部当前源码／freeze／原始trace／patch／双JUnit／phase／commands另经只读audit_task_runtime.py核对，未新增任务执行。证据为agent-verifier-alignment/receipt.json与audit.json，冻结SHA256为f4dfb7b47640a25de57950c2e17ca48b80dd177e75190485e5897c5fa2fcb4c2；real_model_requests=0、new_gpu_jobs=0、formal_requests=0、model_repair_rate=null。之前中止的实际1题／2题、各自原始结果和原因完整保留，不覆盖为一次通过

##### 历史问题输入准备：后续模型对照见顶部，勿重复

在任何问题列投影之前，project_agent_questions.py先冻结原来相同五个身份、repo／base_commit及已有三阶段CPU资格；然后对固定revision的完整Parquet在内存核对SHA256，仅解码instance_id／repo／base_commit／problem_statement四列，未解码参考patch、hint或新验证列，原始Parquet不落盘。网页读取工具无法打开固定README，因此没有新增数据授权或许可证声明；使用的固定数据来源／边界沿用已有记录，不将代码仓库许可自动套给数据

新的model-inputs/tasks.jsonl只在旧验证Task中补入原始公开问题文本，保留空参考修复／空hint和原验证规格；旧资格输入不改，snapshots为到原归档目录的软链接而非第二份副本。五题问题各2905／5278／2692／469／773字符，未截短或按结果选子集，输入SHA256见model-inputs/projection.json。脚本与来源保护hash前后核对，真实模型／GPU／正式请求仍为0

上述历史准备后，atomic-cross-repository已完成相同五题的10项模型对照并不采用，详见本页顶部与atomic_edits.md；此处零模型数仅为当时准备边界，不再作为未使用声明。不得重启旧候选或用五题救回阈值。正式锚点仍0.17、0.24未达到，当前自动提交授权以最新harness_goal.md为准。
