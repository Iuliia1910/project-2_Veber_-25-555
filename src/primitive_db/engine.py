# src/primitive_db/engine.py
import shlex
from primitive_db.utils import load_metadata, save_metadata
from primitive_db.core import create_table, drop_table, list_tables

DB_META_FILE = "db_meta.json"


def print_help():
    """Выводит справку по командам"""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def run():
    """Основной цикл программы"""
    while True:
        metadata = load_metadata(DB_META_FILE)
        user_input = input(">>>Введите команду: ")
        try:
            args = shlex.split(user_input)
        except ValueError as e:
            print(f"Некорректная команда: {e}. Попробуйте снова.")
            continue

        if not args:
            continue

        command = args[0]

        if command == "exit":
            break
        elif command == "help":
            print_help()
        elif command == "create_table":
            if len(args) < 2:
                print("Некорректное значение: отсутствует имя таблицы. Попробуйте снова.")
                continue
            table_name = args[1]
            columns = args[2:]
            metadata = create_table(metadata, table_name, columns)
            save_metadata(DB_META_FILE, metadata)
        elif command == "drop_table":
            if len(args) != 2:
                print("Некорректное значение: укажите имя таблицы. Попробуйте снова.")
                continue
            table_name = args[1]
            metadata = drop_table(metadata, table_name)
            save_metadata(DB_META_FILE, metadata)
        elif command == "list_tables":
            list_tables(metadata)
        else:
            print(f"Функции {command} нет. Попробуйте снова.")
