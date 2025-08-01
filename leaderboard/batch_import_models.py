#!/usr/bin/env python3
"""
Batch import models to leaderboard
Usage: python batch_import_models.py models_data.json
"""

import json
import sys
from pathlib import Path

# Add the leaderboard directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from manage_leaderboard import LeaderboardManager


def batch_import(models_file: str):
    """Batch import models from JSON file"""

    with open(models_file, "r", encoding="utf-8") as f:
        models_data = json.load(f)

    manager = LeaderboardManager()

    # Clear existing models if specified
    if models_data.get("clear_existing", False):
        print("🗑️ Clearing existing models...")
        manager.data["models"] = []

    # Import models
    imported_count = 0
    for model_data in models_data["models"]:
        model_info = model_data["model_info"]
        subcategory_scores = model_data["scores"]

        success = manager.add_model(model_info, subcategory_scores)
        if success:
            imported_count += 1

    print(
        f"\n✅ Successfully imported {imported_count}/{len(models_data['models'])} models"
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python batch_import_models.py models_data.json")
        sys.exit(1)

    batch_import(sys.argv[1])
