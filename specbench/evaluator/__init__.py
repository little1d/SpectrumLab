from .choice_evaluator import ChoiceEvaluator


def get_evaluator(level: str):
    """
    获取评估器
    目前所有level都使用ChoiceEvaluator，后续可以根据level返回不同的evaluator
    """
    return ChoiceEvaluator()
