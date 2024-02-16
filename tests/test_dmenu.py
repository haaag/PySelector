import pytest
from pyselector.menus.dmenu import Dmenu


@pytest.fixture
def dmenu() -> Dmenu:
    return Dmenu()


def test_build_args(dmenu) -> None:
    args = dmenu._build_args(
        case_sensitive=False,
        multi_select=False,
        prompt='Test>',
        lines=10,
        font='sans',
        bottom=True,
    )
    assert '-i' in args
    assert '-p' in args
    assert '-l' in args
    assert '-fn' in args
    assert '-b' in args


def test_prompt_items_empty(dmenu) -> None:
    dmenu.prompt(prompt='HitEnter>')
