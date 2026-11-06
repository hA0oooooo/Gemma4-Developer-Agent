##### 当前开发基线

submission/已恢复为公榜0.17原包中的四份文本，单31B、六原生工具、8192输出／4096思考、5分钟／24动作／40轮、单命令60秒
原始评分ref57485865，原包 output/research/capacity-trial/submission.zip
SHA256 baea5d6b2c006d4ac758f79b5cfb2c500eefa84e08b37cc1f220e2a72ccf7563

本次仅整理代码与文档，没有重新评分，既有官方与本地结论见[Harness收尾](../research/harness_closeout.md)
旧Skill配置已归档到 output/archive/review-ready-baseline/submission，不是当前默认方案
旧提交历史全文保留于同归档目录的 agent/workflow/baseline.md；原始正式回执仍在output/research各研究目录

##### CPU检查与打包

在仓库根目录，使用 /mnt/data/haoyang/miniconda3/envs/agent/bin/python

```bash
export LITELLM_LOCAL_MODEL_COST_MAP=True
python -m pyflakes src/*.py
python -m unittest discover -s src -p 'test_*.py'
python src/build_submission.py --output output/packages/review.zip
```

打包执行官方schema校验，不启动Gemma、不调用Kaggle
必须显式指定新输出路径，不能覆盖两个受保护旧ZIP
重新压缩的ZIP不保证容器hash相同，内部四文件应逐字节匹配原0.17包

##### 真实评测与独立复核

单题入口src/run_baseline.py，配对入口src/evaluate_development.py，补丁独立复核入口src/check_patch.py
模型、任务、输入、依赖与资源准备见[环境工作流](official_starter.md)，结果判读与环境资格见[本地检查](local_check.md)
旧30题是开发熟题，重新运行不产生独立验收
src/run_local_mock.py只检验接线，不代表Gemma能力；打包和CPU回归通过也不是修复分数

##### 正式提交

src/submit.py必须显式 --file 与 --message
只有用户授权新方案且完整验收通过时才提交一次，先核对账户、额度、待评分、整批12小时预算和包身份
状态不明先查记录，不自动重发；不能使用排行榜反复试探来选择策略
本轮整理不调用提交入口

##### 已有正式比较

0.17为保留基线，接口预算融合0.13，公开0.22原样包在我方0.15
完整版本映射与证据见[Harness收尾](../research/harness_closeout.md)，固定实现diff与环境审计位于output/research/harness-closeout
没有逐题官方日志时，不从总分推断某道题失败或认定作者虚报
