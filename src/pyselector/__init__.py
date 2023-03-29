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

from .selector import Menu as Menu

__version__ = "0.0.7b0"
