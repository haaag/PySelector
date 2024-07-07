# interface.py
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import NewType
from typing import Protocol
from typing import Sequence
from typing import TypeVar

from pyselector.constants import PROMPT

if TYPE_CHECKING:
    from pyselector.key_manager import KeyManager

T = TypeVar('T')
PromptReturn = tuple[T, int]
UserConfirms = NewType('UserConfirms', int)
UserCancel = NewType('UserCancel', int)


@dataclass
class Arg:
    param: str
    help: str
    type: type


class ExecutableNotFoundError(Exception):
    pass


class MenuInterface(Protocol):
    name: str
    url: str
    keybind: KeyManager

    @property
    def command(self) -> str:
        """Returns the command to execute for the menu."""

    def prompt(
        self,
        items: list[Any] | tuple[Any] | None = None,
        case_sensitive: bool | None = None,
        multi_select: bool = False,
        prompt: str = PROMPT,
        preprocessor: Callable[..., Any] = lambda x: str(x),
        **kwargs,
    ) -> PromptReturn: ...

    def select(
        self,
        items: Sequence[T],
        hide_keys: bool = False,
        **kwargs,
    ) -> T | None:
        """Shows items in the menu and returns the selected item"""

    def input(self, prompt: str = PROMPT) -> str:
        """Shows a prompt in the menu and returns the user's input"""

    def confirm(self, question: str, options: Sequence[str]) -> bool:
        """Prompt the user with a question and a list of options."""

    def supported(self) -> str:
        """Shows a list of supported arguments for the menu"""
