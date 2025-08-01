#!/usr/bin/env python3
"""
Simplified Leaderboard Management for SpectrumLab
Core functionality for batch import operations
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import statistics


class LeaderboardManager:
    def __init__(self, leaderboard_path: str = "leaderboard/leaderboard_v_1.0.json"):
        self.leaderboard_path = Path(leaderboard_path)
        self.data = self._load_leaderboard()

    def _load_leaderboard(self) -> Dict[str, Any]:
        """Load leaderboard data from JSON file"""
        if self.leaderboard_path.exists():
            try:
                with open(self.leaderboard_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if not content:  # File is empty
                        return {"leaderboard_info": {"total_models": 0}, "models": []}
                    return json.loads(content)
            except (json.JSONDecodeError, ValueError) as e:
                print(
                    f"Warning: Invalid JSON in {self.leaderboard_path}. Creating new leaderboard. Error: {e}"
                )
                return {"leaderboard_info": {"total_models": 0}, "models": []}
        else:
            return {"leaderboard_info": {"total_models": 0}, "models": []}

    def _save_leaderboard(self):
        """Save leaderboard data to JSON file"""
        # Ensure directory exists
        self.leaderboard_path.parent.mkdir(parents=True, exist_ok=True)

        # Update total_models count
        self.data["leaderboard_info"]["total_models"] = len(self.data["models"])

        # Sort models by overall accuracy (descending)
        self.data["models"].sort(
            key=lambda x: x["results"].get("overall_accuracy", 0), reverse=True
        )

        with open(self.leaderboard_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def _calculate_category_accuracy(
        self, category_results: Dict[str, Any]
    ) -> Optional[float]:
        """Calculate category accuracy from subcategories"""
        subcategories = category_results.get("subcategories", {})
        valid_scores = []

        for subcat_name, subcat_data in subcategories.items():
            accuracy = subcat_data.get("accuracy")
            if accuracy is not None:
                valid_scores.append(accuracy)

        return round(statistics.mean(valid_scores), 2) if valid_scores else None

    def _calculate_overall_accuracy(self, results: Dict[str, Any]) -> Optional[float]:
        """Calculate overall accuracy from all categories"""
        category_scores = []

        for category in ["Signal", "Perception", "Semantic", "Generation"]:
            if category in results:
                category_accuracy = results[category].get("accuracy")
                if category_accuracy is not None:
                    category_scores.append(category_accuracy)

        return round(statistics.mean(category_scores), 2) if category_scores else None

    def _recalculate_model_scores(self, model: Dict[str, Any]):
        """Recalculate all accuracy scores for a model"""
        results = model["results"]

        # Calculate category accuracies
        for category in ["Signal", "Perception", "Semantic", "Generation"]:
            if category in results:
                calculated_accuracy = self._calculate_category_accuracy(
                    results[category]
                )
                if calculated_accuracy is not None:
                    results[category]["accuracy"] = calculated_accuracy

        # Calculate overall accuracy
        overall_accuracy = self._calculate_overall_accuracy(results)
        if overall_accuracy is not None:
            results["overall_accuracy"] = overall_accuracy

    def find_model(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Find a model by name"""
        for model in self.data["models"]:
            if model["name"] == model_name:
                return model
        return None

    def add_model(
        self,
        model_info: Dict[str, Any],
        subcategory_scores: Dict[str, Dict[str, float]],
    ):
        """Add a new model to the leaderboard"""
        # Check if model already exists
        existing_model = self.find_model(model_info["name"])
        if existing_model:
            print(f"Model '{model_info['name']}' already exists. Skipping...")
            return False

        # Create model entry
        model_entry = {
            "name": model_info["name"],
            "name_link": model_info.get("name_link", ""),
            "submitter": model_info.get("submitter", ""),
            "submitter_link": model_info.get("submitter_link", ""),
            "submission_time": datetime.now().isoformat() + "Z",
            "model_type": model_info.get("model_type", "unknown"),
            "model_size": model_info.get("model_size", "Unknown"),
            "is_multimodal": model_info.get("is_multimodal", False),
            "results": {},
            "model_info": {
                "homepage": model_info.get("homepage", ""),
                "paper": model_info.get("paper", ""),
                "code": model_info.get("code", ""),
                "description": model_info.get("description", ""),
            },
        }

        # Add subcategory scores
        for category, subcats in subcategory_scores.items():
            model_entry["results"][category] = {
                "accuracy": None,  # Will be calculated
                "subcategories": {},
            }

            for subcat, accuracy in subcats.items():
                model_entry["results"][category]["subcategories"][subcat] = {
                    "accuracy": accuracy if accuracy is not None else None
                }

        # Calculate derived scores
        self._recalculate_model_scores(model_entry)

        # Add to leaderboard
        self.data["models"].append(model_entry)
        self._save_leaderboard()

        print(f"✅ Successfully added model '{model_info['name']}' to leaderboard")
        return True
