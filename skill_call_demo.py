#!/usr/bin/env python3
"""读取文件内容并调用 skill 的 Python demo.

用法示例:
    python skill_call_demo.py --file ./需求说明.txt --skill skill-creator --dry-run
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def read_text_file(path: Path) -> str:
    """读取 UTF-8 文本文件并返回内容。"""
    return path.read_text(encoding="utf-8")


def build_prompt(skill_name: str, file_content: str) -> str:
    """根据文件内容构造一段可直接发送给 Codex 的请求。"""
    return (
        f"请使用 ${skill_name} 处理以下文件内容，并给出可执行结果。\n\n"
        "要求：\n"
        "1) 先总结文件关键信息；\n"
        "2) 再按 skill 的最佳实践执行任务；\n"
        "3) 输出分步骤结果和最终结论。\n\n"
        "文件内容如下：\n"
        "---\n"
        f"{file_content}\n"
        "---"
    )


def invoke_codex(prompt: str) -> str:
    """通过 codex CLI 调用模型执行 skill 请求。"""
    if shutil.which("codex") is None:
        raise RuntimeError("未找到 codex 命令。请先安装并配置 Codex CLI。")

    cmd = ["codex", "exec", prompt, "--output-last-message", "-"]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="读取文件并调用 skill 的 demo")
    parser.add_argument("--file", required=True, type=Path, help="输入文本文件路径")
    parser.add_argument("--skill", default="skill-creator", help="要调用的 skill 名称")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅打印将要发送的 prompt，不实际调用 codex",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 输出，便于后续自动化处理",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not args.file.exists():
        print(f"文件不存在: {args.file}", file=sys.stderr)
        return 2

    file_content = read_text_file(args.file)
    prompt = build_prompt(args.skill, file_content)

    if args.dry_run:
        output = prompt
    else:
        try:
            output = invoke_codex(prompt)
        except Exception as exc:
            print(f"调用失败: {exc}", file=sys.stderr)
            return 1

    if args.json:
        print(json.dumps({"skill": args.skill, "file": str(args.file), "output": output}, ensure_ascii=False, indent=2))
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
