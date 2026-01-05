# src/primitive_db/engine.py
import shlex
from primitive_db.utils import load_metadata, save_metadata, load_table_data, save_table_data
from primitive_db.core import create_table, drop_table, list_tables, insert, select_rows, update_rows, delete_rows, table_info
from prettytable import PrettyTable

DB_META_FILE = "db_meta.json"

def print_help():
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> ...")
    print("<command> drop_table <имя_таблицы>")
    print("<command> list_tables")
    print("<command> insert into <имя_таблицы> values (<значения>)")
    print("<command> select from <имя_таблицы> [where <столбец>=<значение>]")
    print("<command> update <имя_таблицы> set <столбец>=<значение> where <столбец>=<значение>")
    print("<command> delete from <имя_таблицы> where <столбец>=<значение>")
    print("<command> info <имя_таблицы>")
    print("<command> help")
    print("<command> exit\n")

def parse_condition(expr: str):
    column, value = expr.split("=")
    column = column.strip()
    value = value.strip().strip('"').strip("'")
    if value.lower() == "true":
        value = True
    elif value.lower() == "false":
        value = False
    elif value.isdigit():
        value = int(value)
    return {column: value}

def parse_values(values_str: str):
    values_str = values_str.strip().strip("()")
    parts = [v.strip().strip('"').strip("'") for v in values_str.split(",")]
    result = []
    for v in parts:
        if v.lower() == "true":
            result.append(True)
        elif v.lower() == "false":
            result.append(False)
        elif v.isdigit():
            result.append(int(v))
        else:
            result.append(v)
    return result

def print_table(rows: list):
    if not rows:
        print("Нет данных.")
        return
    table = PrettyTable()
    table.field_names = rows[0].keys()
    for row in rows:
        table.add_row(row.values())
    print(table)

def run():
    while True:
        metadata = load_metadata(DB_META_FILE) or {}
        user_input = input(">>>Введите команду: ").strip()
        if not user_input:
            continue
        try:
            args = shlex.split(user_input)
        except ValueError as e:
            print(f"Некорректная команда: {e}")
            continue

        command = args[0].lower()
        try:
            if command == "exit":
                break
            elif command == "help":
                print_help()
            elif command == "create_table":
                table_name = args[1]
                columns = args[2:]
                metadata = create_table(metadata, table_name, columns)
                save_metadata(DB_META_FILE, metadata)
            elif command == "drop_table":
                table_name = args[1]
                metadata = drop_table(metadata, table_name)
                save_metadata(DB_META_FILE, metadata)
            elif command == "list_tables":
                tables = list_tables(metadata)
                if tables:
                    for t in tables:
                        print(f"- {t}")
                else:
                    print("Таблиц нет")
            elif command == "insert":
                if args[1].lower() != "into" or args[3].lower() != "values":
                    print("Некорректная команда insert")
                    continue
                table_name = args[2]
                values = parse_values(" ".join(args[4:]))
                table_data = load_table_data(table_name)
                table_data = insert(metadata, table_name, values, table_data)
                save_table_data(table_name, table_data)
            elif command == "select":
                table_name = args[2]
                table_data = load_table_data(table_name)
                if "where" in args:
                    where_index = args.index("where")
                    condition = parse_condition(" ".join(args[where_index+1:]))
                    rows = select_rows(table_data, condition)
                else:
                    rows = select_rows(table_data)
                print_table(rows)
            elif command == "update":
                table_name = args[1]
                set_index = args.index("set")
                where_index = args.index("where")
                set_clause = parse_condition(" ".join(args[set_index+1:where_index]))
                condition = parse_condition(" ".join(args[where_index+1:]))
                table_data = load_table_data(table_name)
                table_data = update_rows(table_data, set_clause, condition)
                save_table_data(table_name, table_data)
            elif command == "delete":
                if args[1].lower() != "from" or "where" not in args:
                    print("Некорректная команда delete")
                    continue
                table_name = args[2]
                where_index = args.index("where")
                condition = parse_condition(" ".join(args[where_index+1:]))
                table_data = load_table_data(table_name)
                table_data = delete_rows(table_data, condition)
                save_table_data(table_name, table_data)
            elif command == "info":
                table_name = args[1]
                table_data = load_table_data(table_name)
                table_info(metadata, table_name, table_data)
            else:
                print(f"Функции {command} нет")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")