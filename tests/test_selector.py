import pytest
from pyselector import Menu
from pyselector.menus.dmenu import Dmenu
from pyselector.menus.fzf import Fzf
from pyselector.menus.rofi import Rofi


@pytest.fixture
def menu() -> Menu:
    return Menu()


def test_get_rofi(menu) -> None:
    rofi = menu.get('rofi')
    assert isinstance(rofi, Rofi)


def test_get_dmenu(menu) -> None:
    dmenu = menu.get('dmenu')
    assert isinstance(dmenu, Dmenu)


def test_get_fzf(menu) -> None:
    fzf = menu.get('fzf')
    assert isinstance(fzf, Fzf)
