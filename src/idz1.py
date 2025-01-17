#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# необходимо выполнить индивидуальное задание 1 лабораторной работы 2.19, добавив возможность
# работы с исключениями и логгирование.

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional


# Настройка логирования
logging.basicConfig(filename="routes_log.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class Route:
    """Класс для представления маршрута."""

    def __init__(self, start: str, end: str, number: str):
        self.start = start
        self.end = end
        self.number = number

    def to_dict(self) -> Dict[str, str]:
        """Преобразование маршрута в словарь для сохранения."""
        return {"start": self.start, "end": self.end, "number": self.number}

    @staticmethod
    def from_dict(data: Dict[str, str]) -> Route:
        """Создание маршрута из словаря."""
        return Route(start=data["start"], end=data["end"], number=data["number"])


class RouteManager:
    """Класс для управления маршрутами."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.routes: List[Route] = self._load_routes()

    def _load_routes(self) -> List[Route]:
        """Загрузка маршрутов из файла."""
        if not self.file_path.exists():
            logging.warning("Файл с маршрутами не найден. Создан новый список.")
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                logging.info("Маршруты успешно загружены из файла.")
                return [Route.from_dict(item) for item in data]
        except (json.JSONDecodeError, Exception) as e:
            logging.error(f"Ошибка загрузки маршрутов: {e}")
            return []

    def save_routes(self) -> None:
        """Сохранение маршрутов в файл."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([route.to_dict() for route in self.routes], file, ensure_ascii=False, indent=4)
            logging.info("Маршруты успешно сохранены.")
        except Exception as e:
            logging.error(f"Ошибка сохранения маршрутов: {e}")
            raise

    def add_route(self, start: str, end: str, number: str) -> None:
        """Добавление нового маршрута."""
        if not number.isdigit():
            raise ValueError("Номер маршрута должен быть числом.")
        new_route = Route(start, end, number)
        self.routes.append(new_route)
        logging.info(f"Добавлен маршрут: {new_route.to_dict()}")

    def find_route(self, number: str) -> Optional[Route]:
        """Поиск маршрута по номеру."""
        for route in self.routes:
            if route.number == number:
                logging.info(f"Найден маршрут: {route.to_dict()}")
                return route
        logging.warning(f"Маршрут с номером {number} не найден.")
        return None


def main() -> None:
    """Основная функция программы."""
    # Получаем путь к файлу в домашнем каталоге пользователя
    home_dir = Path.home()
    file_path = home_dir / "idz.json"
    manager = RouteManager(file_path)

    # Парсер аргументов командной строки
    parser = argparse.ArgumentParser(description="Управление маршрутами")
    parser.add_argument("--add", action="store_true", help="Добавить новый маршрут")
    parser.add_argument("--find", type=str, help="Найти маршрут по номеру")
    args = parser.parse_args()

    # Добавление нового маршрута
    if args.add:
        start = input("Введите начальный пункт маршрута: ")
        end = input("Введите конечный пункт маршрута: ")
        number = input("Введите номер маршрута: ")
        try:
            manager.add_route(start, end, number)
            manager.save_routes()
            print("Маршрут успешно добавлен.")
        except ValueError as e:
            print(f"Ошибка: {e}")

    # Поиск маршрута по номеру
    if args.find:
        route = manager.find_route(args.find)
        if route:
            print(f"Маршрут найден: Начало: {route.start}, Конец: {route.end}")
        else:
            print("Маршрут с таким номером не найден.")

    # Сохранение маршрутов при выходе
    manager.save_routes()


if __name__ == "__main__":
    main()
