# test_keybinds.py

from __future__ import annotations

import pytest
from pyselector.key_manager import Keybind
from pyselector.key_manager import KeybindError
from pyselector.key_manager import KeyManager


@pytest.fixture
def key_manager() -> KeyManager:
    return KeyManager()


@pytest.fixture
def test_keybind() -> tuple[str, str, bool]:
    return ("alt-n", "add record", False)


def test_add_keybind(
    key_manager: KeyManager, test_keybind: tuple[str, str, bool]
) -> None:
    bind, description, hidden = test_keybind
    keybind = key_manager.add(bind, description, lambda: None, hidden=hidden)
    assert isinstance(keybind, Keybind)
    assert keybind.bind == bind
    assert keybind.description == description
    assert keybind.hidden == hidden


def test_register_keybind(
    key_manager: KeyManager, test_keybind: tuple[str, str, bool]
) -> None:
    bind, description, hidden = test_keybind
    keybind = Keybind(
        id=1,
        bind=bind,
        code=10,
        description=description,
        hidden=hidden,
        callback=lambda: None,
    )
    registered_keybind = key_manager.register(keybind)
    assert registered_keybind == keybind


def test_register_and_replace_keybind(
    key_manager: KeyManager, test_keybind: tuple[str, str, bool]
) -> None:
    bind, description, hidden = test_keybind
    keybind = Keybind(
        id=1,
        bind=bind,
        code=10,
        description=description,
        hidden=hidden,
        callback=lambda: None,
    )
    key_manager.register(keybind)
    key_manager.register(keybind, exist_ok=True)


def test_register_existing_keybind(
    key_manager: KeyManager, test_keybind: tuple[str, str, bool]
) -> None:
    bind, description, hidden = test_keybind
    keybind = Keybind(
        id=1,
        bind=bind,
        code=10,
        description=description,
        hidden=hidden,
        callback=lambda: None,
    )
    key_manager.register(keybind)
    with pytest.raises(KeybindError):
        key_manager.register(keybind)


def test_unregister_keybind(
    key_manager: KeyManager, test_keybind: tuple[str, str, bool]
) -> None:
    bind, description, hidden = test_keybind
    keybind = Keybind(
        id=1,
        bind=bind,
        code=10,
        description=description,
        hidden=hidden,
        callback=lambda: None,
    )
    key_manager.register(keybind)
    key_manager.unregister(bind)
    assert key_manager.list_registered == []


def test_unregister_keybind_error(key_manager: KeyManager) -> None:
    with pytest.raises(KeybindError):
        key_manager.unregister("CTRL+XX")


def test_toggle_all_keybinds(key_manager: KeyManager) -> None:
    key_manager.add("CTRL+S", "Save file", lambda: None)
    key_manager.add("CTRL+Z", "Undo last action", lambda: None)
    key_manager.add("CTRL+X", "Cut selected text", lambda: None)
    key_manager.toggle_all()
    for keybind in key_manager.list_registered:
        assert keybind.hidden


def test_toggle_hidden_keybinds(key_manager: KeyManager) -> None:
    key_manager.add("CTRL+S", "Save file", lambda: None, hidden=False)
    key_manager.add("CTRL+Z", "Undo last action", lambda: None, hidden=False)
    key_manager.add("CTRL+X", "Cut selected text", lambda: None, hidden=False)
    key_manager.add("CTRL+P", "Ignore", lambda: None, hidden=True)

    key_manager.toggle_hidden()
    assert len(key_manager.temp_hidden) == 3

    for keybind in key_manager.temp_hidden:
        assert keybind.hidden

    key_manager.toggle_hidden(restore=True)
    for keybind in key_manager.temp_hidden:
        assert not keybind.hidden
