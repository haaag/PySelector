# helpers.ey

from __future__ import annotations

import logging
import shutil
import subprocess
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Sequence

from pyselector.interfaces import ExecutableNotFoundError
from pyselector.interfaces import UserCancelSelection

logger = logging.getLogger(__name__)


def check_command(name: str, reference: str) -> str:
    command = shutil.which(name)
    if not command:
        msg = f"command '{name}' not found in $PATH ({reference})"
        raise ExecutableNotFoundError(msg)
    return command


def check_type(items: Iterable[Any]) -> None:
    if not isinstance(items, (tuple, list)):
        msg = 'items must be a tuple or list'
        raise ValueError(msg)
    if not isinstance(items, Iterable):
        msg = 'items must be iterable.'
        raise ValueError(msg)
    if not isinstance(items, Sequence):
        msg = 'items must be a sequence or indexable.'
        raise ValueError(msg)


def _execute(
    args: list[str],
    items: list[Any] | tuple[Any],
    preprocessor: Callable[..., Any] | None = None,
) -> tuple[str | None, int]:
    logger.debug('executing: %s', args)
    check_type(items)

    preprocessor = preprocessor or str

    with subprocess.Popen(
        args,  # noqa: S603
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
    if return_code == UserCancelSelection(1):
        return selected, return_code
    return selected, return_code
