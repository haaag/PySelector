# dmenu.py

import logging
import shlex
import warnings
from typing import Iterable
from typing import Optional
from typing import Union

from pyselector import helpers
from pyselector.interfaces import PromptReturn
from pyselector.key_manager import KeyManager

log = logging.getLogger(__name__)


class Dmenu:
    def __init__(self) -> None:
        self.name = "dmenu"
        self.url = "https://tools.suckless.org/dmenu/"
        self.keybind = KeyManager()

    @property
    def command(self) -> str:
        return helpers.check_command(self.name, self.url)

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
            lines   (int): dmenu lists items vertically, with the given number of lines.
            bottom  (str): dmenu appears at the bottom of the screen.
            font    (str): defines the font or font set used.
            height  (str): The height of the selection window (e.g. 50%).

        Returns:
            A tuple containing the selected item (str or list of str) and the return code (int).
        """
        if items is None:
            items = []

        args = shlex.split(self.command)

        if kwargs.get("lines"):
            args.extend(["-l", str(kwargs.pop("lines"))])

        if prompt:
            args.extend(["-p", prompt])

        if kwargs.get("bottom"):
            kwargs.pop("bottom")
            args.append("-b")

        if case_sensitive:
            args.append("-i")

        if kwargs.get("font"):
            args.extend(["-fn", kwargs.pop("font")])

        if multi_select:
            log.warning("not supported in dmenu: %s", "multi-select")

        if kwargs:
            for arg, value in kwargs.items():
                warnings.warn(UserWarning(f"'{arg}={value}' not supported"))

        selection, code = helpers._execute(args, items)
        return helpers.parse_bytes_line(selection), code