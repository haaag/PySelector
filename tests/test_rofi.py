# test_rofi.py

from typing import NamedTuple
from typing import Type
from typing import Union

import pytest
from pyselector.menus.rofi import Rofi


class Case(NamedTuple):
    input: str
    expected: Union[str, Type[Exception]]


@pytest.fixture
def rofi() -> Rofi:
    return Rofi()


@pytest.fixture
def items() -> list[str]:
    return ['Option 1', 'Option 2', 'Option 3']


def test_build_args(rofi) -> None:
    alt_r = rofi.keybind.add(
        bind='alt-r',
        description='Testing add keybind',
        action=lambda: None,
    )
    args = rofi._build_args(
        case_sensitive=True,
        multi_select=True,
        prompt='test>',
        lines=5,
        theme='default',
        mesg='Testing...',
        filter='Testing...',
        location='upper-right',
        width='60%',
        height='50%',
    )

    assert isinstance(args, list)
    assert '-case-sensitive' in args
    assert '-multi-select' in args
    assert '-p' in args
    assert '-l' in args
    assert '-theme' in args
    assert '-mesg' in args
    assert '-filter' in args
    assert f'-kb-custom-{alt_r.id}' in args
    assert '-location' in args
    assert '-theme-str' in args


def test_build_args_not_case_sensitive(rofi: Rofi) -> None:
    args = rofi._build_args(
        case_sensitive=False,
        multi_select=True,
        prompt='test>',
    )
    assert '-i' in args


def test_return_nonzero(rofi: Rofi, items) -> None:
    """Test case user hits escape raises SystemExit"""
    lines, code = rofi.prompt(items=items, prompt='Hit <Escape>', mesg='> Hit <Escape>')

    assert code != 0


def test_multi_lines_selected(rofi, items) -> None:
    """Test case where multi_select is True"""
    lines, _ = rofi.prompt(
        items=items,
        prompt='Select all items with <Shift+Enter>',
        multi_select=True,
        mesg='> Select all items with <Shift+Enter>',
    )
    assert isinstance(lines, list)
    assert len(lines) == 3


def test_case_sensitive(rofi) -> None:
    """Test case where case_sensitive is True"""
    result, _ = rofi.prompt(
        items=['OPTION 1'],
        prompt='Type option with CAPS on>',
        case_sensitive=True,
        mesg='> Type option with CAPS on',
    )
    assert result == 'OPTION 1'


def test_int_items_to_str(rofi) -> None:
    items = [1, 2, 3]
    result, _ = rofi.prompt(items=items, prompt='Select first item>', mesg='> Select first item')
    assert isinstance(result, int)
    assert result == 1


@pytest.mark.parametrize(
    ('input', 'expected'),
    (
        Case(input='upper-left', expected='1'),
        Case(input='left', expected='8'),
        Case(input='bottom-left', expected='7'),
        Case(input='upper-center', expected='2'),
        Case(input='center', expected='0'),
        Case(input='bottom-center', expected='6'),
        Case(input='upper-right', expected='3'),
        Case(input='right', expected='4'),
        Case(input='bottom-right', expected='5'),
    ),
)
def test_rofi_location_success(rofi, input, expected) -> None:
    assert rofi.location(input) == expected


@pytest.mark.parametrize(
    ('input', 'expected'),
    (
        Case(input='upper-bottom', expected=KeyError),
        Case(input='upper-up', expected=KeyError),
    ),
)
def test_rofi_location_failure(rofi, input, expected) -> None:
    with pytest.raises(expected):
        rofi.location(input)
