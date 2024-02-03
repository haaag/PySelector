import pytest
from pyselector.menus.dmenu import Dmenu


@pytest.fixture
def dmenu() -> Dmenu:
    return Dmenu()


def test_build_command(dmenu) -> None:
    args = dmenu._build_command(
        case_sensitive=True,
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


# def test_build_command_warning(dmenu) -> None:
#     with pytest.warns(UserWarning):
#         _ = dmenu._build_command(
#             case_sensitive=True,
#             multi_select=True,
#             prompt="RaisesUserWarning",
#         )
#
#     with pytest.warns(UserWarning):
#         _ = dmenu._build_command(
#             case_sensitive=True,
#             multi_select=True,
#             prompt="RaisesUserWarning",
#             invalid_arg=True,
#         )


def test_prompt_items_empty(dmenu) -> None:
    dmenu.prompt(prompt='PressEnter>')
