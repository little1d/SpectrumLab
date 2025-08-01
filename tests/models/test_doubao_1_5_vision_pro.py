from spectrumlab.models import Doubao_1_5_Vision_Pro
from spectrumlab.utils.image_utils import encode_image_to_base64
from spectrumlab.benchmark.signal_group import SignalGroup
from spectrumlab.evaluator.choice_evaluator import ChoiceEvaluator


def test_doubao_1_5_vision_pro_text_generation():
    model = Doubao_1_5_Vision_Pro()
    prompt = "What is spectroscopy?"
    response = model.generate(prompt)
    assert isinstance(response, str)
    assert len(response) > 0


def test_doubao_1_5_vision_pro_multimodal_generation():
    model = Doubao_1_5_Vision_Pro()
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


def test_doubao_1_5_vision_pro_signalgroup_evaluation():
    model = Doubao_1_5_Vision_Pro()
    signal_group = SignalGroup("data")
    data = signal_group.get_data_by_subcategories(["Spectrum Type Classification"])
    evaluator = ChoiceEvaluator()
    results = evaluator.evaluate(data_items=data, model=model, save_path=None)
    assert "metrics" in results
    assert "overall" in results["metrics"]


def test_doubao_1_5_vision_pro_signalgroup_evaluation_parallel():
    model = Doubao_1_5_Vision_Pro()
    signal_group = SignalGroup("data")
    data = signal_group.get_data_by_subcategories(["Spectrum Type Classification"])
    evaluator = ChoiceEvaluator()
    results = evaluator.evaluate_many(data_items=data, model=model, save_path=None)
    assert "metrics" in results
    assert "overall" in results["metrics"]
    