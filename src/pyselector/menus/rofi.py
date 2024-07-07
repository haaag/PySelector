# menus.rofi.py
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
from pyselector.interfaces import UserCancel
from pyselector.key_manager import KeyManager

if TYPE_CHECKING:
    from pyselector.interfaces import PromptReturn


log = logging.getLogger(__name__)

T = TypeVar('T')
ROFI_RETURN_CODE_START = 10

LOCATION = {
    'upper-left': 1,
    'left': 8,
    'bottom-left': 7,
    'upper-center': 2,
    'center': 0,
    'bottom-center': 6,
    'upper-right': 3,
    'right': 4,
    'bottom-right': 5,
}

SUPPORTED_ARGS = {
    'name': Arg('rofi', 'rofi', str),
    'url': Arg('', constants.HOMEPAGE_ROFI, str),
    'markup': Arg('-markup-rows', 'enable markup in rows', bool),
    'prompt': Arg('-p', 'set prompt', str),
    'lines': Arg('-l', 'set number of lines', int),
    'mesg': Arg('-mesg', 'set message', str),
    'location': Arg('-location', f'Specify where the window should be located. {tuple(LOCATION.keys())}', int),
    'width': Arg('-width', 'set width in percentage', str),
    'height': Arg('-height', 'set height in percentage', str),
    'theme': Arg('-theme', 'Path to the new theme file format. This overrides the old theme settings', str),
    'filter': Arg('-filter', 'Filter the list by setting text in input bar to filter', str),
}


def location(direction: str = 'center') -> str:
    """
    Specify where the window should be located. The numbers map to the
    following locations on screen:

        1 2 3
        8 0 4
        7 6 5

    Default: 0
    """
    try:
        return str(LOCATION[direction])
    except KeyError as e:
        msg = 'location %s not found.\nchosse from %s'
        raise KeyError(msg, e, list(LOCATION.keys())) from e


class Rofi:
    """
    A Python wrapper for the rofi application, which provides a simple and
    efficient way to display a list of items for user selection.

    This class provides a convenient interface for building and executing rofi commands,
    allowing customization of various settings such as case sensitivity, multi-select,
    prompt message, and more

    Methods:
        prompt(items=None, case_sensitive=False, multi_select=False, prompt="PySelector> ", **kwargs):
        Displays a rofi selection window with the specified items and settings,
        returns the selected item(s) and return code.
    """

    def __init__(self) -> None:
        self.name = 'rofi'
        self.url = constants.HOMEPAGE_ROFI
        self.keybind = KeyManager()
        self.keybind.code_count = ROFI_RETURN_CODE_START

    @property
    def command(self) -> str:
        return helpers.check_command(self.name, self.url)

    def _build_dimensions(self, kwargs) -> list[str]:
        dimensions: list[str] = []
        w = kwargs.pop('width', None)
        h = kwargs.pop('height', None)

        if not w and not h:
            return dimensions

        if w:
            dimensions.append(f'width: {w};')
        if h:
            dimensions.append(f'height: {h};')

        return shlex.split("-theme-str 'window {" + ' '.join(dimensions) + "}'")

    def _build_mesg(self, kwargs) -> list[str]:
        messages: list[str] = []
        m = kwargs.pop('mesg', None)

        if m:
            messages.extend(shlex.split(shlex.quote(m)))

        for key in self.keybind.list_keys:
            if not key.hidden:
                messages.append(f'{constants.BULLET} Use <{key.bind}> {key.description}')

        if len(messages) == 0:
            return messages

        result = '\n'.join(messages)
        return shlex.split(f'-mesg {shlex.quote(result)}')

    def _build_title_markup(self, kwargs) -> list[str]:
        markup = 'true' if kwargs.pop('title_markup', False) else 'false'
        return shlex.split(f"-theme-str 'textbox {{ markup: {markup};}}'")

    def _build_keybinds(self, args: list[str]) -> None:
        if len(self.keybind.list_keys) == 0:
            return

        for key in self.keybind.list_keys:
            args.extend(shlex.split(f'-kb-custom-{key.id} {key.bind}'))

    def _build_args(
        self,
        case_sensitive: bool = False,
        multi_select: bool = False,
        prompt: str = constants.PROMPT,
        **kwargs,
    ) -> list[str]:
        args = shlex.split(self.command)
        args.extend(['-dmenu', '-sync'])
        args.extend(['-p', prompt])
        args.extend(['-l', str(kwargs.pop('lines', 10))])

        if kwargs.get('theme'):
            args.extend(['-theme', kwargs.pop('theme')])

        if kwargs.pop('markup', False):
            args.append('-markup-rows')

        if kwargs.get('filter'):
            args.extend(['-filter', kwargs.pop('filter')])

        if kwargs.get('location'):
            direction = kwargs.pop('location')
            args.extend(['-location', location(direction)])

        if multi_select:
            args.append('-multi-select')

        self._build_keybinds(args)
        args.append('-case-sensitive' if case_sensitive else '-i')
        args.extend(self._build_dimensions(kwargs))
        args.extend(self._build_mesg(kwargs))
        args.extend(self._build_title_markup(kwargs))

        for arg, value in kwargs.items():
            log.debug("'%s=%s' not supported in '%s'", arg, value, self.name)
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
            lines    (int): The number of lines to display in the selection window.
            mesg     (str): A message to display at the top of the selection window.
            filter   (str): Filter the list by setting text in input bar to filter.
            location (str): The location of the selection window (e.g. "upper-left", "center" or "bottom-right").
            width    (str): The width of the selection window (e.g. 60%).
            height   (str): The height of the selection window (e.g. 50%).
            theme    (str): The path of the rofi theme to use.

        Returns:
            A tuple containing the selected item (str or list of str if `multi_select` enabled)
            and the return code (int).

        Return Code Value
            0: Row has been selected accepted by user.
            1: User cancelled the selection.
            10-28: Row accepted by custom keybinding.
        """
        helpers.check_type(items)

        if items is None:
            items = []

        args = self._build_args(case_sensitive, multi_select, prompt, **kwargs)
        selected, code = helpers.run(args, items, preprocessor)

        if not selected or code == UserCancel(1):
            return None, code

        # 'multi-select' is not supported, for now
        # if multi_select:
        #     result = extract.items(items, selected, preprocessor)
        # else:
        #     result = extract.item(items, selected, preprocessor)

        result: Any = None
        for item in items:
            if preprocessor(item) == selected:
                result = item
                break

        if not result:
            log.debug('result is empty')
            return selected, 1

        return result, code

    def input(self, prompt: str = constants.PROMPT) -> str:
        raise NotImplementedError

    def supported(self) -> str:
        return '\n'.join(f'{k:<10} {v.type.__name__.upper():<5} {v.help}' for k, v in SUPPORTED_ARGS.items())
