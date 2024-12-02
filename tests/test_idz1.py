#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import json
from pathlib import Path
from idz1 import Route, RouteManager

@pytest.fixture
def temp_file(tmp_path: Path) -> Path:
    """Фикстура для временного файла."""
    return tmp_path / "routes.json"

def test_route_methods():
    """Тестирование методов Route."""
    route = Route("Москва", "Санкт-Петербург", "101")
    route_dict = route.to_dict()
    assert route_dict == {
        "start": "Москва",
        "end": "Санкт-Петербург",
        "number": "101"
    }

    new_route = Route.from_dict(route_dict)
    assert new_route.start == "Москва"
    assert new_route.end == "Санкт-Петербург"
    assert new_route.number == "101"

def test_route_manager_initialization(temp_file: Path):
    """Тестирование инициализации RouteManager."""
    manager = RouteManager(temp_file)
    assert manager.routes == []

def test_add_route(temp_file: Path):
    """Тестирование добавления маршрута."""
    manager = RouteManager(temp_file)
    manager.add_route("Москва", "Казань", "202")
    assert len(manager.routes) == 1
    assert manager.routes[0].start == "Москва"
    assert manager.routes[0].end == "Казань"
    assert manager.routes[0].number == "202"

    # Тестирование ошибки при некорректном номере
    with pytest.raises(ValueError, match="Номер маршрута должен быть числом."):
        manager.add_route("Москва", "Сочи", "ABC")

def test_save_and_load_routes(temp_file: Path):
    """Тестирование сохранения и загрузки маршрутов."""
    manager = RouteManager(temp_file)
    manager.add_route("Москва", "Владивосток", "303")
    manager.save_routes()

    # Проверка, что данные сохранены в файл
    with open(temp_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    assert len(data) == 1
    assert data[0] == {
        "start": "Москва",
        "end": "Владивосток",
        "number": "303"
    }

    # Загрузка маршрутов из файла
    new_manager = RouteManager(temp_file)
    assert len(new_manager.routes) == 1
    assert new_manager.routes[0].start == "Москва"
    assert new_manager.routes[0].end == "Владивосток"
    assert new_manager.routes[0].number == "303"

def test_find_route(temp_file: Path):
    """Тестирование поиска маршрута."""
    manager = RouteManager(temp_file)
    manager.add_route("Москва", "Екатеринбург", "404")
    manager.add_route("Сочи", "Краснодар", "505")

    route = manager.find_route("404")
    assert route is not None
    assert route.start == "Москва"
    assert route.end == "Екатеринбург"

    route = manager.find_route("999")
    assert route is None

def test_logging(temp_file: Path, caplog):
    """Тестирование логирования."""
    manager = RouteManager(temp_file)

    # Проверка логов при добавлении маршрута
    with caplog.at_level("INFO"):
        manager.add_route("Омск", "Новосибирск", "606")
    assert "Добавлен маршрут:" in caplog.text

    # Проверка логов при поиске маршрута
    with caplog.at_level("WARNING"):
        manager.find_route("999")
    assert "Маршрут с номером 999 не найден." in caplog.text

    # Проверка логов при загрузке и сохранении
    manager.save_routes()
    with caplog.at_level("INFO"):
        RouteManager(temp_file)
    assert "Маршруты успешно загружены из файла." in caplog.text
