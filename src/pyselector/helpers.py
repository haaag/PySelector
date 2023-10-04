# helpers.ey

from __future__ import annotations

import logging
import shutil
import subprocess
from typing import Any

from pyselector.interfaces import ExecutableNotFoundError
from pyselector.interfaces import UserCancelSelection

log = logging.getLogger(__name__)


def check_command(name: str, reference: str) -> str:
    command = shutil.which(name)
    if not command:
        msg = f"command '{name}' not found in $PATH ({reference})"
        raise ExecutableNotFoundError(msg)
    return command


def parse_bytes_line(b: bytes) -> str:
    return " ".join(b.decode(encoding="utf-8").split())


def parse_multiple_bytes_lines(b: bytes) -> list[str]:
    multi = b.decode(encoding="utf-8").splitlines()
    return [" ".join(line.split()) for line in multi]


def _execute(args: list[str], items: list[Any] | tuple[Any]) -> tuple[str | None, int]:
    # TODO: Add callback to process `items`
    # Example:
    # lambda item: f'{item.id} - {item.body}'
    log.debug("executing: %s", args)

    with subprocess.Popen(
        args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, text=True
    ) as proc:
        input_items = "\n".join(map(str, items))
        selected, _ = proc.communicate(input=input_items)
        return_code = proc.wait()

    if not selected:
        return None, return_code
    if return_code == UserCancelSelection(1):
        return None, return_code
    return selected, return_code


def parse_selected_items(items: tuple[Any], selected: str) -> list[Any]:
    selected_clean = [item for item in selected.split("\n") if item]
    input_items = "\n".join(map(str, items))
    items_str = input_items.split("\n")
    result = []
    try:
        for selection in selected_clean:
            idx = items_str.index(selection)
            result.append(items[idx])
    except ValueError as err:
        log.warning(err)
        result = selected_clean
    return result
