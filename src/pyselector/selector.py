# menu.py

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from pyselector import logger

if TYPE_CHECKING:
    from pyselector.interfaces import MenuInterface

log = logging.getLogger(__name__)


REGISTERED_MENUS: dict[str, type[MenuInterface]] = {}


class Menu:
    @staticmethod
    def register(name: str, menu: type[MenuInterface]) -> None:
        log.debug(f"Menu.register.keybind: {name =} {menu.keybind =}")
        REGISTERED_MENUS[name] = menu

    @staticmethod
    def registered() -> dict[str, type[MenuInterface]]:
        return REGISTERED_MENUS

    @staticmethod
    def get(name: str) -> MenuInterface:
        try:
            menu = REGISTERED_MENUS[name]
        except KeyError as e:
            err_msg = f"Unknown menu: {name!r}"
            log.error(err_msg)
            raise ValueError(err_msg) from e
        return menu()

    @staticmethod
    def logging_debug(verbose: bool = False) -> None:
        logging.basicConfig(
            level=logging.DEBUG if verbose else logging.INFO,
            format="%(levelname)s %(name)s - %(message)s",
            handlers=[logger.handler],
        )
