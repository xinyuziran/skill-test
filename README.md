# skill-test

skill prompt test

## Python Demo：读取文件并调用 Skill

下面提供一个最小可运行示例：`skill_call_demo.py`。

### Demo 能做什么

- 读取本地文本文件内容（UTF-8）
- 拼装一段带 `$skill-name` 的请求 prompt
- 可选：通过 `codex exec` 真正发起调用
- 支持 `--dry-run` 先只看 prompt

### 代码文件

- `skill_call_demo.py`

### 使用方式

1) 准备一个输入文件（例如 `input.txt`）

```text
请帮我基于以下需求创建一个 skill：
- 目标：把接口文档转成前端调用手册
- 约束：输出包含示例请求与错误码说明
```

2) 仅预览将发送的 skill 请求（推荐先跑这个）

```bash
python skill_call_demo.py --file input.txt --skill skill-creator --dry-run
```

3) 真正调用（需要本机已安装并登录 Codex CLI）

```bash
python skill_call_demo.py --file input.txt --skill skill-creator
```

4) 以 JSON 输出（便于流水线集成）

```bash
python skill_call_demo.py --file input.txt --skill skill-creator --dry-run --json
```

### 参数说明

- `--file`：必填，输入文本文件路径
- `--skill`：可选，默认 `skill-creator`
- `--dry-run`：仅打印 prompt，不实际调用
- `--json`：JSON 格式输出结果
