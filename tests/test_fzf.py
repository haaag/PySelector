# test_fzf.py

import pytest
from pyselector.menus.fzf import Fzf


@pytest.fixture
def fzf() -> Fzf:
    return Fzf()


def test_check_command(fzf) -> None:
    assert 'fzf' in fzf.command


def test_build_args(fzf) -> None:
    args = fzf._build_args(
        case_sensitive=True,
        multi_select=True,
        prompt='Testing>',
    )
    assert '+i' in args
    assert '--prompt' in args
    assert '--multi' in args


def test_build_args_kwargs(fzf) -> None:
    args = fzf._build_args(
        case_sensitive=True,
        multi_select=False,
        prompt='Testing>',
        mesg='Testing...',
        height='40%',
        cycle=True,
        preview=True,
    )
    assert '--prompt' in args
    assert '--header' in args
    assert '--cycle' in args
    assert '--no-preview' not in args
    assert '--multi' not in args
    assert '--height' in args


def test_build_args_header(fzf) -> None:
    args = fzf._build_args(
        case_sensitive=True,
        multi_select=False,
        prompt='Testing>',
        mesg='Testing>',
    )
    assert '--header' in args


def test_build_args_multi_select(fzf) -> None:
    args = fzf._build_args(
        case_sensitive=True,
        multi_select=True,
        prompt='Testing>',
        preview=False,
        height='40%',
        invalid_arg=True,
    )
    assert '--no-preview' in args
    assert '--multi' in args
    assert '--height' in args
