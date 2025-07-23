from spectrumlab.models import DeepSeek_VL2
from spectrumlab.utils.image_utils import encode_image_to_base64
from spectrumlab.benchmark.signal_group import SignalGroup
from spectrumlab.evaluator.choice_evaluator import ChoiceEvaluator


def test_deepseek_vl_2_text_generation():
    model = DeepSeek_VL2()
    prompt = "What is spectroscopy?"
    response = model.generate(prompt)
    assert isinstance(response, str)
    assert len(response) > 0


def test_deepseek_vl_2_multimodal_generation():
    model = DeepSeek_VL2()
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


def test_deepseek_vl_2_signalgroup_evaluation():
    model = DeepSeek_VL2()
    signal_group = SignalGroup("data")
    data = signal_group.get_data_by_subcategories(["Spectrum Type Classification"])
    evaluator = ChoiceEvaluator()
    results = evaluator.evaluate(data_items=data, model=model, save_path=None)
    assert "metrics" in results
    assert "overall" in results["metrics"]


def test_deepseek_vl_2_signalgroup_evaluation_parallel():
    model = DeepSeek_VL2()
    signal_group = SignalGroup("data")
    data = signal_group.get_data_by_subcategories(["Spectrum Type Classification"])
    evaluator = ChoiceEvaluator()
    results = evaluator.evaluate_many(data_items=data, model=model, save_path=None)
    assert "metrics" in results
    assert "overall" in results["metrics"]