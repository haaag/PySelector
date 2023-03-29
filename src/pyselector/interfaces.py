# interface.py
from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Iterable
from typing import Optional
from typing import Protocol
from typing import Union

if TYPE_CHECKING:
    from pyselector.key_manager import KeyManager

PromptReturn = tuple[Union[str, list[str]], int]


class ExecutableNotFoundError(Exception):
    pass


class MenuInterface(Protocol):
    name: str
    url: str
    keybind: KeyManager

    @property
    def command(self) -> str:
        ...

    def prompt(
        self,
        items: Optional[Iterable[Union[str, int]]] = None,
        case_sensitive: bool = None,
        multi_select: bool = False,
        prompt: str = "PySelector> ",
        **kwargs,
    ) -> PromptReturn:
        ...
