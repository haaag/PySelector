# interface.py
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import Protocol
from typing import Sequence
from typing import TypeVar

from pyselector import constants
from pyselector import helpers

if TYPE_CHECKING:
    from pyselector.key_manager import KeyManager

T = TypeVar('T')
PromptReturn = tuple[T, int]


@dataclass
class Arg:
    param: str
    help: str
    type: type


class MenuInterface(Protocol):
    name: str
    url: str
    keybind: KeyManager

    @property
    def command(self) -> str:
        """Returns the command to execute for the menu."""

    @helpers.deprecated("method will be deprecated. use 'select' method")
    def prompt(
        self,
        items: list[Any] | tuple[Any] | None = None,
        case_sensitive: bool | None = None,
        multi_select: bool = False,
        prompt: str = constants.PROMPT,
        preprocessor: Callable[..., Any] = lambda x: str(x),
        **kwargs,
    ) -> PromptReturn: ...

    def select(
        self,
        items: Sequence[T],
        hide_keys: bool = False,
        **kwargs,
    ) -> PromptReturn:
        """Shows items in the menu and returns the selected item"""

    def input(self, prompt: str = constants.PROMPT, **kwargs) -> str | None:
        """Shows a prompt in the menu and returns the user's input"""

    def confirm(
        self,
        question: str,
        options: Sequence[str] = ('Yes', 'No'),
        confirm_opts: Sequence[str] = ('Yes'),
        **kwargs,
    ) -> bool:
        """Prompt the user with a question and a list of options."""

    def supported(self) -> str:
        """Shows a list of supported arguments for the menu"""
