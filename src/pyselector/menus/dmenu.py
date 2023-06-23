# dmenu.py
from __future__ import annotations

import logging
import shlex
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


class Dmenu:
    def __init__(self) -> None:
        self.name = "dmenu"
        self.url = constants.HOMEPAGE_DMENU
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
        args = shlex.split(self.command)

        if kwargs.get("lines"):
            args.extend(["-l", str(kwargs.pop("lines"))])

        if prompt:
            args.extend(["-p", prompt])

        if kwargs.get("bottom"):
            kwargs.pop("bottom")
            args.append("-b")

        if not case_sensitive:
            args.append("-i")

        if kwargs.get("font"):
            args.extend(["-fn", kwargs.pop("font")])

        if multi_select:
            log.debug("not supported in dmenu: %s", "multi-select")

        for key in self.keybind.registered_keys:
            log.debug("key=%s not supported in dmenu", key)

        if kwargs:
            for arg, value in kwargs.items():
                log.debug("'%s=%s' not supported", arg, value)
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
            lines   (int): dmenu lists items vertically, with the given number of lines.
            bottom  (str): dmenu appears at the bottom of the screen.
            font    (str): defines the font or font set used.
            height  (str): The height of the selection window (e.g. 50%).

        Returns:
            A tuple containing the selected item (str or list of str) and the return code (int).
        """
        if items is None:
            items = []

        args = self._build_command(case_sensitive, multi_select, prompt, **kwargs)

        selection, code = helpers._execute(args, items)
        return helpers.parse_bytes_line(selection), code
