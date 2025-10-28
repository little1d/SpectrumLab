from spectrumlab.models import Qwen_2_5_VL_72B
from spectrumlab.utils.image_utils import encode_image_to_base64
from spectrumlab.benchmark.signal_group import SignalGroup
from spectrumlab.evaluator.choice_evaluator import ChoiceEvaluator


def test_qwen_2_5_vl_72b_text_generation():
    model = Qwen_2_5_VL_72B()
    prompt = "What is spectroscopy?"
    response = model.generate(prompt)
    assert isinstance(response, str)
    assert len(response) > 0


def test_qwen_2_5_vl_72b_multimodal_generation():
    model = Qwen_2_5_VL_72B()
    image_path = "playground/models/test.jpg"
    image_base64 = encode_image_to_base64(image_path)
    prompt = {
        "text": "Please explain this spectroscopy image.",
        "images": [
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpg;base64,{image_base64}"},
            }
        ],
    }
    response = model.generate(prompt)
    assert isinstance(response, str)
    assert len(response) > 0


def test_qwen_2_5_vl_72b_signalgroup_evaluation():
    model = Qwen_2_5_VL_72B()
    signal_group = SignalGroup("data")
    data = signal_group.get_data_by_subcategories(["Spectrum Type Classification"])
    evaluator = ChoiceEvaluator()
    results = evaluator.evaluate(data_items=data, model=model, save_path=None)
    assert "metrics" in results
    assert "overall" in results["metrics"]


def test_qwen_2_5_vl_72b_signalgroup_evaluation_parallel():
    model = Qwen_2_5_VL_72B()
    signal_group = SignalGroup("data")
    data = signal_group.get_data_by_subcategories(["Spectrum Type Classification"])
    evaluator = ChoiceEvaluator()
    results = evaluator.evaluate_many(data_items=data, model=model, save_path=None)
    assert "metrics" in results
    assert "overall" in results["metrics"]
