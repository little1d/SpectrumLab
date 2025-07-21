from spectrumlab.models import DeepSeek


def test_deepseek_text_generation():
    model = DeepSeek()
    prompt = "What is spectroscopy?"
    response = model.generate(prompt)
    assert isinstance(response, str)
    assert len(response) > 0
