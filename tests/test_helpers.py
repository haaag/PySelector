# test_helpers.py

from typing import NamedTuple
from typing import Type
from typing import Union

import pytest
from pyselector import helpers
from pyselector.interfaces import ExecutableNotFoundError


class Case(NamedTuple):
    input: Union[str, bytes]
    expected: Union[str, int, Type[ExecutableNotFoundError]]


def test_check_command_success() -> None:
    case = Case(input="cat", expected="/bin/cat")
    command = helpers.check_command(
        name=case.input,
        reference="...",
    )
    assert command == case.expected


def test_check_command_failure() -> None:
    case = Case(input="i_dont_exists", expected=ExecutableNotFoundError)
    with pytest.raises(case.expected):
        helpers.check_command(name=case.input, reference=case.input)


@pytest.mark.parametrize(
    "input",
    (
        b"Testing line",
        b"Another line",
    ),
)
def test_parse_single_bytes_line(input) -> None:
    line = helpers.parse_bytes_line(input)
    assert isinstance(input, bytes)
    assert isinstance(line, str)


@pytest.mark.parametrize(
    ("input", "expected"),
    (
        Case(input=b"Testing", expected=1),
        Case(input=b"Testing\nLines\nAnother", expected=3),
        Case(input=b"Testing\nFour\nLines\nAnother", expected=4),
    ),
)
def test_parse_mutitple_bytes_lines(input, expected) -> None:
    lines = helpers.parse_multiple_bytes_lines(input)
    assert isinstance(lines, list)
    assert len(lines) == expected
