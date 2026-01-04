# src/primitive_db/core.py
from typing import Dict, List

# поддерживаемые типы для колонок
VALID_TYPES = {"int", "str", "bool"}
TYPE_CAST = {
    "int": int,
    "str": str,
    "bool": lambda x: x.lower() == "true",
}

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

    # добавляем ID:int
    parsed_columns.insert(0, "ID:int")

    metadata[table_name] = parsed_columns
    print(f'Таблица "{table_name}" успешно создана со столбцами: {", ".join(parsed_columns)}')
    return metadata


def drop_table(metadata: Dict, table_name: str) -> Dict:
    """Удаляет таблицу"""
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


# ---------------- CRUD ----------------

def insert_row(metadata: Dict, table_name: str, values: List[str], table_data: List[dict]) -> List[dict]:
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return table_data

    columns = metadata[table_name][1:]  # без ID
    if len(values) != len(columns):
        print("Ошибка: Некорректное количество значений.")
        return table_data

    new_id = max([row["ID"] for row in table_data], default=0) + 1
    record = {"ID": new_id}

    for col_def, raw_value in zip(columns, values):
        name, typ = col_def.split(":")
        try:
            record[name] = TYPE_CAST[typ](raw_value)
        except Exception:
            print(f"Некорректное значение: {raw_value}")
            return table_data

    table_data.append(record)
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return table_data


def select_rows(table_data: List[dict], where: dict | None = None) -> List[dict]:
    if not where:
        return table_data
    key, value = next(iter(where.items()))
    return [row for row in table_data if row.get(key) == value]


def update_rows(table_data: List[dict], set_clause: dict, where: dict) -> List[dict]:
    key_w, value_w = next(iter(where.items()))
    updated = False
    for row in table_data:
        if row.get(key_w) == value_w:
            for k, v in set_clause.items():
                row[k] = v
            print(f'Запись с ID={row["ID"]} в таблице успешно обновлена.')
            updated = True
    if not updated:
        print("Записи, соответствующей условию, не найдено.")
    return table_data


def delete_rows(table_data: List[dict], where: dict) -> List[dict]:
    key, value = next(iter(where.items()))
    initial_len = len(table_data)
    table_data = [row for row in table_data if row.get(key) != value]
    if len(table_data) < initial_len:
        print("Запись успешно удалена.")
    else:
        print("Записи, соответствующей условию, не найдено.")
    return table_data