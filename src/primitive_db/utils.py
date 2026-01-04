# src/primitive_db/utils.py
import json
from typing import Dict

def load_metadata(filepath: str) -> Dict:
    """Загружает метаданные из JSON-файла. Если файл отсутствует, возвращает пустой словарь."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_metadata(filepath: str, data: Dict) -> None:
    """Сохраняет метаданные в JSON-файл."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
