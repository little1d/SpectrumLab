from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from pathlib import Path
import json
from datetime import datetime
from tqdm import tqdm


class BaseEvaluator(ABC):
    def __init__(self, prediction_key: str = "model_prediction"):
        self.prediction_key = prediction_key

    @abstractmethod
    def _build_prompt(self, item: Dict) -> str:
        pass

    @abstractmethod
    def _extract_prediction(self, response: str, item: Dict) -> str:
        pass

    @abstractmethod
    def _calculate_accuracy(self, answer: str, prediction: str, item: Dict) -> bool:
        pass

    def evaluate(
        self,
        data_items: List[Dict],
        model,
        max_out_len: int = 512,
        batch_size: Optional[int] = None,
        save_path: str = "./eval_results",
    ) -> Dict:
        if not data_items:
            print("❌ No data items provided")
            return {"error": "No data items provided"}

        print(f"🔄 Starting evaluation on {len(data_items)} items...")
        print(f"📝 Model: {type(model).__name__}")

        # 1. Build prompts
        print("📝 Building prompts...")
        prompts = [self._build_prompt(item) for item in data_items]

        # 2. Run model inference
        print("🚀 Running model inference...")
        responses = []
        try:
            # 统一使用sequential generation with progress bar
            for i, prompt in enumerate(
                tqdm(prompts, desc="Generating responses", unit="item")
            ):
                try:
                    response = model.generate(prompt, max_out_len)
                    responses.append(response)
                except Exception as e:
                    print(f"\n⚠️  Error on item {i + 1}: {e}")
                    responses.append(f"Error: {str(e)}")

        except Exception as e:
            return {"error": f"Model generation failed: {e}"}

        # 3. Extract predictions and add to data
        print("🔍 Extracting predictions...")
        processed_items = []
        for item, response in tqdm(
            zip(data_items, responses),
            desc="Processing responses",
            total=len(data_items),
            unit="item",
        ):
            item_copy = item.copy()
            prediction = self._extract_prediction(response, item)
            item_copy[self.prediction_key] = prediction
            item_copy["model_response"] = response

            answer = item.get("answer", "")
            is_correct = self._calculate_accuracy(answer, prediction, item)
            item_copy["pass"] = is_correct

            processed_items.append(item_copy)

        # 4. Save results
        saved_files = self._save_results(processed_items, save_path)
        print(f"💾 Results saved to: {saved_files}")

        # 5. Calculate metrics
        print("📊 Calculating metrics...")
        metrics = self._calculate_metrics(processed_items)

        # 6. Print results
        self._print_results(metrics)

        return {
            "metrics": metrics,
            "saved_files": saved_files,
            "total_items": len(data_items),
        }

    def evaluate_many():
        # TODO
        pass

    def _save_results(self, results_data: List[Dict], save_path: str) -> List[str]:
        """Save results grouped by subcategory."""
        if not results_data:
            return []

        save_dir = Path(save_path)
        save_dir.mkdir(parents=True, exist_ok=True)

        # Group by subcategory
        subcategory_data = {}
        for item in results_data:
            sub_category = item.get("sub_category", "Unknown")
            if sub_category not in subcategory_data:
                subcategory_data[sub_category] = []
            subcategory_data[sub_category].append(item)

        # Save each subcategory
        saved_files = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for sub_category, data_list in subcategory_data.items():
            safe_name = sub_category.replace(" ", "_").replace("/", "_")
            filename = f"{safe_name}_{timestamp}.json"
            filepath = save_dir / filename

            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data_list, f, indent=2, ensure_ascii=False)
                saved_files.append(str(filepath))
                print(f"  ✅ Saved {len(data_list)} items to {filename}")
            except Exception as e:
                print(f"❌ Failed to save {sub_category}: {e}")

        return saved_files

    def _calculate_metrics(self, processed_items: List[Dict]) -> Dict:
        if not processed_items:
            return {}

        # Overall metrics
        total = len(processed_items)
        correct = 0
        no_prediction = 0

        # Category and subcategory metrics
        category_stats = {}
        subcategory_stats = {}

        for item in processed_items:
            prediction = item.get(self.prediction_key, "")
            category = item.get("category", "Unknown")
            sub_category = item.get("sub_category", "Unknown")

            # Check if prediction exists
            if not prediction or prediction.strip() == "":
                no_prediction += 1

            # Use the pre-calculated "pass" field
            is_correct = item.get("pass", False)
            if is_correct:
                correct += 1

            # Update category stats
            if category not in category_stats:
                category_stats[category] = {"correct": 0, "total": 0}
            category_stats[category]["total"] += 1
            if is_correct:
                category_stats[category]["correct"] += 1

            # Update subcategory stats
            if sub_category not in subcategory_stats:
                subcategory_stats[sub_category] = {"correct": 0, "total": 0}
            subcategory_stats[sub_category]["total"] += 1
            if is_correct:
                subcategory_stats[sub_category]["correct"] += 1

        # Calculate percentages
        overall_accuracy = (correct / total * 100) if total > 0 else 0

        for stats in category_stats.values():
            stats["accuracy"] = (
                (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
            )

        for stats in subcategory_stats.values():
            stats["accuracy"] = (
                (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
            )

        return {
            "overall": {
                "accuracy": overall_accuracy,
                "correct": correct,
                "total": total,
                "no_prediction_count": no_prediction,
            },
            "category_metrics": category_stats,
            "subcategory_metrics": subcategory_stats,
        }

    def _print_results(self, metrics: Dict):
        """Print evaluation results."""
        if not metrics:
            return

        print("\n" + "=" * 60)
        print("EVALUATION RESULTS")
        print("=" * 60)

        # Overall accuracy
        if "overall" in metrics:
            overall = metrics["overall"]
            print(
                f"Overall Accuracy: {overall['accuracy']:.2f}% ({overall['correct']}/{overall['total']})"
            )

        # Category-wise accuracy
        if "category_metrics" in metrics:
            print("\nCategory-wise Accuracy:")
            for category, stats in metrics["category_metrics"].items():
                print(
                    f"  {category}: {stats['accuracy']:.2f}% ({stats['correct']}/{stats['total']})"
                )

        # Sub-category-wise accuracy
        if "subcategory_metrics" in metrics:
            print("\nSub-category-wise Accuracy:")
            for subcat, stats in metrics["subcategory_metrics"].items():
                print(
                    f"  {subcat}: {stats['accuracy']:.2f}% ({stats['correct']}/{stats['total']})"
                )

        if "overall" in metrics and metrics["overall"]["no_prediction_count"] > 0:
            print(
                f"\n⚠️  No prediction count: {metrics['overall']['no_prediction_count']}"
            )

        print("=" * 60)
