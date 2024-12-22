import pytest
import logging
from pathlib import Path
from datetime import date
from primer1 import Staff, Worker, IllegalYearError, UnknownCommandError


@pytest.fixture
def temp_file(tmp_path: Path) -> Path:
    """Фикстура для временного файла."""
    return tmp_path / "workers.xml"


@pytest.fixture
def staff_with_data():
    """Фикстура для создания тестового объекта Staff с данными."""
    staff = Staff()
    staff.add("Иванов И.И.", "Инженер", 2005)
    staff.add("Петров П.П.", "Менеджер", 2010)
    return staff


def test_add_worker():
    """Тестирование добавления сотрудника."""
    staff = Staff()
    staff.add("Иванов И.И.", "Инженер", 2000)
    assert len(staff.workers) == 1
    assert staff.workers[0] == Worker(name="Иванов И.И.", post="Инженер", year=2000)


def test_add_worker_invalid_year():
    """Тестирование добавления сотрудника с некорректным годом."""
    staff = Staff()
    current_year = date.today().year
    with pytest.raises(IllegalYearError):
        staff.add("Иванов И.И.", "Инженер", current_year + 1)


def test_select_workers(staff_with_data):
    """Тестирование выбора сотрудников с заданным стажем."""
    selected = staff_with_data.select(10)
    assert len(selected) == 2  # Ожидаем двух сотрудников
    assert selected[0].name == "Иванов И.И."
    assert selected[1].name == "Петров П.П."


def test_save_and_load_workers(temp_file, staff_with_data):
    """Тестирование сохранения и загрузки сотрудников из файла."""
    staff_with_data.save(temp_file)
    loaded_staff = Staff()
    loaded_staff.load(temp_file)
    assert len(loaded_staff.workers) == len(staff_with_data.workers)
    assert loaded_staff.workers[0].name == staff_with_data.workers[0].name


def test_save_empty_staff(temp_file):
    """Тестирование сохранения пустого списка сотрудников."""
    staff = Staff()
    staff.save(temp_file)
    loaded_staff = Staff()
    loaded_staff.load(temp_file)
    assert len(loaded_staff.workers) == 0


def test_unknown_command():
    """Тестирование обработки неизвестной команды."""
    with pytest.raises(UnknownCommandError) as excinfo:
        raise UnknownCommandError("неизвестная_команда")
    assert "неизвестная_команда" in str(excinfo.value)


def test_logging_add_worker(caplog):
    """Тестирование логгирования добавления сотрудника."""
    staff = Staff()
    with caplog.at_level(logging.INFO):
        staff.add("Иванов И.И.", "Инженер", 2000)
        logging.info("Добавлен сотрудник: Иванов И.И., Инженер, поступивший в 2000 году.")
    assert "Добавлен сотрудник: Иванов И.И., Инженер, поступивший в 2000 году." in caplog.text


def test_logging_load_data(temp_file, caplog):
    """Тестирование логгирования загрузки данных."""
    staff = Staff()
    staff.add("Иванов И.И.", "Инженер", 2000)
    staff.save(temp_file)

    with caplog.at_level(logging.INFO):
        new_staff = Staff()
        new_staff.load(temp_file)
        logging.info(f"Загружены данные из файла {temp_file}.")
    assert f"Загружены данные из файла {temp_file}." in caplog.text


def test_logging_error(caplog):
    """Тестирование логгирования ошибок."""
    staff = Staff()
    with caplog.at_level(logging.ERROR):
        try:
            staff.add("Иванов И.И.", "Инженер", -1)
        except IllegalYearError as e:
            logging.error(f"Ошибка: {e}")
    assert "Ошибка: -1 -> Illegal year number" in caplog.text
