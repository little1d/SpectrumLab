import re
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from .base import BaseEvaluator


class ChoiceEvaluator(BaseEvaluator):
    def __init__(self, prediction_key: str = "model_prediction"):
        super().__init__()
        self.prediction_key = prediction_key

    def _build_prompt(self, item: Dict) -> str:
        question = item.get("question", "")
        choices = item.get("choices", [])

        # 构建选项部分
        option_lines = [f"{chr(65 + i)}. {choice}" for i, choice in enumerate(choices)]
        options_block = "\n".join(option_lines)

        prompt_parts = [
            f"Question: {question}",
            "",
            "Available options:",
            options_block,
            "",
            "Please think step by step and provide your reasoning.",
            "After your analysis, indicate your final choice by putting it in \\box{}.",
            "For example: \\box{Option A}",
            "",
            "Your response: ",
        ]

        prompt = "\n".join(prompt_parts)
        return prompt

    def _extract_prediction(self, response: str, item: Dict) -> str:
        if not response:
            return ""

        choices = item.get("choices", [])
        box_pattern = r"\\box\{([^}]+)\}"
        matches = re.findall(box_pattern, response)

        if matches:
            extracted = matches[-1].strip()
            for choice in choices:
                if choice.lower() == extracted.lower():
                    return choice
            return extracted
        return ""

    def evaluate(
        self,
        data_items: List[Dict],
        model,
        max_out_len: int = 512,
        batch_size: int = None,
        save_path: str = "./eval_results",
    ) -> str:
        if not data_items:
            print("❌ No data items provided")
            return []

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
        print(f"🔍 Extracting predictions and grouping by subcategory...")
        subcategory_data = {}

        for item, response in zip(data_items, responses):
            item_copy = item.copy()
            prediction = self._extract_prediction(response, item)
            item_copy[self.prediction_key] = prediction

            sub_category = item.get("sub_category", "Unknown")
            if sub_category not in subcategory_data:
                subcategory_data[sub_category] = []
            subcategory_data[sub_category].append(item_copy)

        # 4. save results
        saved_files = []
        for sub_category, data_list in subcategory_data.items():
            file_path = self._save_results(data_list, save_path, sub_category)
            if file_path:
                saved_files.append(file_path)

        print(f"💾 Saved {len(saved_files)} result files:")
        for file_path in saved_files:
            print(f"  - {file_path}")

        # 5. calculate metrics
        print(f"🔄 Calculating metrics...")
        results = self._calculate_metrics(saved_files)

        print(f"✅ Evaluation completed!")

        return results

    def _save_results(
        self, results_data: List[Dict], save_path: str, sub_category: str
    ) -> str:
        if not results_data:
            print("❌ No results data provided")
            return ""
        save_dir = Path(save_path)
        save_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_sub_category = sub_category.replace(" ", "_").replace("/", "_")
        filename = f"{safe_sub_category}_{timestamp}.json"
        filepath = save_dir / filename

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(results_data, f, indent=2, ensure_ascii=False)
            return str(filepath)
        except Exception as e:
            print(f"❌ Failed to save results for {sub_category}: {e}")
            return ""

    def calculate_metrics(self, results_file: List[str]) -> Dict:
        try:
            with open(results_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"❌ Failed to load results: {e}")
            return {}

        if not data:
            return {"error": "No data founded"}

        print(f"🔄 Calculating metrics from {len(data)} items...")

        total = len(data)
        correct = 0
        no_prediction = 0

        # 详细结果
        detailed_results = []

        for item in data:
            answer = item.get("answer", "")
            prediction = item.get(self.prediction_key, "")
            choices = item.get("choices", [])

            if not prediction:
                no_prediction += 1

            is_correct = self.string_match(answer, prediction, choices)
            if is_correct:
                correct += 1

            detailed_results.append(
                {
                    "id": item.get("id", ""),
                    "question": item.get("question", "")[:50] + "...",
                    "answer": answer,
                    "prediction": prediction,
                    "is_correct": is_correct,
                }
            )

        accuracy = (correct / total * 100) if total > 0 else 0

        results = {
            "file": results_file,
            "sub_category": (
                data[0].get("sub_category", "Unknown") if data else "Unknown"
            ),
            "accuracy": accuracy,
            "correct": correct,
            "total": total,
            "no_prediction_count": no_prediction,
            "detailed_results": detailed_results,
        }

        # 打印结果
        self._print_metrics(results)

        return results

    # Adapted from: MMAR
    # Source: https://github.com/ddlBoJack/MMAR/blob/main/code/evaluation.py#L8
    def string_match(self, answer: str, prediction: str, choices: List[str]) -> bool:

        def tokenize(text):
            return set(re.findall(r"\b\w+\b", text.lower()))

        prediction_tokens = tokenize(prediction)
        answer_tokens = tokenize(answer)

        if not prediction_tokens:
            return False

        incorrect_tokens = set()
        for choice in choices:
            choice_tokens = tokenize(choice)
            if choice_tokens != answer_tokens:
                incorrect_tokens.update(choice_tokens - answer_tokens)

        cond1 = answer_tokens.issubset(prediction_tokens)
        cond2 = prediction_tokens.isdisjoint(incorrect_tokens)

        return cond1 and cond2

    def _print_metrics(self, results: Dict):
        print("\n" + "=" * 50)
        print(f"METRICS for {results['sub_category']}")
        print("=" * 50)
        print(f"File: {Path(results['file']).name}")
        print(
            f"Accuracy: {results['accuracy']:.2f}% ({results['correct']}/{results['total']})"
        )
        if results["no_prediction_count"] > 0:
            print(f"⚠️  No prediction: {results['no_prediction_count']} items")
        print("=" * 50)
