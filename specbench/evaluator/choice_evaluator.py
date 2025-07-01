import re
from typing import List, Dict
from .base import BaseEvaluator


class ChoiceEvaluator(BaseEvaluator):
    """选择题评估器"""

    def __init__(self, prediction_key: str = "prediction"):
        super().__init__()
        self.prediction_key = prediction_key

    def _build_prompt(self, item: Dict) -> str:
        """构建prompt"""
        question = item.get("question", "")
        choices = item.get("choices", [])

        prompt = f"Question: {question}\n\n"
        prompt += "Please choose the correct answer from the following options:\n"

        for i, choice in enumerate(choices):
            prompt += f"{chr(65+i)}. {choice}\n"

        prompt += "\nAnswer: "
        return prompt

    def _extract_prediction(self, response: str, item: Dict) -> str:
        """从模型响应中提取预测结果"""
        if not response:
            return ""

        response = response.strip()
        choices = item.get("choices", [])

        # 方法1: 查找选择标识符 (A, B, C, D)
        choice_pattern = r"\b([A-D])\b"
        matches = re.findall(choice_pattern, response.upper())
        if matches:
            choice_idx = ord(matches[0]) - ord("A")
            if 0 <= choice_idx < len(choices):
                return choices[choice_idx]

        # 方法2: 直接在choices中查找匹配
        for choice in choices:
            if choice.lower() in response.lower():
                return choice

        # 方法3: 返回原始响应的前50个字符
        return response[:50]

    def _calculate_metrics(self, data_with_predictions: List[Dict]) -> Dict:
        """计算评估指标"""
        if not data_with_predictions:
            return self._empty_result()

        # 初始化统计变量
        correct_total = 0
        total_count = len(data_with_predictions)
        no_prediction_count = 0

        # 分类统计
        category_metrics = {}
        subcat_metrics = {}

        # 详细结果
        detailed_results = []
        matched_outputs = []

        # 逐个评估
        for idx, sample in enumerate(data_with_predictions):
            prediction = sample.get(self.prediction_key, "")
            if not prediction:
                no_prediction_count += 1

            answer = sample.get("answer", "")
            choices = sample.get("choices", [])
            category = sample.get("category", "Unknown")
            sub_category = sample.get("sub_category", "Unknown")

            # 初始化分类统计
            if category not in category_metrics:
                category_metrics[category] = [0, 0]
            if sub_category not in subcat_metrics:
                subcat_metrics[sub_category] = [0, 0]

            # 使用string_match评估
            is_correct = self.string_match(answer, prediction, choices)

            # 更新统计
            if is_correct:
                correct_total += 1
                category_metrics[category][0] += 1
                subcat_metrics[sub_category][0] += 1
                matched_outputs.append([answer, prediction])

            category_metrics[category][1] += 1
            subcat_metrics[sub_category][1] += 1

            # 记录详细结果
            detailed_results.append(
                {
                    "id": sample.get("id", f"item_{idx}"),
                    "question": sample.get("question", ""),
                    "choices": choices,
                    "answer": answer,
                    "prediction": prediction,
                    "model_response": sample.get("model_response", ""),
                    "is_correct": is_correct,
                    "category": category,
                    "sub_category": sub_category,
                }
            )

        # 构建结果
        results = {
            "overall": {
                "accuracy": self._calculate_accuracy(correct_total, total_count),
                "correct": correct_total,
                "total": total_count,
            },
            "category_metrics": self._format_metrics(category_metrics),
            "subcat_metrics": self._format_metrics(subcat_metrics),
            "no_prediction_count": no_prediction_count,
            "matched_outputs": matched_outputs,
            "detailed_results": detailed_results,
        }

        return results

    def string_match(self, answer: str, prediction: str, choices: List[str]) -> bool:
        """基于token匹配的字符串比较逻辑"""

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

    def _format_metrics(self, metrics_dict: Dict) -> Dict:
        """格式化指标"""
        result = {}
        for key, (correct, total) in metrics_dict.items():
            result[key] = {
                "accuracy": self._calculate_accuracy(correct, total),
                "correct": correct,
                "total": total,
            }
        return result

    def _empty_result(self) -> Dict:
        """返回空结果"""
        return {
            "overall": {"accuracy": 0.0, "correct": 0, "total": 0},
            "category_metrics": {},
            "subcat_metrics": {},
            "no_prediction_count": 0,
            "matched_outputs": [],
            "detailed_results": [],
        }
