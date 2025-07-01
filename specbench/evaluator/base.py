from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseEvaluator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def _build_prompt(self, item: Dict) -> str:
        pass

    @abstractmethod
    def _extract_prection(self, response: str, item: Dict) -> str:
        pass

    @abstractmethod
    def _calculate_metrics(self, data_with_predictions: List[Dict]) -> Dict:
        pass

    @abstractmethod
    def evaluate(
        self,
        data_items: List[Dict],
        model,
        max_out_len: int = 512,
        batch_size: Optional[int] = None,
        save_dict: bool = False,
        save_path: str = "./eval_results",
    ) -> Dict:
        if not data_items:
            print("❌ No data items provided")
            return ""

        print(f"🔄 Starting evaluation on {len(data_items)} items...")
        print(f"Model: {repr(model)}")

        # 1. build prompts
        print(f"📝  Building prmopts...")
        prompts = [self._build_prompt(item) for item in data_items]

        # 2. run model inference
        print(f"🚀 Running model inference...")
        try:
            responses = model.generate(prompts, max_out_len)
        except Exception as e:
            return {"error": f"Model generation failed: {e}"}

        # 3. extract predictions
        print(f"📝  Extracting predictions...")
        model_predictions = []
        for item, response in zip(data_items, responses):
            item_copy = item.copy()
            prediction = self._extract_prection(response, item)
            item_copy[self.prediction_key] = prediction
            # item_copy["model_response"] = response # original response
            model_predictions.append(item_copy)

        # 4. save results
        save_file = self._save_results(model_predictions, save_path)
        print(f"💾 Results saved to {save_file}")

        # 5. calculate metrics
        print(f"🔄 Calculating metrics...")
        results = self.calculate_metrics(model_predictions)

        return results

    def evaluate_many():
        # TODO
        pass

    def _save_results(self, results: Dict, save_path: str, suffix: str = ""):
        pass

    def _print_results(self, results: Dict):
        # TODO
        # print("\n" + "=" * 60)
        # print("EVALUATION RESULTS")
        # print("=" * 60)

        # # 总体准确率
        # if "overall" in results:
        #     overall = results["overall"]
        #     print(
        #         f"Overall Accuracy: {overall['accuracy']:.2f}% ({overall['correct']}/{overall['total']})"
        #     )

        # # Category-wise accuracy
        # if "category_metrics" in results:
        #     print("\nCategory-wise Accuracy:")
        #     for category, metrics in results["category_metrics"].items():
        #         print(
        #             f"  {category}: {metrics['accuracy']:.2f}% ({metrics['correct']}/{metrics['total']})"
        #         )

        # # Sub-category-wise accuracy
        # if "subcat_metrics" in results:
        #     print("\nSub-category-wise Accuracy:")
        #     for subcat, metrics in results["subcat_metrics"].items():
        #         print(
        #             f"  {subcat}: {metrics['accuracy']:.2f}% ({metrics['correct']}/{metrics['total']})"
        #         )

        # if "no_prediction_count" in results and results["no_prediction_count"] > 0:
        #     print(f"\n⚠️  No prediction count: {results['no_prediction_count']}")

        # print("=" * 60)
        pass
