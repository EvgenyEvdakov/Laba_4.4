#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import argparse
from pathlib import Path
import logging
from datetime import datetime  # Импортируем datetime

# Настройка логирования без миллисекунд в формате
logging.basicConfig(
    filename="routes_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"  # Убираем миллисекунды из формата времени
)


# Функция для добавления миллисекунд к записи лога
def log_with_millis(level, message):
    millis = int((datetime.now().microsecond) / 1000)  # Получаем миллисекунды
    logging.log(level, f"{message}.{millis:03d}")  # Форматируем строку лога


# Получаем путь к домашнему каталогу пользователя
home_dir = str(Path.home())

# Создаем путь к файлу данных в домашнем каталоге пользователя
file_path = Path(home_dir) / "idz.json"


# Функция для ввода данных о маршрутах
def add_route(routes, start, end, number):
    try:
        # Проверка на корректность номера маршрута
        if not number.isdigit():
            raise ValueError("Номер маршрута должен быть числом.")

        route = {
            "start": start,
            "end": end,
            "number": number
        }
        routes.append(route)
        log_with_millis(logging.INFO, f"Добавлен новый маршрут: {route}")
        return routes
    except ValueError as e:
        log_with_millis(logging.ERROR, f"Ошибка при добавлении маршрута: {e}")
        print(f"Ошибка: {e}")


# Функция для вывода информации о маршруте по номеру
def find_route(routes, number):
    try:
        found = False
        for route in routes:
            if route["number"] == number:
                print("Начальный пункт маршрута:", route["start"])
                print("Конечный пункт маршрута:", route["end"])
                log_with_millis(logging.INFO, f"Найден маршрут: {route}")
                found = True
                break
        if not found:
            log_with_millis(logging.WARNING, f"Маршрут с номером {number} не найден.")
            print("Маршрут с таким номером не найден.")
    except Exception as e:
        log_with_millis(logging.ERROR, f"Ошибка при поиске маршрута: {e}")
        print(f"Ошибка при поиске маршрута: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Управление маршрутами')
    parser.add_argument('--add', action='store_true', help='Добавить новый маршрут')
    parser.add_argument('--number', type=str, help='Номер маршрута для поиска')

    args = parser.parse_args()

    # Загрузка существующих маршрутов из файла
    try:
        with open(file_path, "r") as file:
            routes = json.load(file)
        log_with_millis(logging.INFO, "Данные маршрутов загружены из файла.")
    except FileNotFoundError:
        routes = []
        log_with_millis(logging.WARNING, "Файл с маршрутами не найден, создан новый список маршрутов.")
    except json.JSONDecodeError:
        routes = []
        log_with_millis(logging.ERROR, "Ошибка при чтении JSON файла. Файл поврежден, создан новый список маршрутов.")
    except Exception as e:
        routes = []
        log_with_millis(logging.ERROR, f"Неожиданная ошибка при загрузке данных: {e}")
        print(f"Ошибка при загрузке данных: {e}")

    # Добавление нового маршрута
    if args.add:
        try:
            start = input("Введите начальный пункт маршрута: ")
            end = input("Введите конечный пункт маршрута: ")
            number = input("Введите номер маршрута: ")
            routes = add_route(routes, start, end, number)
        except Exception as e:
            log_with_millis(logging.ERROR, f"Ошибка при добавлении маршрута: {e}")
            print(f"Ошибка при добавлении маршрута: {e}")

    # Поиск маршрута по номеру
    if args.number:
        try:
            find_route(routes, args.number)
        except Exception as e:
            log_with_millis(logging.ERROR, f"Ошибка при поиске маршрута: {e}")
            print(f"Ошибка при поиске маршрута: {e}")

    # Сохранение данных в файл JSON после ввода информации
    try:
        with open(file_path, "w") as file:
            json.dump(routes, file)
        log_with_millis(logging.INFO, "Данные маршрутов сохранены в файл.")
    except Exception as e:
        log_with_millis(logging.ERROR, f"Ошибка при сохранении данных: {e}")
        print(f"Ошибка при сохранении данных: {e}")
