# menus.rofi.py
from __future__ import annotations

import logging
import shlex
import sys
from typing import TYPE_CHECKING
from typing import Iterable
from typing import Optional
from typing import Union

from pyselector import constants
from pyselector import helpers
from pyselector.key_manager import KeyManager

if TYPE_CHECKING:
    from pyselector.interfaces import PromptReturn


log = logging.getLogger(__name__)

ROFI_RETURN_CODE_START = 10
BULLET = "\u2022"


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
        self.name = "rofi"
        self.url = constants.HOMEPAGE_ROFI
        self.keybind = KeyManager()

        self.keybind.code_count = ROFI_RETURN_CODE_START

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
        messages: list[str] = []
        dimensions_args: list[str] = []
        args = []

        args.extend(shlex.split(self.command))
        args.append("-dmenu")
        args.append("-sync")

        if kwargs.get("theme"):
            args.extend(["-theme", kwargs.pop("theme")])

        if kwargs.get("lines"):
            args.extend(["-l", str(kwargs.pop("lines"))])

        if prompt:
            args.extend(["-p", prompt])

        if kwargs.get("markup"):
            del kwargs["markup"]
            args.append("-markup-rows")

        if kwargs.get("mesg"):
            messages.extend(shlex.split(f"'{kwargs.pop('mesg')}'"))

        if kwargs.get("filter"):
            args.extend(["-filter", kwargs.pop("filter")])

        if kwargs.get("location"):
            direction = kwargs.pop("location")
            args.extend(["-location", self.location(direction)])

        if kwargs.get("width"):
            dimensions_args.append(f"width: {kwargs.pop('width')};")

        if kwargs.get("height"):
            dimensions_args.append(f"height: {kwargs.pop('height')};")

        if case_sensitive:
            args.append("-case-sensitive")
        else:
            args.append("-i")

        if multi_select:
            args.append("-multi-select")

        if dimensions_args:
            formated_string = " ".join(dimensions_args)
            args.extend(shlex.split("-theme-str 'window {" + formated_string + "}'"))

        for key in self.keybind.registered_keys:
            args.extend(shlex.split(f"-kb-custom-{key.id} {key.bind}"))
            if not key.hidden:
                messages.append(f"{BULLET} Use <{key.bind}> {key.description}")

        if messages:
            mesg = "\n".join(messages)
            args.extend(shlex.split(f"-mesg '{mesg}'"))

        if kwargs:
            for arg, value in kwargs.items():
                log.debug("'%s=%s' not supported", arg, value)

        title_markup = "true" if kwargs.pop("title_markup", False) else "false"
        args.extend(shlex.split(f"-theme-str 'textbox {{ markup: {title_markup};}}'"))

        return args

    def prompt(
        self,
        items: Optional[Iterable[Union[str, int]]] = None,
        case_sensitive: bool = False,
        multi_select: bool = False,
        prompt: str = "PySelector> ",
        **kwargs,
    ) -> PromptReturn:
        """Prompts the user with a rofi window containing the given items
           and returns the selected item and code.

        Args:
            items (Iterable[str, int], optional):  The items to display in the rofi window
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
            A tuple containing the selected item (str or list of str if `multi_select` enabled) and the return code (int).

        Return Code Value
            0: Row has been selected accepted by user.
            1: User cancelled the selection.
            10-28: Row accepted by custom keybinding.
        """
        if items is None:
            items = []

        args = self._build_command(case_sensitive, multi_select, prompt, **kwargs)
        selection, code = helpers._execute(args, items)

        if multi_select:
            return helpers.parse_multiple_bytes_lines(selection), code
        return helpers.parse_bytes_line(selection), code

    @staticmethod
    def location(direction: Optional[str] = None) -> str:
        """
        Specify where the window should be located. The numbers map to the
        following locations on screen:

            1 2 3
            8 0 4
            7 6 5

        Default: 0
        """
        try:
            location = {
                "upper-left": 1,
                "left": 8,
                "bottom-left": 7,
                "upper-center": 2,
                "center": 0,
                "bottom-center": 6,
                "upper-right": 3,
                "right": 4,
                "bottom-right": 5,
            }
            return str(location[direction])
        except KeyError as e:
            raise KeyError(
                "location %s not found.\nchosse from %s", e, list(location.keys())
            ) from e
            sys.exit(1)
