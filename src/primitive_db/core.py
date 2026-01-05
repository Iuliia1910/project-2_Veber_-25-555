# src/primitive_db/core.py
from typing import Any, Dict, List

from primitive_db.decorators import confirm_action, handle_db_errors, log_time

VALID_TYPES = {"int": int, "str": str, "bool": bool}

@handle_db_errors
def create_table(metadata: Dict, table_name: str, columns: List[str]) -> Dict:
    if table_name in metadata:
        raise KeyError(f'Таблица "{table_name}" уже существует')

    parsed_columns = []
    for col in columns:
        if ":" not in col:
            raise ValueError(f"Некорректное значение: {col}")
        name, typ = col.split(":")
        if typ not in VALID_TYPES:
            raise ValueError(f"Некорректный тип данных: {typ}")
        parsed_columns.append(f"{name}:{typ}")

    parsed_columns.insert(0, "ID:int")
    metadata[table_name] = parsed_columns
    print(f'Таблица "{table_name}" успешно создана '
          f'со столбцами: {", ".join(parsed_columns)}')
    return metadata

@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata: Dict, table_name: str) -> Dict:
    if table_name not in metadata:
        raise KeyError(f'Таблица "{table_name}" не существует')
    metadata.pop(table_name)
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata

@handle_db_errors
def list_tables(metadata: Dict) -> List[str]:
    return list(metadata.keys())

@handle_db_errors
@log_time
def insert(metadata: Dict, table_name: str, values: List[Any],
           table_data: List[dict] | None) -> List[dict]:
    if table_name not in metadata:
        raise KeyError(f'Таблица "{table_name}" не существует')

    table_data = table_data or []
    columns = metadata[table_name][1:]

    if len(values) != len(columns):
        raise ValueError("Некорректное количество значений")

    new_id = max((row["ID"] for row in table_data), default=0) + 1
    record = {"ID": new_id}

    for col, value in zip(columns, values):
        name, typ = col.split(":")
        try:
            record[name] = VALID_TYPES[typ](value)
        except Exception:
            raise ValueError(f"Некорректное значение для поля {name}: {value}")

    table_data.append(record)
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return table_data

@handle_db_errors
@log_time
def select_rows(table_data: List[dict] | None,
                where: dict | None = None) -> List[dict]:
    table_data = table_data or []
    if not where:
        return table_data
    key, value = next(iter(where.items()))
    return [row for row in table_data if row.get(key) == value]

@handle_db_errors
def update_rows(table_data: List[dict] | None, set_clause: dict,
                where: dict) -> List[dict]:
    table_data = table_data or []
    key, value = next(iter(where.items()))
    updated = False
    for row in table_data:
        if row.get(key) == value:
            for k, v in set_clause.items():
                row[k] = v
            updated = True
    if not updated:
        raise ValueError("Записи для обновления не найдены")
    print("Записи успешно обновлены.")
    return table_data

@handle_db_errors
@confirm_action("удаление записи")
def delete_rows(table_data: List[dict] | None, where: dict) -> List[dict]:
    table_data = table_data or []
    key, value = next(iter(where.items()))
    new_data = [row for row in table_data if row.get(key) != value]
    if len(new_data) == len(table_data):
        raise ValueError("Записи для удаления не найдены")
    print("Записи успешно удалены.")
    return new_data

# =========================
# INFO
# =========================

@handle_db_errors
def table_info(metadata: Dict, table_name: str, table_data: List[dict] | None) -> dict:
    if table_name not in metadata:
        raise KeyError(f'Таблица "{table_name}" не существует')
    table_data = table_data or []
    info = {
        "name": table_name,
        "columns": metadata[table_name],
        "rows_count": len(table_data),
    }
    print(f"Таблица: {info['name']}")
    print(f"Столбцы: {', '.join(info['columns'])}")
    print(f"Количество записей: {info['rows_count']}")
    return info