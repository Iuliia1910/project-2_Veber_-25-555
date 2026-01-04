# src/primitive_db/engine.py
import shlex
from primitive_db.utils import load_metadata, save_metadata, load_table_data, save_table_data
from primitive_db.core import (
    create_table,
    drop_table,
    list_tables,
    insert_row,
    select_rows,
    update_rows,
    delete_rows,
)
from prettytable import PrettyTable

DB_META_FILE = "db_meta.json"
DATA_DIR = "data"


def print_help():
    """Вывод справки по командам"""
    print("\n***Процесс работы с таблицей***")
    print("Функции управления таблицами:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> list_tables - показать список всех таблиц\n")
    print("Функции CRUD:")
    print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...)")
    print("<command> select from <имя_таблицы> [where <столбец> = <значение>]")
    print("<command> update <имя_таблицы> set <столбец> = <значение> where <столбец> = <значение>")
    print("<command> delete from <имя_таблицы> where <столбец> = <значение>")
    print("<command> info <имя_таблицы>")
    print("Общие команды:")
    print("<command> help - справка")
    print("<command> exit - выход из программы\n")


def print_table(rows: list):
    """Вывод данных красиво через PrettyTable"""
    if not rows:
        print("Нет данных.")
        return
    table = PrettyTable()
    table.field_names = rows[0].keys()
    for row in rows:
        table.add_row(row.values())
    print(table)


def parse_condition(expr: str) -> dict:
    """Превращает 'age = 28' в {'age': 28}"""
    column, value = expr.split("=")
    column = column.strip()
    value = value.strip().strip('"')
    if value.lower() == "true":
        value = True
    elif value.lower() == "false":
        value = False
    elif value.isdigit():
        value = int(value)
    return {column: value}


def parse_set_clause(expr: str) -> dict:
    """Превращает 'age = 28' в {'age': 28} для update"""
    return parse_condition(expr)


def run():
    """Основной цикл программы"""
    while True:
        metadata = load_metadata(DB_META_FILE)
        user_input = input(">>>Введите команду: ")

        try:
            args = shlex.split(user_input)
        except ValueError as e:
            print(f"Некорректная команда: {e}")
            continue

        if not args:
            continue

        command = args[0].lower()

        # ---------------- Общие команды ----------------
        if command == "exit":
            break
        elif command == "help":
            print_help()

        # ---------------- Управление таблицами ----------------
        elif command == "create_table":
            if len(args) < 2:
                print("Некорректное значение: отсутствует имя таблицы")
                continue
            table_name = args[1]
            columns = args[2:]
            metadata = create_table(metadata, table_name, columns)
            save_metadata(DB_META_FILE, metadata)

        elif command == "drop_table":
            if len(args) != 2:
                print("Некорректное значение: укажите имя таблицы")
                continue
            table_name = args[1]
            metadata = drop_table(metadata, table_name)
            save_metadata(DB_META_FILE, metadata)

        elif command == "list_tables":
            list_tables(metadata)

        # ---------------- CRUD ----------------
        elif command == "insert":
            if args[1].lower() != "into" or "values" not in args:
                print("Некорректная команда insert")
                continue
            table_name = args[2]
            values_index = args.index("values") + 1
            values_str = " ".join(args[values_index:])
            values_str = values_str.strip("()")
            values = [v.strip().strip('"') for v in values_str.split(",")]
            table_data = load_table_data(table_name)
            table_data = insert_row(metadata, table_name, values, table_data)
            save_table_data(table_name, table_data)

        elif command == "select":
            if args[1].lower() != "from":
                print("Некорректная команда select")
                continue
            table_name = args[2]
            table_data = load_table_data(table_name)
            if "where" in args:
                where_index = args.index("where") + 1
                condition = parse_condition(" ".join(args[where_index:]))
                rows = select_rows(table_data, condition)
            else:
                rows = select_rows(table_data)
            print_table(rows)

        elif command == "update":
            table_name = args[1]
            if "set" not in args or "where" not in args:
                print("Некорректная команда update")
                continue
            set_index = args.index("set") + 1
            where_index = args.index("where")
            set_clause = parse_set_clause(" ".join(args[set_index:where_index]))
            condition = parse_condition(" ".join(args[where_index + 1 :]))
            table_data = load_table_data(table_name)
            table_data = update_rows(table_data, set_clause, condition)
            save_table_data(table_name, table_data)

        elif command == "delete":
            if args[1].lower() != "from" or "where" not in args:
                print("Некорректная команда delete")
                continue
            table_name = args[2]
            where_index = args.index("where")
            condition = parse_condition(" ".join(args[where_index + 1 :]))
            table_data = load_table_data(table_name)
            table_data = delete_rows(table_data, condition)
            save_table_data(table_name, table_data)

        elif command == "info":
            table_name = args[1]
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue
            columns = metadata[table_name]
            table_data = load_table_data(table_name)
            print(f"Таблица: {table_name}")
            print(f"Столбцы: {', '.join(columns)}")
            print(f"Количество записей: {len(table_data)}")

        else:
            print(f"Функции {command} нет. Попробуйте снова.")