# fzf.py
from __future__ import annotations

import logging
import shlex
from typing import Iterable
from typing import Optional
from typing import Union

from pyselector import helpers
from pyselector.key_manager import KeyManager

log = logging.getLogger(__name__)


class Fzf:
    def __init__(self) -> None:
        self.name = "fzf"
        self.url = "https://github.com/junegunn/fzf"
        self.keybind = KeyManager()

    @property
    def command(self) -> str:
        return helpers.check_command(self.name, self.url)

    def _build_command(
        self,
        case_sensitive,
        multi_select,
        prompt,
        **kwargs,
    ) -> list[str]:
        header: list[str] = []
        args = shlex.split(self.command)

        if case_sensitive is not None:
            args.append("+i" if case_sensitive else "-i")

        if kwargs.get("mesg"):
            header.extend(shlex.split(f"'{kwargs.pop('mesg')}'"))

        if kwargs.get("cycle"):
            kwargs.pop("cycle")
            args.append("--cycle")

        if not kwargs.pop("preview", None):
            args.append("--no-preview")

        if kwargs.get("height"):
            args.extend(shlex.split(f"--height {kwargs.pop('height')}"))

        if prompt:
            args.extend(["--prompt", prompt])

        if multi_select:
            args.append("--multi")

        # FIX: rethink keybinds for FZF
        log.debug("keybinds are disabled")
        for key in self.keybind.list_registered:
            args.extend(shlex.split(f"--bind='{key.bind}:{key.action}'"))
            if not key.hidden:
                header.append(f"Use {key.bind} {key.description}")

        if kwargs:
            for arg, value in kwargs.items():
                log.debug("'%s=%s' not supported", arg, value)

        if header:
            mesg = "\n".join(msg.replace("\n", " ") for msg in header)
            args.extend(shlex.split(f"--header '{mesg}'"))

        return args

    def prompt(
        self,
        items: Optional[Iterable[Union[str, int]]] = None,
        case_sensitive: bool = None,
        multi_select: bool = False,
        prompt: str = "PySelector> ",
        **kwargs,
    ) -> tuple[Union[str, list[str]], int]:
        if not items:
            items = []

        args = self._build_command(case_sensitive, multi_select, prompt, **kwargs)
        selection, code = helpers._execute(args, items)

        if multi_select:
            return helpers.parse_multiple_bytes_lines(selection), code
        return helpers.parse_bytes_line(selection), code
