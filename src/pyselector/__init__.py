"""
A module for selecting options from a list using various menu implementations.

Menus available:
- Rofi
- Dmenu (work-in-progress)
- Fzf (work-in-progress)

Usage:

options = ["a", "b", "c"]
menu = pyselector.Menu.rofi()
menu.keybind.add(
    key="alt-n",
    description="sort by recent",
    callback=lambda: None,
    hidden=False,
)
selected_option, keycode = menu.prompt(options)
"""
from __future__ import annotations

from .menus.dmenu import Dmenu
from .menus.fzf import Fzf
from .menus.rofi import Rofi
from .selector import Menu as Menu

Menu.register("dmenu", Dmenu)
Menu.register("rofi", Rofi)
Menu.register("fzf", Fzf)

__version__ = "0.0.14b0"
