# menu.py

from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from typing import Protocol
from typing import Type

from pyselector import logger

if TYPE_CHECKING:
    from pyselector.key_manager import KeyManager


class MenuInterface(Protocol):
    name: str
    url: str
    keybind: KeyManager

    @property
    def command(self) -> str:
        raise NotImplementedError


REGISTERED_MENUS: dict[str, Type[MenuInterface]] = {}


class Menu:
    @staticmethod
    def register(name: str, menu: Type[MenuInterface]) -> None:
        REGISTERED_MENUS[name] = menu

    @staticmethod
    def registered() -> dict[str, Type[MenuInterface]]:
        return REGISTERED_MENUS

    @staticmethod
    def get(name: str) -> Type[MenuInterface]:
        try:
            menu = REGISTERED_MENUS[name]
        except KeyError as e:
            raise ValueError(f"Unknown menu: {name!r}") from e
        return menu

    @staticmethod
    def logging_debug(verbose: bool = False) -> None:
        logging.basicConfig(
            level=logging.DEBUG if verbose else logging.INFO,
            format="%(levelname)s %(name)s - %(message)s",
            handlers=[logger.handler],
        )
