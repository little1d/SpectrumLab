from spectrumlab.models import DeepSeek
from spectrumlab.utils.image_utils import encode_image_to_base64
from spectrumlab.benchmark.signal_group import SignalGroup
from spectrumlab.evaluator.choice_evaluator import ChoiceEvaluator


def test_deepseek_text_generation():
    model = DeepSeek()
    prompt = "What is spectroscopy?"
    response = model.generate(prompt)
    assert isinstance(response, str)
    assert len(response) > 0


def test_deepseek_multimodal_generation():
    model = DeepSeek()
    image_path = "playground/models/test.png"
    image_base64 = encode_image_to_base64(image_path)
    prompt = {
        "text": "Please explain this spectroscopy image.",
        "images": [
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{image_base64}"},
            }
        ],
    }
    response = model.generate(prompt)
    assert isinstance(response, str)
    assert len(response) > 0


def test_deepseek_signalgroup_evaluation():
    model = DeepSeek()
    signal_group = SignalGroup("data")
    data = signal_group.get_data_by_subcategories(["Spectrum Type Classification"])
    evaluator = ChoiceEvaluator()
    results = evaluator.evaluate(data_items=data, model=model, save_path=None)
    assert "metrics" in results
    assert "overall" in results["metrics"]
