# dmenu.py
from __future__ import annotations

import logging
import shlex
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import Sequence
from typing import TypeVar

from pyselector import constants
from pyselector import helpers
from pyselector.interfaces import Arg
from pyselector.key_manager import KeyManager

if TYPE_CHECKING:
    from pyselector.interfaces import PromptReturn

log = logging.getLogger(__name__)

T = TypeVar('T')

SUPPORTED_ARGS: dict[str, Arg] = {
    'name': Arg('dmenu', 'dmenu', str),
    'url': Arg('url', constants.HOMEPAGE_DMENU, str),
    'prompt': Arg('-p', 'defines the prompt to be displayed to the left of the input field', str),
    'lines': Arg('lines', 'dmenu lists items vertically, with the given number of lines', int),
    'bottom': Arg('bottom', 'dmenu appears at the bottom of the screen', bool),
    # FIX: create _build_font fn
    'fn': Arg('fn', 'defines the font or font set used', str),
    'nb': Arg('nb', 'defines the normal background color', str),
    'nf': Arg('nf', 'defines the normal foreground color', str),
    'sb': Arg('sb', 'defines the selected background color', str),
    'sf': Arg('sf', 'defines the selected foreground color', str),
}


class Dmenu:
    def __init__(self) -> None:
        self.name = 'dmenu'
        self.url = constants.HOMEPAGE_DMENU
        self.keybind = KeyManager()

    @property
    def command(self) -> str:
        return helpers.check_command(self.name, self.url)

    def _build_args(
        self,
        case_sensitive: bool = False,
        multi_select: bool = False,
        prompt: str = constants.PROMPT,
        **kwargs,
    ) -> list[str]:
        args = shlex.split(self.command)

        if kwargs.get('lines'):
            args.extend(['-l', str(kwargs.pop('lines'))])

        if prompt:
            args.extend(['-p', prompt])

        if kwargs.get('bottom'):
            kwargs.pop('bottom')
            args.append('-b')

        if not case_sensitive:
            args.append('-i')

        if kwargs.get('font'):
            args.extend(['-fn', kwargs.pop('font')])

        if multi_select:
            log.debug('not supported in dmenu: %s', 'multi-select')

        for key in self.keybind.list_keys:
            log.debug('key=%s not supported in dmenu', key)

        if kwargs:
            for arg, value in kwargs.items():
                log.debug("'%s=%s' not supported", arg, value)
        return args

    def prompt(
        self,
        items: Sequence[T] | None = None,
        case_sensitive: bool = False,
        multi_select: bool = False,
        prompt: str = constants.PROMPT,
        preprocessor: Callable[..., Any] = lambda x: str(x),
        **kwargs,
    ) -> PromptReturn:
        """Prompts the user with a rofi window containing the given items
           and returns the selected item and code.

        Args:
            items (Sequence[str, int], optional):  The items to display in the rofi window
            case_sensitive (bool, optional):       Whether or not to perform a case-sensitive search
            multi_select (bool, optional):         Whether or not to allow the user to select multiple items
            prompt (str, optional):                The prompt to display in the rofi window
            **kwargs:                              Additional keyword arguments.

        Keyword Args:
            lines   (int): dmenu lists items vertically, with the given number of lines.
            bottom  (str): dmenu appears at the bottom of the screen.
            font    (str): defines the font or font set used.
            height  (str): The height of the selection window (e.g. 50%).

        Returns:
            A tuple containing the selected item (str or list of str) and the return code (int).
        """
        helpers.check_type(items)

        if items is None:
            items = []

        args = self._build_args(case_sensitive, multi_select, prompt, **kwargs)
        selected, code = helpers.run(args, items, preprocessor)

        if not selected:
            return None, code

        result: Any = None
        for item in items:
            if preprocessor(item) == selected:
                result = item
                break

        if not result:
            log.warning('result is empty')
            return selected, 1

        return result, code

    def supported(self) -> str:
        return '\n'.join(f'{k:<10} {v.type.__name__.upper():<5} {v.help}' for k, v in SUPPORTED_ARGS.items())
