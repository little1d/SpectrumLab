import os
from dataclasses import dataclass
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root directory
project_root = Path(__file__).parent.parent.parent
env_path = project_root / ".env"
load_dotenv(env_path)


@dataclass
class Config:
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
