# helpers.ey

from __future__ import annotations

import logging
import re
import shutil
import subprocess
import warnings
from functools import wraps
from typing import IO
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Sequence
from typing import TypeVar

from pyselector.constants import UserCancel
from pyselector.exc import ExecutableNotFoundError

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
        text=True,
    ) as proc:
        input_items = '\n'.join(map(preprocessor, items))
        selected, _ = proc.communicate(input=input_items)
        return_code = proc.wait()

    if not selected:
        return None, return_code

    selected = selected.rstrip('\n')
    if return_code == UserCancel(1):
        return selected, return_code

    return selected, return_code


def remove_ansi_codes(text: str) -> str:
    """
    Removes ANSI escape codes representing color information from a string.

    Args:
        text (str): The text potentially containing ANSI color codes.

    Returns:
        str: The text with color codes removed.
    """
    color_code_pattern = r'\033\[[\d;]*m'
    return re.sub(color_code_pattern, '', text)


def write_items_to_stdin(stdin: IO[bytes], items: Iterable[Any], encoding: str, preprocessor: Callable[..., Any]):
    byte = None
    newline_char = '\n'
    return_char = '\r'
    for item in items:
        line = preprocessor(item)
        byte = _check_byte_encoding(line, byte, newline_char, return_char)
        if not byte:
            line = line.encode(encoding)
        stdin.write(line + b'\n')
        stdin.flush()


def _check_byte_encoding(line: Any, byte: bool | None, newline_char: str | bytes, return_char: str | bytes) -> bool:
    if byte is None:
        byte = isinstance(line, bytes)
        if byte:
            newline_char = b'\n'
            return_char = b'\r'
    elif isinstance(line, bytes) is not byte:
        msg = f'element values must be all byte strings or all unicode strings, not mixed of them: {line}'
        raise ValueError(msg)
    if newline_char in line or return_char in line:
        msg = rf'element values must not contain CR({return_char!r})/' rf'LF({newline_char!r}): {line!r}'
        raise ValueError(msg)
    return byte


def read_output_from_stdout(stdout: IO[bytes], encoding: str) -> tuple[str, str]:
    # FIX: type: mypy: "IO[bytes]" has no attribute "peek"
    byte = isinstance(stdout.peek(1), bytes)  # type: ignore[attr-defined]
    decode = (lambda b: b.decode(encoding)) if byte else (lambda t: t)
    return tuple(decode(ln.strip(b'\r\n\0')) for ln in iter(stdout.readline, b''))


def deprecated(mesg: str) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            warnings.warn(f'{func.__name__!r} {mesg}', DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        return wrapper

    return decorator
