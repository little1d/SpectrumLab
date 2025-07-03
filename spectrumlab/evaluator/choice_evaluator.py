import re
from typing import List, Dict
from .base import BaseEvaluator
from spectrumlab.utils.image_utils import (
    prepare_images_for_prompt,
    normalize_image_paths,
)


class ChoiceEvaluator(BaseEvaluator):
    def __init__(self, prediction_key: str = "model_prediction"):
        super().__init__(prediction_key)

    def _build_prompt(self, item: Dict) -> str:
        question = item.get("question", "")
        choices = item.get("choices", [])
        image_paths_field = item.get("image_path")

        # 构建选项文本
        option_lines = [f"{chr(65 + i)}. {choice}" for i, choice in enumerate(choices)]
        options_block = "\n".join(option_lines)

        text_parts = [
            f"Question: {question}",
            "",
            "Available options:",
            options_block,
            "",
            "Please think step by step and provide your reasoning.",
            "After your analysis, indicate your final choice by putting it in \\box{}.",
            "For example: \\box{Option A}",
            "",
            "Your response:",
        ]

        text_content = "\n".join(text_parts)

        # Check if there are images
        image_paths = normalize_image_paths(image_paths_field)

        if image_paths:
            # Prepare image data
            image_data = prepare_images_for_prompt(image_paths)

            if image_data:
                # Return multimodal format
                return {"text": text_content, "images": image_data}

        # Return pure text format
        return text_content

    def _extract_prediction(self, response: str, item: Dict) -> str:
        """Extract prediction from model response using \\box{} pattern."""
        if not response:
            return ""

        choices = item.get("choices", [])

        # Look for \\box{} pattern
        box_pattern = r"\\box\{([^}]+)\}"
        matches = re.findall(box_pattern, response)

        if matches:
            extracted = matches[-1].strip()
            # Try to match with actual choices
            for choice in choices:
                if choice.lower() == extracted.lower():
                    return choice
            return extracted

        return ""

    def _calculate_accuracy(self, answer: str, prediction: str, item: Dict) -> bool:
        """Calculate accuracy using string matching from MMAR."""
        choices = item.get("choices", [])
        return self._string_match(answer, prediction, choices)

    def _string_match(self, answer: str, prediction: str, choices: List[str]) -> bool:
        # Adapted from: MMAR
        # Source: https://github.com/ddlBoJack/MMAR/blob/main/code/evaluation.py#L8

        def tokenize(text):
            return set(re.findall(r"\b\w+\b", text.lower()))

        prediction_tokens = tokenize(prediction)
        answer_tokens = tokenize(answer)

        if not prediction_tokens:
            return False

        # Get tokens from incorrect choices
        incorrect_tokens = set()
        for choice in choices:
            choice_tokens = tokenize(choice)
            if choice_tokens != answer_tokens:
                incorrect_tokens.update(choice_tokens - answer_tokens)

        # Two conditions for correct match
        cond1 = answer_tokens.issubset(
            prediction_tokens
        )  # All answer tokens in prediction
        cond2 = prediction_tokens.isdisjoint(
            incorrect_tokens
        )  # No incorrect choice tokens

        return cond1 and cond2
