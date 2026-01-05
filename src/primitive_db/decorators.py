# src/primitive_db/decorators.py
import time
from functools import wraps

def handle_db_errors(func):
    """Декоратор для централизованной обработки ошибок базы данных"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден. Возможно, база данных не инициализирована.")
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

        # Возвращаем "безопасное" значение в зависимости от аннотации
        from inspect import signature
        sig = signature(func)
        return_type = sig.return_annotation
        if return_type == list:
            return []
        elif return_type == dict:
            return {}
        return None
    return wrapper

def confirm_action(action_name: str):
    """Декоратор для подтверждения опасных действий"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            confirm = input(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ').lower()
            if confirm != "y":
                print("Операция отменена пользователем.")
                return args[3] if len(args) > 3 else None  # возвращаем table_data, если есть
            return func(*args, **kwargs)
        return wrapper
    return decorator

def log_time(func):
    """Декоратор для замера времени выполнения"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        end = time.monotonic()
        print(f"Функция {func.__name__} выполнилась за {end - start:.3f} секунд")
        return result
    return wrapper