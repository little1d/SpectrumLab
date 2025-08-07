from typing import List, Dict, Optional, Any
from ..benchmark import get_benchmark_group
from ..evaluator import get_evaluator


def run_evaluation(
    model,
    level: str,
    subcategories: Optional[List[str]] = None,
    data_path: str = "./data",
    save_path: str = "./results",
    max_out_len: int = 512,
) -> Dict[str, Any]:
    print("🚀 Starting evaluation")
    print(f"📊 Model: {model.__class__.__name__}")
    print(f"📁 Level: {level}")
    print(f"📂 Data path: {data_path}")
    print(f"💾 Save path: {save_path}")

    print("\n📥 Loading benchmark data...")
    benchmark = get_benchmark_group(level, data_path)

    if subcategories:
        data = benchmark.get_data_by_subcategories(subcategories)
        print(f"📋 Subcategories: {subcategories}")
    else:
        data = benchmark.get_data_by_subcategories("all")
        print("📋 Subcategories: all")

    print(f"📊 Total data items: {len(data)}")

    print("\n⚙️ Getting evaluator...")
    evaluator = get_evaluator(level)

    print("\n🔄 Running evaluation...")
    results = evaluator.evaluate(
        data_items=data,
        model=model,
        max_out_len=max_out_len,
        save_path=save_path,
    )

    return results
