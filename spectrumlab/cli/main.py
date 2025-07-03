"""
SpectrumLab 命令行界面
"""

import argparse
from typing import Optional, List


def main(argv: Optional[List[str]] = None) -> int:
    """
    SpectrumLab 主命令行入口点
    """
    parser = argparse.ArgumentParser(
        prog="spectrumlab", description="化学谱学大模型 Benchmark 引擎"
    )

    parser.add_argument("--version", action="version", version="%(prog)s 0.0.1")

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 示例子命令
    eval_parser = subparsers.add_parser("eval", help="运行评估")
    eval_parser.add_argument("--model", help="模型名称", required=True)
    eval_parser.add_argument("--dataset", help="数据集名称", required=True)

    args = parser.parse_args(argv)

    if args.command == "eval":
        print(f"正在评估模型: {args.model}")
        print(f"使用数据集: {args.dataset}")
        return 0
    elif args.command is None:
        parser.print_help()
        return 0

    return 0


if __name__ == "__main__":
    exit(main())
