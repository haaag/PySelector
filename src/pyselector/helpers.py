# helpers.ey

from __future__ import annotations

import logging
import re
import shutil
import subprocess
from typing import Any
from typing import Callable
from typing import Sequence
from typing import TypeVar

from pyselector.interfaces import ExecutableNotFoundError
from pyselector.interfaces import UserCancel

logger = logging.getLogger(__name__)

T = TypeVar('T')


def check_command(name: str, reference: str) -> str:
    command = shutil.which(name)
    if not command:
        msg = f"command '{name}' not found in $PATH ({reference})"
        raise ExecutableNotFoundError(msg)
    return command


def check_type(items: Sequence[T]) -> None:
    items_type = type(items).__name__
    if not isinstance(items, (tuple, list)):
        msg = f'items must be a tuple or list, got a {items_type}.'
        raise ValueError(msg)
    if not isinstance(items, Sequence):
        msg = f'items must be a sequence or indexable, got a {items_type}.'
        raise ValueError(msg)


def run(
    args: list[str],
    items: Sequence[T],
    preprocessor: Callable[..., Any],
) -> tuple[str | None, int]:
    logger.debug('executing: %s', args)

    with subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    ) as proc:
        input_items = '\n'.join(map(preprocessor, items))
        selected, _ = proc.communicate(input=input_items)
        return_code = proc.wait()

    if not selected:
        return None, return_code
    selected = selected.strip()

    if return_code == UserCancel(1):
        return selected, return_code

    return selected, return_code


def remove_color_codes(text: str) -> str:
    """
    Removes ANSI escape codes representing color information from a string.

    Args:
        text (str): The text potentially containing ANSI color codes.

    Returns:
        str: The text with color codes removed.
    """

    color_code_pattern = r'\033\[[\d;]*m'
    return re.sub(color_code_pattern, '', text)
