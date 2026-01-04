# src/primitive_db/core.py
from typing import Dict, List

VALID_TYPES = {"int", "str", "bool"}

def create_table(metadata: Dict, table_name: str, columns: List[str]) -> Dict:
    """Создаёт таблицу с проверкой типов и добавлением ID:int"""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    parsed_columns = []
    for col in columns:
        if ":" not in col:
            print(f"Некорректное значение: {col}. Попробуйте снова.")
            return metadata
        name, typ = col.split(":")
        if typ not in VALID_TYPES:
            print(f"Некорректное значение: {typ}. Попробуйте снова.")
            return metadata
        parsed_columns.append(f"{name}:{typ}")

    # Добавляем ID:int в начало
    parsed_columns.insert(0, "ID:int")

    metadata[table_name] = parsed_columns
    print(f'Таблица "{table_name}" успешно создана со столбцами: {", ".join(parsed_columns)}')
    return metadata

def drop_table(metadata: Dict, table_name: str) -> Dict:
    """Удаляет таблицу, если она существует"""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    metadata.pop(table_name)
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata

def list_tables(metadata: Dict) -> None:
    """Показывает список всех таблиц"""
    if not metadata:
        print("Таблиц нет.")
        return
    for table in metadata:
        print(f"- {table}")
