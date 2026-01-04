# src/primitive_db/utils.py
import json
import os
from typing import Dict, List

DATA_DIR = "data"


def load_metadata(filepath: str) -> Dict:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_metadata(filepath: str, data: Dict) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_table_data(table_name: str) -> List[dict]:
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(f"{DATA_DIR}/{table_name}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_table_data(table_name: str, data: List[dict]) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(f"{DATA_DIR}/{table_name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
