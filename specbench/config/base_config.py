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
    deepseek_base_url: str = os.getenv(
        "DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"
    )
    deepseek_model_name: str = os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-chat")
