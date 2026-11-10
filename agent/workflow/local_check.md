##### 当前检查入口

当前CPU检查见[基线工作流](baseline.md)，本页下文为历史诊断经验，不代表仍有运行中实验
读取Skill原件在output/research/read-contract/shipping/agent/skills/read-window，专用测试在output/archive/review-ready-baseline/src，不在默认submission或通用回归中

##### 运行器导入资格的实际教训

旧研究运行器queue.py遮蔽Python标准库queue，urllib3因此找不到LifoQueue；只加安全导入模式又暴露缺少项目src路径。当前实际成功方式是Python3.12安全路径模式配合显式项目src的PYTHONPATH，并让所有worker继承；需从真实worker入口验证到服务构造，单纯schema通过不够。两处原失败／三worker退出码和日志均保留在read-window-repair及recovery/prelaunch-failure

后续新运行器不要沿用标准库同名模块，不直接重放已封存queue.py。CPU Mock仅证明接线和共享预算，必须另核真实API进程、创建时间、模型响应及任务patch／测试；私有namespace中宿主localhost连不上，或运行中归档model_server.log尚未复制，都不能当作停止并重复启动的依据

##### 本地修复比较前的环境资格

当前实测表明，测试失败可能同时包含目标缺陷和依赖差异，不能把所有原版失败都排除，也不能只凭补丁测试绿色认定需求完成。新一轮比较在模型开始前固定题目、依赖profile、源码／测试身份和补充API检查；保留题只在候选通过预定开发门槛后释放，不拿来排查环境或调参

先用干净原snapshot在同一隔离环境运行现有套件，记录实际pip版本、原始JUnit身份和每项失败；再将补丁应用至另一干净副本，以完全相同依赖运行。原版因目标bug失败是正常信号；怀疑环境问题时，只能另行登记诊断，依据自身仓库锁定版本做单变量比较。原版和补丁必须一起比较，保留失败及额外验证成本，不能在当前模型批次中换依赖或重写分数

已完成Rich3130例证：当前Pygments2.21.0下干净原版1过5失败、补丁4过2失败；隔离新环境仅改为原poetry.lock的Pygments2.15.1，原版3过3失败、补丁6过0失败，六项身份相同且无skip。此处两个剩余失败可归到固定版本差异，但0.17对照与新读取候选生成相同补丁，不能算新方案增益，也不证明Kaggle使用历史版本。原始证据output/research/read-window-repair/recovery/compatibility，当前36项严格判定未变

真实行为门禁必须走实际消费入口，而非仅看对象字段：例如Requests经prepare_auth之后才消费path_url，FastAPI通过实际路由请求检查根／兄弟scopes及重复调用，HTTPX解析器测试不覆盖服务退出或请求体清理。检查在模型前登记，原生套件、独立副本套件、补充API结果和源码审核分别报告；补充检查失败不能用退出码0或绿色子集掩盖，补充检查通过也不推导完整隐藏集得分

本批环境诊断仅属于开发校准，未改官方data／测试／计分器；未来若修正环境profile，需要另行冻结并从头比较新候选与原样0.17，不能回写旧结案或用新依赖救回负结果。当前运行中的reasoned-test-design继续原冻结环境，不据上述诊断更改输入

##### 在行共享模型服务的日志位置

src/run_experiments.py在共享服务的finally阶段才把server.log_path复制为分片model_server.log；运行中该归档文件不存在不等于服务失败。当前feedback-budget三份自有API的真实stdout分别在/proc/<已核对PID>/fd/1指向的/tmp/inference_server_<port>_*.log，已见实际chat HTTP200。先按owner／CLI／API PID及创建时间确认身份，再读取其自己的日志；此实验处于私有网络namespace，不能把控制端直接连接不到127.0.0.1当作停止证据。SSH断线、缺归档文件或观察超时均不能据此重复启动。

##### 本地计划seed的统一生效入口（2026-10-27）

src/run_baseline.py已取消只改configs/*.yaml的旧注入方式，使用现有SDK GenerationConstraints编译接口将--seed应用到所有编译创建的LlmAgent，包括内联／引用／未写生成配置的Agent、子Agent与AgentTool；明确覆盖其显式seed，但不修改候选原始或复制后的YAML。protocol.json记录generation_seed_override，config_sha256记录实际未重写的配置字节；后续审核应同时核实执行覆盖规则和实际请求，不能仅查某份sampling.yaml。未指定--seed时维持SDK默认路径与原显式seed，不为SDK后台摘要请求统一seed作保证。

继承SDK所有生成限制／默认值，模型、工具、共享预算与验证器不变。六项新增回归经真实SDK编译／Runner脚本请求检查inline、include、default、AgentTool与父续接的seed，并核对生成字段、源码字节及预算；全src76单元与16元数据门禁通过、pyflakes干净。它不是Gemma推理、HTTP服务、完整任务verifier或提分实验。原先三次CPU夹具错误及失败日志保留：模型复制使实例记录器失效、skip_summarization导致父不续接、初版无seed对照没有应用EvalConfig的SDK默认值，均修正夹具后完整检查。

完整来源／日志／旧源码及当前合格源码快照位于output/research/seed-provenance，qualification.json SHA256=4adf225c9ac8a4e9a8fbe0bd010e0d5291a0867a17aaac60e646af4317c9c1a2。run_baseline.py SHA256=162b35ada8f5d3487743b3b1160e33384373315aabbfdd201a90ff2ba3466cae，test_generation_seed.py SHA256=376223f4409add5b4149edcc19c25c1b44828768685d3040ebb1d6ba8df8601e。旧冻结研究不回写或重跑，下一项模型计划须绑定新核心身份；0.17包／isolated-proposals结案selection均未变，Gemma／新verifier／正式请求均0。

##### CPU 模拟检查

用途是检查 Agent loop、工具执行、补丁提取和 pytest 调用，不使用真实 Gemma，也不代表任务修复能力

在 Linux 仓库根目录与 agent 环境执行

```bash
python -m pyflakes src/*.py
python -m pip check
python src/build_submission.py --output output/packages/review.zip
python src/run_local_mock.py
```

模拟结果保存在 output/local-check，真实 GPU 评测保存在 output/baseline；官方环境准备和真实运行命令统一见 [official_starter.md](official_starter.md)

当前模拟链路产出 273 字节补丁并调用 pytest，test_exit_code=2、resolved=False、error=None；模拟模型只写入一个标记，不实现任务要求，因此不要求验证测试通过

test_exit_code=-1 表示验证未执行；非零 exit code 要结合测试日志区分环境失败与目标功能尚未实现，不能仅凭 ModuleNotFoundError 判断环境缺包

##### 冻结输入清单与输出产物的文件身份

run_experiments.py允许--plan直接指向输出目录的plan.json；此时它也是调用方可能已冻结的输入，不能无条件重新序列化。当前同文件／符号链接／硬链接均保留输入字节和mtime，输入输出分离时仍写输出plan.json。CLI回归见src/test_plan_preservation.py；修正前3类别名布局失败，修正后4项通过，另6项服务守卫／3项调度及pyflakes通过，原始证据output/research/native-e4b/runner-plan-fix-verification.json。

该问题使native-e4b原八项计划在第一波4项后触发冻结字节门禁并终止；运行题集／seed／模型／预算的JSON含义未变，但本批不完整、未配对且不可接纳。失败、成本及两份各自阳性源码缺口均保留，未重跑／放宽门槛救回。当前修正不是质量优化或官方得分，新研究须绑定修正后的源码而非宣称旧freeze未变。


##### OAuth真实到期边界修正

2026-10-27在feedback-budget完整封签后，src/kaggle_network.py新增authenticate_kaggle，现有src/submit.py与后续官方观察器调用它。安装版SDK的access_token_has_expired实际使用now-30min，曾在真实到期后继续沿用旧token而使GetSubmissionLimits返回401；单次官方续期及随后完整历史PENDING核查已留证。新包装先保留SDK认证，只有OAuth真实到期或不足60秒时调用现存官方refresh一次，绑定同一账户后更新客户端token；legacy／有效OAuth路径、显式包参数、额度及单次提交不变，失败不重发且错误不含URL／凭据。

output/research/oauth-expiry保留核心及观察器精确改前源码、差分、19项初查及新增失败门禁后的21项CPU检查。21项在禁止所有requests HTTP的条件下通过，覆盖真实SDK过期后30分钟窗口、60秒边界、有效／legacy、未知状态、失败不续试、账户绑定及认证失败不上传／提交；pyflakes通过。没有新增模型、真实续期、官方查询或提交，未升级SDK；qualification SHA256=8ed3e6df05abbf0301a7bbf31b2289884abf6b1f9611f9eb5a109555efda7806。后续新freeze需绑定新核心，不重写旧保护清单或重跑已封签分析器。
