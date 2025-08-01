# import swanlab
from spectrumlab.models import GPT4_1
from spectrumlab.benchmark.signal_group import SignalGroup
from spectrumlab.benchmark.generation_group import GenerationGroup
from spectrumlab.benchmark.perception_group import PerceptionGroup
from spectrumlab.benchmark.semantic_group import SemanticGroup
from spectrumlab.evaluator.choice_evaluator import ChoiceEvaluator
from spectrumlab.evaluator.open_evaluator import OpenEvaluator

# export your swanlab api-key

# Change your model!
# MODEL = GPT4o()
MODEL = GPT4_1()


# Change this!!! such as gpt-4o_evaluation_results
SAVE_DIR = "./gpt4_1_generation_evaluation_results"

# 定义每个 Group 及其子任务和评测器
GROUPS = [
    {
        "name": "Signal",
        "group": SignalGroup("data"),
        "evaluator": ChoiceEvaluator(),
        "subcategories": None,  # None 表示全部
    },
    {
        "name": "Perception",
        "group": PerceptionGroup("data"),
        "evaluator": ChoiceEvaluator(),
        "subcategories": None,
    },
    {
        "name": "Semantic",
        "group": SemanticGroup("data"),
        "evaluator": ChoiceEvaluator(),
        "subcategories": None,
    },
    {
        "name": "Generation",
        "group": GenerationGroup("data"),
        "evaluator": OpenEvaluator(),
        "subcategories": None,
    },
]

# Change the experiment_name to your model name!!!
# swanlab.init(
#     workspace="SpectrumLab",
#     project="spectrumlab-eval",
#     experiment_name="gpt_4_1_generation_evaluation_results",
#     config={"model": MODEL.model_name},
# )

for group_info in GROUPS:
    name = group_info["name"]
    group = group_info["group"]
    evaluator = group_info["evaluator"]
    subcategories = group_info["subcategories"]
    print(f"\n===== Evaluating {name} Group =====")
    data = group.get_data_by_subcategories(subcategories or "all")
    results = evaluator.evaluate(data_items=data, model=MODEL, save_path=SAVE_DIR)
    accuracy = results["metrics"]["overall"]["accuracy"]
    print(f"{name} Group evaluation completed! Overall accuracy: {accuracy:.2f}%\n")
    # swanlab.log({f"{name}_accuracy": accuracy})

# swanlab.finish()

# use nohup in the terminal to start the evaluation
# nohup python run_evaluation.py > run_eval.log 2>&1 &
