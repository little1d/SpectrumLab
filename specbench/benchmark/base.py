from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Optional, Union
import json
from specbench.evaluator import get_evaluator


class BaseGroup(ABC):
    def __init__(self, level: str, path: str = "./data"):
        self.level = level
        self.path = Path(path)
        self.datasets = {}
        self._init_evaluator()
        self._load_datasets()

    def _load_datasets(self):
        """
        Load benchmark datasets for the current level.
        """
        local_level_path = self.path / self.level

        print(f"Loading datasets for level '{self.level}'...")
        print(f"Looking for local datasets in: {local_level_path}")

        if local_level_path.exists() and local_level_path.is_dir():
            print("✔ Local datasets found, loading …")
            self._load_from_local(local_level_path)
        else:
            print("✖ Local datasets not found, falling back to HuggingFace …")
            self._load_from_remote(local_level_path)

        print(
            f"Loaded {len(self.datasets)} sub-categories: {list(self.datasets.keys())}"
        )

    def _load_from_local(self, local_level_path: Path):
        """从本地加载数据"""
        self.datasets = {}

        for sub_category_dir in local_level_path.iterdir():
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

    def _load_json(self, file_path: Path) -> List[Dict]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
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

    def get_benchmark_data(self, benchmark: str) -> List[Dict]:
        """获取指定benchmark的数据"""
        return self.datasets.get(benchmark, [])

    def get_available_benchmarks(self) -> List[str]:
        return list(self.datasets.keys())

    def _normalize_benchmark_name(
        self, benchmarks: Union[str, List[str]] = "all"
    ) -> List[str]:
        if benchmarks == "all":
            return self.get_available_benchmarks()
        elif isinstance(benchmarks, str):
            return [benchmarks]
        elif isinstance(benchmarks, list):
            return benchmarks
        else:
            raise ValueError(f"Invalid benchmark name: {benchmarks}")

    def _validate_benchmark_name(self, benchmarks: List[str]) -> List[str]:
        available = self.get_available_benchmarks()
        valid_benchmarks = []
        invalid_benchmarks = []

        for benchmark in benchmarks:
            if benchmark in available:
                valid_benchmarks.append(benchmark)
            else:
                invalid_benchmarks.append(benchmark)

        if invalid_benchmarks:
            raise ValueError(
                f"Invalid benchmark names: {invalid_benchmarks}. "
                f"Available benchmarks: {list(available)}"
            )

        return valid_benchmarks

    @abstractmethod
    def _init_evaluator(self):
        self.evaluator = get_evaluator(self.level)

    @abstractmethod
    def evaluate(self, benchmarks: Union[str, List[str]], save_dict: bool = True):
        """automatic evaluation function

        Parameters
        ----------
        benchmarks : Union[str, List[str]]
            the benchmarks to evaluate
        save_dict : bool, optional
            save the evaluation results to a dictionary, by default True
        """
        pass

    def evaluate_many(
        self,
        benchmarks: Union[str, List[str]],
        save_dict: bool = True,
        n_runs: int = 5,
        random_seed: int = 42,
    ):
        # TODO
        import random
        import numpy as np

        random.seed(random_seed)
        np.random.seed(random_seed)

        results = []
        for run_idx in range(n_runs):
            run_seed = random_seed + run_idx
            random.seed(run_seed)
            np.random.seed(run_seed)

            result = self.evaluate(benchmarks, save_dict=False)
            result["run_idx"] = run_idx
            result["run_seed"] = run_seed
            results.append(result)

        return results

    def __len__(self) -> int:
        """返回可用benchmark的数量"""
        return len(self.datasets)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(level='{self.level}', benchmarks={len(self)})"
        )
