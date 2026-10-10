##### 本地检查

本地模拟模型驱动官方 Agent loop，检查工具调用、补丁提取和测试调用，产物固定在 output/local-check

macOS 无法使用官方 manylinux wheels 复现 Linux 测试环境，本地模拟结果不作为模型分数

##### 环境

```sh
python3.12 -m venv .venv-harness
.venv-harness/bin/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple \
  pyyaml pydantic python-dotenv rich docker cachetools networkx numpy pandas litellm google-genai 'google-adk==1.36.1' pyflakes
.venv-harness/bin/pip install --no-deps data/competition/sdk/*.whl
.venv-harness/bin/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple \
  pytest hatchling starlette httpx anyio email-validator typer fastapi-cli \
  python-multipart pydantic-settings pydantic-extra-types typing-inspection uvicorn itsdangerous jinja2
```

测试依赖安装到宿主解释器，subprocess sandbox 通过 system_site_packages 继承

##### 执行

```sh
PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple \
  .venv-harness/bin/python src/run_local_mock.py
```

查看 evaluation/task_results.jsonl、patches 和 test_outputs

已验证过模拟模型产出 273 字节补丁并触发 pytest，测试因缺 scripts.prepare_release 退出 2，说明测试调用完成，未说明任务修复成功

test_exit_code=-1 表示验证未执行，No module named pytest 表示测试环境未就绪
