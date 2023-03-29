import pytest
from pyselector import Menu
from pyselector.menus.dmenu import Dmenu
from pyselector.menus.fzf import Fzf
from pyselector.menus.rofi import Rofi


@pytest.fixture
def menu() -> Menu:
    return Menu()


def test_get_rofi(menu) -> None:
    assert isinstance(menu.rofi(), Rofi)


def test_get_dmenu(menu) -> None:
    assert isinstance(menu.dmenu(), Dmenu)


def test_get_fzf(menu) -> None:
    assert isinstance(menu.fzf(), Fzf)
