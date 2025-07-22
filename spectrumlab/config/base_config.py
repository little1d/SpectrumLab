import os
from dataclasses import dataclass
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root directory
project_root = Path(__file__).parent.parent.parent
env_path = project_root / ".env"
print(env_path)
load_dotenv(env_path)


@dataclass
class Config:
    # This api key is for testing closed MLLMs by Boyue Richdata
    BOYUE_API_KEY: str = os.getenv("BOYUE_API_KEY")
    BOYUE_BASE_URL: str = os.getenv("BOYUE_BASE_URL")
    
    # DeepSeek API Configuration
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY")
    deepseek_base_url: str = os.getenv("DEEPSEEK_BASE_URL")
    deepseek_model_name: str = os.getenv("DEEPSEEK_MODEL_NAME")

    # GPT-4o API Configuration
    gpt4o_api_key: str = os.getenv("GPT4O_API_KEY")
    gpt4o_base_url: str = os.getenv("GPT4O_BASE_URL")
    gpt4o_model_name: str = os.getenv("GPT4O_MODEL_NAME")

    # InternVL API Configuration
    internvl_api_key: str = os.getenv("INTERNVL_API_KEY")
    internvl_base_url: str = os.getenv("INTERNVL_BASE_URL")
    internvl_model_name: str = os.getenv("INTERNVL_MODEL_NAME")

    # Claude API Configuration
    claude_api_key: str = BOYUE_API_KEY
    claude_base_url: str = BOYUE_BASE_URL
    claude_sonnet_3_5_model_name: str = os.getenv("CLAUDE_SONNET_3_5")
    claude_opus_4_model_name: str = os.getenv("CLAUDE_OPUS_4")
    claude_haiku_3_5_model_name: str = os.getenv("CLAUDE_HAIKU_3_5")
    claude_sonnet_4_model_name: str = os.getenv("CLAUDE_SONNET_4")

    # GPT-4.1, GPT-4-Vision
    gpt4_1_api_key: str = BOYUE_API_KEY
    gpt4_1_base_url: str = BOYUE_BASE_URL
    gpt4_1_model_name: str = os.getenv("GPT4_1")
    gpt4_vision_api_key: str = BOYUE_API_KEY
    gpt4_vision_base_url: str = BOYUE_BASE_URL
    gpt4_vision_model_name: str = os.getenv("GPT4_VISION")
    
    # Grok-2-Vision
    grok_2_vision_api_key: str = BOYUE_API_KEY
    grok_2_vision_base_url: str = BOYUE_BASE_URL
    grok_2_vision_model_name: str = os.getenv("GROK_2_VISION")
    
    # Gemini-2.5-Pro
    gemini_2_5_pro_api_key: str = BOYUE_API_KEY
    gemini_2_5_pro_base_url: str = BOYUE_BASE_URL
    gemini_2_5_pro_model_name: str = os.getenv("GEMINI_2_5_PRO")
    
    # Qwen-VL-Max 
    qwen_vl_api_key: str = BOYUE_API_KEY
    qwen_vl_base_url: str = BOYUE_BASE_URL
    qwen_vl_model_name: str = os.getenv("QWEN_VL")
    
