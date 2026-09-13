"""命令行main函数入口点"""

 #引入库函数
from __future__ import annotations

import sys
from collections.abc import Sequence
from pathlib import Path

from plagiarism_checker import calculate_similarity


def read_text(path: Path) -> str:
    """读取UTF-8文件"""

    try:
        return path.read_text(encoding="utf-8-sig")
    except OSError as error:
        raise ValueError(f"无法读取文件 {path}: {error}") from error
    except UnicodeError as error:
        raise ValueError(f"文件不是有效的 UTF-8 文本 {path}: {error}") from error


def write_result(path: Path, similarity: float) -> None:
    """将相似度四舍五入到小数点后两位。"""

    try:
        path.write_text(f"{similarity:.2f}", encoding="utf-8")
    except OSError as error:
        raise ValueError(f"无法写入答案文件 {path}: {error}") from error


def run(arguments: Sequence[str]) -> int:
    """使用三个路径参数运行应用程序，并返回退出代码。"""

    if len(arguments) != 3:
        usage = "用法: python main.py <原文绝对路径> <抄袭文绝对路径> <答案绝对路径>"
        print(usage, file=sys.stderr)
        return 2

    original_path, suspected_path, output_path = map(Path, arguments)
    try:
        original = read_text(original_path)
        suspected = read_text(suspected_path)
        write_result(output_path, calculate_similarity(original, suspected))
    except ValueError as error:
        print(f"错误: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))
