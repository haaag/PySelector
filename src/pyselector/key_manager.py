# keybinds.py

from __future__ import annotations

import logging
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Callable

log = logging.getLogger(__name__)


class KeybindError(Exception):
    pass


@dataclass
class Keybind:
    """
    Represents a keybind, which associates a keyboard key or
    combination of keys with a action function.

    Attributes:
        id      (int): The unique identifier of the keybind.
        bind    (str): The key or key combination that triggers the keybind.
        code    (int): The unique code of the keybind.
        description (str): A brief description of the keybind.
        action  (Optional[str]): An optional action associated with the keybind. Defaults to an empty string.
        hidden  (bool): Whether the keybind is hidden from the user interface. Defaults to True.
        action (Optional[Callable[..., Any]]): The function to call when the keybind is triggered. Defaults to None.
    """

    id: int
    bind: str
    description: str
    code: int
    action: Callable[..., Any]
    hidden: bool = True

    def toggle(self) -> None:
        """Toggles the visibility of the keybind in the user interface."""
        log.debug('toggling keybind=%s %s', self.hidden, self.bind)
        self.hidden = not self.hidden

    def show(self) -> None:
        self.hidden = False

    def hide(self) -> None:
        self.hidden = True

    def __hash__(self):
        return hash((self.code, self.description))

    def __str__(self) -> str:
        return f"{self.bind:<10}: {self.description} ({'Hidden' if self.hidden else 'Visible'})"


@dataclass
class KeyManager:
    """
    A class for managing keybinds, which are associations between key combinations
    and action functions.

    Attributes:
        keys        (dict[str, Keybind]): A dictionary mapping keybinds to their corresponding `Keybind` objects.
        key_count   (int): A counter for assigning unique IDs to newly added keybinds.
        code_count  (int): A counter for assigning unique codes to newly added keybinds.
        temp_hidden (list[Keybind]): A list of temporarily hidden keybinds.
    """

    keys: dict[int, Keybind] = field(default_factory=dict)
    key_count = 1
    code_count = 1
    original_states: list[Keybind] = field(default_factory=list)

    def add(
        self,
        bind: str,
        description: str,
        action: Callable[..., Any] = lambda val: val,
        hidden: bool = False,
        exist_ok: bool = False,
    ) -> Keybind:
        """
        Registers a new keybind with the specified bind and description,
        and associates it with the specified action function.
        """
        log.debug(f'adding keybind={bind} {description}')
        return self.register(
            Keybind(
                id=self.key_count,
                bind=bind,
                code=self.code_count,
                description=description,
                hidden=hidden,
                action=action,
            ),
            exist_ok=exist_ok,
        )

    def unregister(self, code: int) -> Keybind:
        """Removes the keybind with the specified bind."""
        if not self.keys.get(code):
            err_msg = f'No keybind found with {code=}'
            log.error(err_msg)
            raise KeybindError(err_msg)
        log.debug(f'removing keybind={self.keys[code].bind}')
        return self.keys.pop(code)

    def unregister_all(self) -> list[Keybind]:
        """Removes all registered keybinds."""
        keys = list(self.keys.values())
        log.debug(f'removing {len(keys)} keybinds')
        self.keys.clear()
        return keys

    def register(self, key: Keybind, exist_ok: bool = False) -> Keybind:
        """
        Args:
            key     (Keybind): The keybind to register.
            exist_ok (bool): Whether to overwrite an existing keybind with the same bind. Defaults to False.

        Returns:
            Keybind: The registered keybind.

        Raises:
            KeybindError: If `exist_ok` is False and a keybind with the same bind is already registered.
        """
        if key is None:
            err = 'key is None'
            raise KeybindError(err)

        if exist_ok and self.keys.get(key.code):
            self.unregister(key.code)

        if self.keys.get(key.code):
            err = f'{key.bind=} already registered'
            log.error(err)
            raise KeybindError(err)

        self.key_count += 1
        self.code_count += 1
        self.keys[key.code] = key
        log.debug(f'registered keybind={key}')
        return key

    def register_all(self, keys: list[Keybind], exist_ok: bool = False) -> None:
        """Registers a list of keybinds."""
        for k in keys:
            self.register(k, exist_ok)

    @property
    def list_keys(self) -> list[Keybind]:
        return list(self.keys.values())

    def hide_all(self) -> None:
        """Hides all keybinds."""
        for key in self.list_keys:
            if not key.hidden:
                key.hide()

    def toggle_all(self) -> None:
        """Toggles the "hidden" property of all non-hidden keybinds."""
        for k in self.list_keys:
            k.hidden = not k.hidden

    def toggle_hidden(self, restore: bool = False) -> None:
        """
        Toggles the "hidden" property of all non-hidden keybinds, and
        temporarily stores the original "hidden" state of each keybind.
        If `restore` is True, restores the original "hidden" state of each keybind.
        """
        for key in self.list_keys:
            if not key.hidden:
                key.toggle()
                self.original_states.append(key)

        if restore:
            for key in self.original_states:
                key.hidden = not key.hidden
            self.original_states = []

    def hidden_keys(self) -> list[Keybind]:
        """Returns a list of all hidden keybinds."""
        return [key for key in self.list_keys if key.hidden]

    def get_by_code(self, code: int) -> Keybind:
        """
        Returns the keybind with the specified code.

        Raises:
            KeybindError: If no keybind is found with the specified code.
        """
        try:
            key = self.keys[code]
            log.debug(f'found keybind={key.bind}')
            return key
        except KeyError:
            msg = f'No keybind found with {code=}'
            raise KeybindError(msg) from None

    def get_by_bind(self, bind: str) -> Keybind:
        """
        Returns the keybind with the <bind> specified.

        Raises:
            KeybindError: If no keybind is found with the specified bind.
        """
        for key in self.list_keys:
            if key.bind == bind:
                log.debug(f'found keybind={key.bind}')
                return key
        msg = f'No keybind found with {bind=}'
        raise KeybindError(msg) from None

    def get_by_code_list(self, code_list: list[int]) -> list[Keybind]:
        """Returns the keybinds with the specified codes."""
        return [self.get_by_code(code) for code in code_list]

    def get_by_bind_list(self, bind_list: list[str]) -> list[Keybind]:
        """Returns the keybinds with the specified binds."""
        return [self.get_by_bind(bind) for bind in bind_list]

    def unregister_by_code(self, code_list: list[int]) -> list[Keybind]:
        """Removes the keybinds with the specified codes."""
        return [self.unregister(code) for code in code_list]

    def unregister_by_bind(self, bind_list: list[str]) -> list[Keybind]:
        """Removes the keybinds with the specified binds."""
        return [self.unregister(self.get_by_bind(bind).code) for bind in bind_list]

    def unregister_by_list(self, key_list: list[Keybind]) -> list[Keybind]:
        """Removes the specified keybinds."""
        return [self.unregister(k.code) for k in key_list]

    def __str__(self) -> str:
        return '\n'.join([str(k) for k in self.list_keys])

    def __repr__(self):
        return self.__str__()
