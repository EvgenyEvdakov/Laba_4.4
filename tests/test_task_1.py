<<<<<<< HEAD
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any

import pytest

from task_1 import main


def test_main(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[Any]
) -> None:
    inputs = iter(["42", "100"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main()

    captured = capsys.readouterr()
    assert captured.out == "Результат: 142\n"

    inputs = iter(["a", "100"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main()

    captured = capsys.readouterr()
=======
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any

import pytest

from task_1 import main


def test_main(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[Any]
) -> None:
    inputs = iter(["42", "100"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main()

    captured = capsys.readouterr()
    assert captured.out == "Результат: 142\n"

    inputs = iter(["a", "100"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main()

    captured = capsys.readouterr()
>>>>>>> c5c93c71d7ab32bdff3cdc2a89af2656431cf9ca
    assert captured.out == "Результат: a100\n"