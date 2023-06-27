# helpers.ey

from __future__ import annotations

import logging
import shutil
import subprocess
import sys
from typing import Iterable
from typing import Union

from pyselector.interfaces import ExecutableNotFoundError

# ENCODE = sys.getdefaultencoding()


log = logging.getLogger(__name__)


def check_command(name: str, reference: str) -> str:
    command = shutil.which(name)
    if not command:
        raise ExecutableNotFoundError(
            f"command '{name}' not found in $PATH ({reference})"
        )
    return command


def parse_bytes_line(b: bytes) -> str:
    return " ".join(b.decode(encoding="utf-8").split())


def parse_multiple_bytes_lines(b: bytes) -> list[str]:
    multi = b.decode(encoding="utf-8").splitlines()
    return [" ".join(line.split()) for line in multi]


def get_clipboard_data() -> str:
    """Read clipboard to add a new bookmark."""
    with subprocess.Popen(
        ["xclip", "-selection", "clipboard", "-o"],
        stdout=subprocess.PIPE,
    ) as proc:
        data = proc.stdout.read()
    return data.decode("utf-8")


def set_clipboard_data(url: str) -> None:
    """Copy selected bookmark to the system clipboard."""
    data = bytes(url, "utf-8")
    with subprocess.Popen(
        ["xclip", "-selection", "clipboard"],
        stdin=subprocess.PIPE,
    ) as proc:
        proc.stdin.write(data)
        log.debug("copied '%s' to clipboard", url)


def _execute(args: list[str], items: Iterable[Union[str, int]]) -> tuple[bytes, int]:
    log.debug("executing: %s", args)
    with subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
    ) as proc:
        items_str = list(map(str, items))
        bytes_items = "\n".join(items_str).encode(encoding="utf-8")
        selected, _ = proc.communicate(input=bytes_items)
        return_code = proc.wait()

    if not selected:
        sys.exit(0)
    log.debug("item selected: %s", selected)
    return selected, return_code
