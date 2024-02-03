# menu.py

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyselector.interfaces import MenuInterface

logger = logging.getLogger(__name__)


REGISTERED_MENUS: dict[str, type[MenuInterface]] = {}


class Menu:
    @staticmethod
    def register(name: str, menu: type[MenuInterface]) -> None:
        logger.debug(f'Menu.register: {name =}')
        REGISTERED_MENUS[name] = menu

    @staticmethod
    def registered() -> dict[str, type[MenuInterface]]:
        return REGISTERED_MENUS

    @staticmethod
    def get(name: str) -> MenuInterface:
        try:
            menu = REGISTERED_MENUS[name]
        except KeyError as e:
            err_msg = f'Unknown menu: {name!r}'
            logger.error(err_msg)
            raise ValueError(err_msg) from e
        return menu()
