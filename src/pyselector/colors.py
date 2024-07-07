# colors.py
#
# https://pypi.org/project/xlib/

from __future__ import annotations

import logging
from contextlib import suppress
from functools import lru_cache

from PIL import ImageColor
from Xlib.display import Display
from Xlib.error import DisplayNameError
from Xlib.Xatom import RESOURCE_MANAGER
from Xlib.Xatom import STRING

logger = logging.getLogger(__name__)


@lru_cache
def load_colors() -> dict[str, str]:
    with suppress(DisplayNameError):
        logger.debug('loading colors from X11')
        res_prop = Display().screen().root.get_full_property(RESOURCE_MANAGER, STRING)
        res_kv = (line.split(':', 1) for line in res_prop.value.decode().split('\n'))
        return {kv[0]: kv[1].strip() for kv in res_kv if len(kv) == 2}  # noqa: PLR2004
    logger.debug('no colors found in X11')
    return {}


def rgb(color: str) -> str:
    rgb_tuple = ImageColor.getcolor(color, 'RGB')
    return ';'.join(str(value) for value in rgb_tuple)


class Color:
    @staticmethod
    def _colors() -> dict[str, str]:
        return load_colors()

    @staticmethod
    def background(default: str = 'black') -> str:
        return Color._colors().get('*.color0', default)

    @staticmethod
    def foreground(default: str = 'white') -> str:
        return Color._colors().get('*.color15', default)

    @staticmethod
    def black(default: str = 'black') -> str:
        return Color._colors().get('*.color0', default)

    @staticmethod
    def grey(default: str = 'grey') -> str:
        return Color._colors().get('*.color8', default)

    @staticmethod
    def dark_red(default: str = 'red') -> str:
        return Color._colors().get('*.color1', default)

    @staticmethod
    def red(default: str = 'red') -> str:
        return Color._colors().get('*.color9', default)

    @staticmethod
    def dark_green(default: str = 'green') -> str:
        return Color._colors().get('*.color2', default)

    @staticmethod
    def green(default: str = 'green') -> str:
        return Color._colors().get('*.color10', default)

    @staticmethod
    def dark_yellow(default: str = 'yellow') -> str:
        return Color._colors().get('*.color3', default)

    @staticmethod
    def yellow(default: str = 'yellow') -> str:
        return Color._colors().get('*.color11', default)

    @staticmethod
    def dark_blue(default: str = 'blue') -> str:
        return Color._colors().get('*.color4', default)

    @staticmethod
    def blue(default: str = 'blue') -> str:
        return Color._colors().get('*.color12', default)

    @staticmethod
    def dark_magenta(default: str = 'magenta') -> str:
        return Color._colors().get('*.color5', default)

    @staticmethod
    def magenta(default: str = 'magenta') -> str:
        return Color._colors().get('*.color13', default)

    @staticmethod
    def dark_cyan(default: str = 'cyan') -> str:
        return Color._colors().get('*.color6', default)

    @staticmethod
    def cyan(default: str = 'cyan') -> str:
        return Color._colors().get('*.color14', default)

    @staticmethod
    def light_grey(default: str = 'grey') -> str:
        return Color._colors().get('*.color7', default)

    @staticmethod
    def white(default: str = 'white') -> str:
        return Color._colors().get('*.color15', default)


SUPPORTED_COLORS = {
    'foreground': rgb(Color.foreground()),
    'background': rgb(Color.background()),
    'black': rgb(Color.black()),
    'grey': rgb(Color.grey()),
    'red': rgb(Color.red()),
    'dark_red': rgb(Color.dark_red()),
    'green': rgb(Color.green()),
    'dark_green': rgb(Color.dark_green()),
    'yellow': rgb(Color.yellow()),
    'dark_yellow': rgb(Color.dark_yellow()),
    'blue': rgb(Color.blue()),
    'dark_blue': rgb(Color.dark_blue()),
    'magenta': rgb(Color.magenta()),
    'dark_magenta': rgb(Color.dark_magenta()),
    'cyan': rgb(Color.cyan()),
    'dark_cyan': rgb(Color.dark_cyan()),
    'light_grey': rgb(Color.light_grey()),
    'white': rgb(Color.white()),
}
