from abc import ABC
from pathlib import Path
from typing import List, Dict, Union
import json


class BaseGroup(ABC):
    def __init__(self, level: str, path: str = "./data"):
        self.level = level
        self.data_root = Path(path).resolve()
        self.path = self.data_root / self.level
        self.datasets = {}
        self._load_datasets()

    def _load_datasets(self):
        """
        Load benchmark datasets for the current level.
        """
        print(f"Loading datasets for level '{self.level}'...")
        print(f"Looking for local datasets in: {self.path}")

        if self.path.exists() and self.path.is_dir():
            print("✅ Local datasets found, loading...")
            self._load_from_local(self.path)
        else:
            print("❌ Local datasets not found, falling back to HuggingFace...")
            self._load_from_remote(self.path)

        print(
            f"📊 Total available sub-categories in '{self.level}' level: {len(self.datasets)}"
        )
        print(f"📋 Available sub-categories: {list(self.datasets.keys())}")

    def _load_from_local(self, level_path: Path):
        self.datasets = {}

        for sub_category_dir in level_path.iterdir():
            if not sub_category_dir.is_dir():
                continue
            sub_category_name = sub_category_dir.name
            json_filename = f"{sub_category_name.replace(' ', '_')}_datasets.json"
            json_file = sub_category_dir / json_filename

            if json_file.exists():
                try:
                    data = self._load_json(json_file)
                    if data:
                        self.datasets[sub_category_name] = data
                        print(
                            f"  ✔ Loaded {len(data)} items from '{sub_category_name}'"
                        )
                    else:
                        print(f"  ⚠ Empty data in '{sub_category_name}'")
                except Exception as e:
                    print(f"  ✖ Failed to load '{sub_category_name}': {e}")
            else:
                print(f"  ⚠ No {json_filename} found in '{sub_category_name}'")

    def _load_from_remote(self, local_level_path: Path):
        # TODO
        self.datasets = {}

    def _fix_image_path(self, image_path: str) -> str:
        if not image_path or not image_path.strip():
            return image_path
        if image_path.startswith("./data/"):
            relative_part = image_path[7:]
            corrected_path = self.data_root / relative_part
            return str(corrected_path)
        return image_path

    def _load_json(self, file_path: Path) -> List[Dict]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and "image_path" in item:
                            if item["image_path"]:
                                original_path = item["image_path"]
                                item["image_path"] = self._fix_image_path(original_path)

                    return data
                else:
                    print(f"Warning: Expected list in {file_path}, got {type(data)}")
                    return []
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON in {file_path}: {e}")
            return []
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return []

    def get_data_by_subcategories(
        self, subcategories: Union[str, List[str]] = "all"
    ) -> List[Dict]:
        if subcategories == "all":
            subcategories = self.get_available_subcategories()
            print(
                f"🔍 Selecting all available sub-categories ({len(subcategories)} total)"
            )
        elif isinstance(subcategories, str):
            subcategories = [subcategories]
            print(f"🔍 Selecting sub-category: '{subcategories[0]}'")
        else:
            print(f"🔍 Selecting {len(subcategories)} sub-categories: {subcategories}")

        available = set(self.get_available_subcategories())
        invalid_subcategories = [s for s in subcategories if s not in available]
        if invalid_subcategories:
            raise ValueError(
                f"Invalid subcategory names: {invalid_subcategories}. "
                f"Available subcategories: {list(available)}"
            )

        all_data = []
        total_items = 0
        for subcategory in subcategories:
            category_data = self.datasets.get(subcategory, [])
            all_data.extend(category_data)
            total_items += len(category_data)
            print(f"  📦 '{subcategory}': {len(category_data)} items")

        print(f"✅ Total selected items: {total_items}")
        return all_data

    def get_available_subcategories(self) -> List[str]:
        return list(self.datasets.keys())
