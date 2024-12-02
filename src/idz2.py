#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# необходимо изучить возможности модуля logging. Добавить для предыдущего задания вывод в файлы лога даты
# и времени выполнения пользовательской команды с точностью до миллисекунды.

import json
import argparse
from pathlib import Path
import logging
from datetime import datetime
from typing import List, Dict, Optional

# Настройка логирования без миллисекунд в формате
logging.basicConfig(
    filename="routes_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


class Logger:
    """Класс для логирования с миллисекундами."""

    @staticmethod
    def log_with_millis(level: int, message: str):
        millis = int((datetime.now().microsecond) / 1000)  # Получаем миллисекунды
        logging.log(level, f"{message}.{millis:03d}")  # Форматируем строку лога


class RouteManager:
    """Класс для управления маршрутами."""

    def __init__(self, routes: Optional[List[Dict[str, str]]] = None):
        self.routes = routes or []

    def add_route(self, start: str, end: str, number: str) -> None:
        """Добавить новый маршрут."""
        if not number.isdigit():
            raise ValueError("Номер маршрута должен быть числом.")

        route = {
            "start": start,
            "end": end,
            "number": number
        }
        self.routes.append(route)
        Logger.log_with_millis(logging.INFO, f"Добавлен новый маршрут: {route}")

    def find_route(self, number: str) -> Optional[Dict[str, str]]:
        """Найти маршрут по номеру."""
        for route in self.routes:
            if route["number"] == number:
                Logger.log_with_millis(logging.INFO, f"Найден маршрут: {route}")
                return route
        Logger.log_with_millis(logging.WARNING, f"Маршрут с номером {number} не найден.")
        return None

    def save_routes(self, file_path: Path) -> None:
        """Сохранить маршруты в файл."""
        try:
            with open(file_path, "w") as file:
                json.dump(self.routes, file)
            Logger.log_with_millis(logging.INFO, "Данные маршрутов сохранены в файл.")
        except Exception as e:
            Logger.log_with_millis(logging.ERROR, f"Ошибка при сохранении данных: {e}")
            raise


class FileManager:
    """Класс для работы с файлами маршрутов."""

    @staticmethod
    def load_routes(file_path: Path) -> List[Dict[str, str]]:
        """Загрузить маршруты из файла."""
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            Logger.log_with_millis(logging.WARNING, "Файл с маршрутами не найден, создан новый список маршрутов.")
            return []
        except json.JSONDecodeError:
            Logger.log_with_millis(logging.ERROR, "Ошибка при чтении JSON файла. Файл поврежден.")
            return []
        except Exception as e:
            Logger.log_with_millis(logging.ERROR, f"Неожиданная ошибка при загрузке данных: {e}")
            raise


def main() -> None:
    home_dir = str(Path.home())
    file_path = Path(home_dir) / "idz.json"

    routes = FileManager.load_routes(file_path)
    route_manager = RouteManager(routes)

    parser = argparse.ArgumentParser(description='Управление маршрутами')
    parser.add_argument('--add', action='store_true', help='Добавить новый маршрут')
    parser.add_argument('--number', type=str, help='Номер маршрута для поиска')

    args = parser.parse_args()

    if args.add:
        try:
            start = input("Введите начальный пункт маршрута: ")
            end = input("Введите конечный пункт маршрута: ")
            number = input("Введите номер маршрута: ")
            route_manager.add_route(start, end, number)
        except ValueError as e:
            Logger.log_with_millis(logging.ERROR, f"Ошибка при добавлении маршрута: {e}")
            print(f"Ошибка: {e}")

    if args.number:
        route = route_manager.find_route(args.number)
        if route:
            print("Начальный пункт маршрута:", route["start"])
            print("Конечный пункт маршрута:", route["end"])
        else:
            print("Маршрут с таким номером не найден.")

    try:
        route_manager.save_routes(file_path)
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")


if __name__ == '__main__':
    main()
