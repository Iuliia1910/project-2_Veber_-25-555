# src/primitive_db/decorators.py
import time
from functools import wraps


def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден. "
                  "Возможно, база данных не инициализирована.")
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
        from inspect import signature
        sig = signature(func)
        return_type = sig.return_annotation
        if return_type is list:
            return []
        elif return_type is dict:
            return {}
        return None
    return wrapper

def confirm_action(action_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            confirm = input(f'Вы уверены, '
                            f'что хотите выполнить "{action_name}"? [y/n]: ').lower()
            if confirm != "y":
                print("Операция отменена пользователем.")
                return args[3] if len(args) > 3 else None
            return func(*args, **kwargs)
        return wrapper
    return decorator

def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        end = time.monotonic()
        print(f"Функция {func.__name__} выполнилась за {end - start:.3f} секунд")
        return result
    return wrapper