#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
from pathlib import Path

import pytest

from idz2 import FileManager, Logger, RouteManager


@pytest.fixture
def temp_file(tmp_path: Path) -> Path:
    """Фикстура для временного файла."""
    return tmp_path / "routes.json"


def test_logger_with_millis(caplog):
    """Тестирование логгера с миллисекундами."""
    with caplog.at_level("INFO"):
        Logger.log_with_millis(logging.INFO, "Тестовое сообщение")
    assert "Тестовое сообщение" in caplog.text


def test_add_route(temp_file: Path):
    """Тестирование добавления маршрута."""
    manager = RouteManager()
    manager.add_route("Москва", "Казань", "101")
    manager.add_route("Сочи", "Краснодар", "202")
    assert len(manager.routes) == 2
    assert manager.routes[0]["start"] == "Москва"
    assert manager.routes[1]["end"] == "Краснодар"

    # Сохранение маршрутов
    manager.save_routes(temp_file)

    # Проверяем, что данные корректно сохранены
    with open(temp_file, "r") as file:
        saved_data = json.load(file)
    assert len(saved_data) == 2
    assert saved_data[0]["number"] == "101"
    assert saved_data[1]["start"] == "Сочи"


def test_find_route(temp_file: Path):
    """Тестирование поиска маршрута."""
    manager = RouteManager(
        [{"start": "Москва", "end": "Казань", "number": "101"}, {"start": "Сочи", "end": "Краснодар", "number": "202"}]
    )
    route = manager.find_route("101")
    assert route is not None
    assert route["start"] == "Москва"
    assert route["end"] == "Казань"

    not_found_route = manager.find_route("999")
    assert not_found_route is None


def test_load_routes(temp_file: Path, caplog):
    """Тестирование загрузки маршрутов из файла."""
    data = [
        {"start": "Москва", "end": "Казань", "number": "101"},
        {"start": "Сочи", "end": "Краснодар", "number": "202"},
    ]

    # Сохранение тестовых данных
    with open(temp_file, "w") as file:
        json.dump(data, file)

    # Загрузка маршрутов
    with caplog.at_level("INFO"):
        routes = FileManager.load_routes(temp_file)
    assert len(routes) == 2
    assert routes[0]["start"] == "Москва"
    assert routes[1]["end"] == "Краснодар"


def test_load_routes_missing_file(tmp_path: Path, caplog):
    """Тестирование загрузки маршрутов из несуществующего файла."""
    missing_file = tmp_path / "missing.json"

    with caplog.at_level("WARNING"):
        routes = FileManager.load_routes(missing_file)
    assert routes == []
    assert "Файл с маршрутами не найден" in caplog.text


def test_load_routes_invalid_json(temp_file: Path, caplog):
    """Тестирование загрузки маршрутов из файла с некорректным JSON."""
    with open(temp_file, "w") as file:
        file.write("{invalid json")

    with caplog.at_level("ERROR"):
        routes = FileManager.load_routes(temp_file)
    assert routes == []
    assert "Ошибка при чтении JSON файла" in caplog.text


def test_save_routes_error(temp_file: Path, caplog):
    """Тестирование обработки ошибок при сохранении маршрутов."""
    manager = RouteManager([{"start": "Москва", "end": "Казань", "number": "101"}])

    # Попробуем сохранить в системную директорию, к которой нет прав на запись
    no_write_dir = Path("C:/Windows/System32")
    no_write_file = no_write_dir / "routes.json"

    try:
        # Попытка сохранить данные в системную директорию без прав на запись
        with pytest.raises(PermissionError):
            manager.save_routes(no_write_file)
    except PermissionError:
        # Если исключение возникло, проверим, что оно было зафиксировано в логах
        assert "Ошибка при сохранении данных" in caplog.text
