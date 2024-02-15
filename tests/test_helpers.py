# test_helpers.py

import shutil
from typing import Any
from typing import Iterable
from typing import NamedTuple
from typing import Type
from typing import Union

import pytest
from pyselector import helpers
from pyselector.interfaces import ExecutableNotFoundError


class Case(NamedTuple):
    input: Union[str, Iterable[Any]]
    expected: Union[str, int, Type[ExecutableNotFoundError], None]


def test_check_command_success() -> None:
    cat = 'cat'
    cmd = shutil.which(cat)

    if not cmd:
        cmd = '/usr/bin/cat'

    case = Case(input=cat, expected=cmd)
    command = helpers.check_command(
        name=case.input,
        reference='...',
    )
    assert command == case.expected


def test_check_command_failure() -> None:
    case = Case(input='i_dont_exists', expected=ExecutableNotFoundError)
    with pytest.raises(case.expected):
        helpers.check_command(name=case.input, reference=case.input)


@pytest.mark.parametrize(
    'input, expected',
    [
        Case(
            input='not a iterable',
            expected=ValueError,
        ),
        Case(
            input=[],
            expected=None,
        ),
    ],
)
def test_check_type(input, expected):
    if expected is None:
        assert helpers.check_type(input) is None
        return

    with pytest.raises(expected):
        helpers.check_type(input)
