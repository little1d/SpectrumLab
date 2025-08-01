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

        option_lines = [f"{chr(65 + i)}. {choice}" for i, choice in enumerate(choices)]
        options_block = "\n".join(option_lines)

        text_parts = [
            f"Question: {question}",
            "",
            "Available options:",
            options_block,
            "",
            "Please analyze the question and options carefully. Your answer must be exactly one of the provided options, and must be copied verbatim from the options above.",
            "Return your answer using the format \\answer{...}, where the content inside the braces is exactly the text of your chosen option (not the option letter or number, and do not use \\box{} or any other wrapper).",
            "For example, if you choose the option '~1700 cm⁻¹', you should return: \\answer{~1700 cm⁻¹}",
            "Do not return just a value like '~1700 cm' or any partial/incomplete answer. The answer must match one of the options exactly.",
            "",
            "Your response:",
        ]

        text_content = "\n".join(text_parts)

        # Check if there are images
        image_paths = normalize_image_paths(image_paths_field)

        if image_paths:
            assert all(
                isinstance(p, str) for p in image_paths
            ), f"image_paths should be List[str], got {image_paths}"
            # Prepare image data
            image_data = prepare_images_for_prompt(image_paths)

            if image_data:
                # Return multimodal format
                return {"text": text_content, "images": image_data}

        # Return pure text format
        return text_content

    def _extract_prediction(self, response: str, item: Dict) -> str:
        """只提取 \\answer{...} 内的内容"""
        if not response:
            return ""
        answer_pattern = r"\\answer\{([^}]+)\}"
        matches = re.findall(answer_pattern, response)
        if matches:
            return matches[-1].strip()
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
