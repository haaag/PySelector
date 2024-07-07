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
    action=lambda: None,
    hidden=False,
)
selected_option, keycode = menu.prompt(options)
"""
from __future__ import annotations

from pyselector.menus.dmenu import Dmenu
from pyselector.menus.fzf import Fzf
from pyselector.menus.rofi import Rofi
from pyselector.selector import Menu

Menu.register('dmenu', Dmenu)
Menu.register('rofi', Rofi)
Menu.register('fzf', Fzf)

__version__ = '0.0.35'
