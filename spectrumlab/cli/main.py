import argparse
import sys
from typing import Optional, List

from .api import run_evaluation
from spectrumlab.models import (
    GPT4o,
    Claude_Sonnet_3_5,
    DeepSeek_VL2,
    InternVL,
    Qwen_2_5_VL_32B,
)

AVAILABLE_MODELS = {
    "gpt4o": GPT4o,
    "claude": Claude_Sonnet_3_5,
    "deepseek": DeepSeek_VL2,
    "internvl": InternVL,
    "qwen-vl": Qwen_2_5_VL_32B,
}


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="spectrumlab",
        description="A pioneering unified platform designed to systematize and accelerate deep learning research in spectroscopy",
    )

    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    eval_parser = subparsers.add_parser("eval", help="Run model evaluation")

    eval_parser.add_argument(
        "--model",
        "-m",
        required=True,
        choices=list(AVAILABLE_MODELS.keys()),
        help=f"Model name, options: {', '.join(AVAILABLE_MODELS.keys())}",
    )

    eval_parser.add_argument(
        "--level",
        "-l",
        required=True,
        choices=["signal", "perception", "semantic", "generation"],
        help="Evaluation level",
    )

    eval_parser.add_argument(
        "--subcategories",
        "-s",
        nargs="*",
        help="Specify subcategories (optional, default: all)",
    )

    eval_parser.add_argument(
        "--data-path", "-d", default="./data", help="Data path (default: ./data)"
    )

    eval_parser.add_argument(
        "--output", "-o", default="./results", help="Output path (default: ./results)"
    )

    eval_parser.add_argument(
        "--max-length", type=int, default=512, help="Max output length (default: 512)"
    )

    args = parser.parse_args(argv)

    if args.command == "eval":
        try:
            # Initialize the model
            if args.model not in AVAILABLE_MODELS:
                available = ", ".join(AVAILABLE_MODELS.keys())
                raise ValueError(
                    f"Unsupported model: {args.model}. Available: {available}"
                )

            model_class = AVAILABLE_MODELS[args.model]
            model_instance = model_class()

            results = run_evaluation(
                model=model_instance,
                level=args.level,
                subcategories=args.subcategories,
                data_path=args.data_path,
                save_path=args.output,
                max_out_len=args.max_length,
            )

            print("\n" + "=" * 50)
            print("📊 Evaluation Results")
            print("=" * 50)

            if "error" in results:
                print(f"❌ Evaluation failed: {results['error']}")
                return 1

            metrics = results.get("metrics", {})
            overall = metrics.get("overall", {})

            print("✅ Evaluation completed!")
            print(f"📈 Overall accuracy: {overall.get('accuracy', 0):.2f}%")
            print(f"✅ Correct answers: {overall.get('correct', 0)}")
            print(f"📝 Total questions: {overall.get('total', 0)}")

            subcategory_metrics = metrics.get("subcategory_metrics", {})
            if subcategory_metrics:
                print("\n📋 Subcategory details:")
                for subcategory, sub_metrics in subcategory_metrics.items():
                    acc = sub_metrics.get("accuracy", 0)
                    correct = sub_metrics.get("correct", 0)
                    total = sub_metrics.get("total", 0)
                    print(f"  {subcategory}: {acc:.2f}% ({correct}/{total})")

            print(f"\n💾 Results saved to: {args.output}")
            return 0

        except Exception as e:
            print(f"❌ Evaluation failed: {e}")
            return 1

    elif args.command is None:
        parser.print_help()
        return 0
    else:
        print(f"❌ Unknown command: {args.command}")
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
