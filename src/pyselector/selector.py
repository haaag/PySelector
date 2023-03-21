# menu.py

import logging

from pyselector import logger
from pyselector.menus.dmenu import Dmenu
from pyselector.menus.fzf import Fzf
from pyselector.menus.rofi import Rofi


class Menu:
    @staticmethod
    def rofi() -> Rofi:
        return Rofi()

    @staticmethod
    def dmenu() -> Dmenu:
        return Dmenu()

    @staticmethod
    def fzf() -> Fzf:
        return Fzf()

    @staticmethod
    def set_logging_level(verbose: bool = False) -> None:
        logging.basicConfig(
            level=logging.DEBUG if verbose else logging.INFO,
            format="%(levelname)s %(name)s - %(message)s",
            handlers=[logger.handler],
        )
