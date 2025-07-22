from spectrumlab.models import Gemini_2_5_Pro
from spectrumlab.utils.image_utils import encode_image_to_base64
from spectrumlab.benchmark.signal_group import SignalGroup
from spectrumlab.evaluator.choice_evaluator import ChoiceEvaluator


def test_claude_text_generation():
    model = Gemini_2_5_Pro()
    prompt = "What is spectroscopy?"
    response = model.generate(prompt, 8192)
    assert isinstance(response, str)
    assert len(response) > 0


def test_claude_multimodal_generation():
    model = Gemini_2_5_Pro()
    image_path = "playground/models/test.jpg"
    image_base64 = encode_image_to_base64(image_path)
    prompt = {
        "text": "Please explain this spectroscopy image.",
        "images": [
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpg;base64, {image_base64}"},
            }
        ],
    }
    response = model.generate(prompt, 8192)
    assert isinstance(response, str)
    assert len(response) > 0


def test_claude_signalgroup_evaluation():
    model = Gemini_2_5_Pro()
    signal_group = SignalGroup("data")
    data = signal_group.get_data_by_subcategories(["Spectrum Type Classification"])
    evaluator = ChoiceEvaluator()
    results = evaluator.evaluate(data_items=data, model=model, save_path=None, max_out_len=8192)
    assert "metrics" in results
    assert "overall" in results["metrics"]
