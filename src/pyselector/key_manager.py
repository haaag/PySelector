# keybinds.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from typing import Callable
from typing import Optional


class KeybindError(Exception):
    pass


@dataclass(kw_only=True)
class Keybind:
    """
    Represents a keybind, which associates a keyboard key or
    combination of keys with a callback function.

    Attributes:
        id      (int): The unique identifier of the keybind.
        bind    (str): The key or key combination that triggers the keybind.
        code    (int): The unique code of the keybind.
        description (str): A brief description of the keybind.
        action  (Optional[str]): An optional action associated with the keybind. Defaults to an empty string.
        hidden  (bool): Whether the keybind is hidden from the user interface. Defaults to True.
        callback (Optional[Callable[..., Any]]): The function to call when the keybind is triggered. Defaults to None.

    Methods:
        toggle_hidden(): Toggles the visibility of the keybind in the user interface.
    """

    id: int
    bind: str
    code: int
    description: str
    action: Optional[str] = ""
    hidden: bool = True
    callback: Optional[Callable[..., Any]] = None

    def toggle_hidden(self) -> None:
        self.hidden = not self.hidden

    def __hash__(self):
        return hash((self.code, self.description))


class KeyManager:
    """
    A class for managing keybinds, which are associations between key combinations
    and callback functions.

    Attributes:
        keys        (dict[str, Keybind]): A dictionary mapping keybinds to their corresponding `Keybind` objects.
        key_count   (int): A counter for assigning unique IDs to newly added keybinds.
        code_count  (int): A counter for assigning unique codes to newly added keybinds.
        temp_hidden (list[Keybind]): A list of temporarily hidden keybinds.
    """

    def __init__(self) -> None:
        self.keys: dict[int, Keybind] = {}
        self.key_count = 1
        self.code_count = 1
        self.temp_hidden: list[Keybind] = []
        self.original_states: dict[Keybind, bool] = {}

    def add(
        self,
        key: str,
        description: str,
        callback: Callable[..., Any],
        hidden: bool = False,
        exist_ok: bool = False,
    ) -> Keybind:
        """
        Registers a new keybind with the specified bind and description,
        and associates it with the specified callback function.

        Args:
            key         (str): The bind of the keybind.
            description (str): The description of the keybind.
            callback    (Callable[..., Any]): The function to call when the keybind is triggered.
            hidden      (bool): Whether the keybind should be hidden from the user interface. Defaults to False.
            exist_ok    (bool): Whether to overwrite an existing keybind with the same bind. Defaults to False.
        """
        return self.register(
            Keybind(
                id=self.key_count,
                bind=key,
                code=self.code_count,
                description=description,
                hidden=hidden,
                callback=callback,
            ),
            exist_ok=exist_ok,
        )

    def unregister(self, code: int) -> None:
        """Removes the keybind with the specified bind."""
        if not self.keys.get(code):
            raise KeybindError(f"No keybind found with {code=}")
        self.keys.pop(code)

    def unregister_all(self) -> None:
        """Removes all registered keybinds."""
        self.keys.clear()

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
        if exist_ok and self.keys.get(key.code):
            self.unregister(key.code)

        if self.keys.get(key.code):
            raise KeybindError(f"{key.bind=} already registered")

        self.key_count += 1
        self.code_count += 1
        self.keys[key.code] = key
        return key

    @property
    def registered_keys(self) -> list[Keybind]:
        return list(self.keys.values())

    def toggle_all(self) -> None:
        """Toggles the "hidden" property of all non-hidden keybinds."""
        for key in self.registered_keys:
            if not key.hidden:
                key.hidden = True

    def toggle_hidden(self, restore: bool = False) -> None:
        """
        Toggles the "hidden" property of all non-hidden keybinds, and
        temporarily stores the original "hidden" state of each keybind.
        If `restore` is True, restores the original "hidden" state of each keybind.
        """
        for key in self.registered_keys:
            if not key.hidden:
                key.toggle_hidden()
                self.temp_hidden.append(key)
        if restore:
            for key in self.temp_hidden:
                key.toggle_hidden()
            self.temp_hidden = []

    def toggle_nonhidden_keys(self, restore: bool = False) -> None:
        """
        Toggles the "hidden" property of all non-hidden keybinds, and temporarily
        stores the original "hidden" state of each keybind. If `restore` is True,
        restores the original "hidden" state of each keybind.
        """
        if not restore:
            self.original_states = {
                key: key.hidden for key in self.registered_keys if not key.hidden
            }

        for key in self.registered_keys:
            if not key.hidden:
                key.toggle_hidden()

        if restore:
            try:
                for key, state in self.original_states.items():
                    if state:
                        key.toggle_hidden()
            finally:
                self.original_states.clear()

    def get_keybind_by_code(self, code: int) -> Keybind:
        """
        Returns the keybind with the specified code.

        Raises:
            KeybindError: If no keybind is found with the specified code.
        """
        try:
            return self.keys[code]
        except KeyError:
            raise KeybindError(f"No keybind found with {code=}") from None
