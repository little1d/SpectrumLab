import re
from typing import List, Dict
from .base import BaseEvaluator


class ChoiceEvaluator(BaseEvaluator):
    def __init__(self, prediction_key: str = "model_prediction"):
        super().__init__(prediction_key)

    def _build_prompt(self, item: Dict) -> str:
        # TODO: for question contains images, we need to
        """Build prompt for choice question."""
        question = item.get("question", "")
        choices = item.get("choices", [])

        # Build options
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
            "Your response:",
        ]

        return "\n".join(prompt_parts)

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
