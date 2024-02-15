# interface.py
from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import NewType
from typing import Protocol

if TYPE_CHECKING:
    from pyselector.key_manager import KeyManager

PromptReturn = tuple[Any, int]
UserConfirmsSelection = NewType('UserConfirmsSelection', int)
UserCancelSelection = NewType('UserCancelSelection', int)


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
        items: list[Any] | tuple[Any] | None = None,
        case_sensitive: bool | None = None,
        multi_select: bool = False,
        prompt: str = 'PySelector> ',
        preprocessor: Callable[..., Any] | None = None,
        **kwargs,
    ) -> PromptReturn:
        ...
