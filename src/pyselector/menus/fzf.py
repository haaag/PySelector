# fzf.py
from __future__ import annotations

import logging
import shlex
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable

from pyselector import constants
from pyselector import helpers
from pyselector.interfaces import Arg
from pyselector.key_manager import KeyManager

if TYPE_CHECKING:
    from pyselector.interfaces import PromptReturn

log = logging.getLogger(__name__)

FZF_INTERRUPTED_CODE = 130

SUPPORTED_ARGS: dict[str, Arg] = {
    'prompt': Arg('--prompt', 'set prompt', str),
    'cycle': Arg('--cycle', 'enable cyclic scroll', bool),
    'preview': Arg('--preview', 'enable preview', bool),
    'mesg': Arg('--header', 'The given string will be printed as the sticky header', str),
    'height': Arg(
        '--height', 'Display fzf window below the cursor with the given height instead of using the full screen', str
    ),
    'input': Arg('--print-query', 'Print query as the first line', bool),
}


class Fzf:
    def __init__(self) -> None:
        self.name = 'fzf'
        self.url = constants.HOMEPAGE_FZF
        self.keybind = KeyManager()

    @property
    def command(self) -> str:
        return helpers.check_command(self.name, self.url)

    def _build_args(  # noqa: C901
        self,
        case_sensitive: bool = False,
        multi_select: bool = False,
        prompt: str = constants.PROMPT,
        **kwargs,
    ) -> list[str]:
        header: list[str] = []
        args = shlex.split(self.command)
        args.append('--ansi')

        if case_sensitive is not None:
            args.append('+i' if case_sensitive else '-i')

        if kwargs.get('mesg'):
            header.extend(shlex.split(shlex.quote(kwargs.pop('mesg'))))

        if kwargs.pop('cycle', False):
            args.append('--cycle')

        if not kwargs.pop('preview', None):
            args.append('--no-preview')

        if 'height' in kwargs:
            args.extend(shlex.split(shlex.quote(f"--height={kwargs.pop('height')}")))

        if prompt:
            args.extend(['--prompt', prompt])

        if multi_select:
            args.append('--multi')

        # FIX: Do keybinds for FZF
        if self.keybind.list_keys:
            log.debug('Keybinds are disabled')

        for arg, value in kwargs.items():
            log.debug("'%s=%s' not supported", arg, value)

        if header:
            mesg = '\n'.join(msg.replace('\n', ' ') for msg in header)
            args.extend(shlex.split(shlex.quote(f'--header={mesg}')))

        if kwargs.pop('input', False):
            args.append('--print-query')

        return args

    def prompt(
        self,
        items: list[Any] | tuple[Any] | None = None,
        case_sensitive: bool = False,
        multi_select: bool = False,
        prompt: str = constants.PROMPT,
        preprocessor: Callable[..., Any] = lambda x: str(x),
        **kwargs,
    ) -> PromptReturn:
        """
        EXIT STATUS
            0      Normal exit
            1      No match
            2      Error
            130    Interrupted with CTRL-C or ESC
        """
        helpers.check_type(items)

        if not items:
            items = []

        args = self._build_args(case_sensitive, multi_select, prompt, **kwargs)
        selected, code = helpers.run(args, items, preprocessor)

        if code == FZF_INTERRUPTED_CODE:
            return None, 1

        if not selected:
            return selected, code

        result: Any = None

        for item in items:
            if helpers.remove_color_codes(preprocessor(item)) == selected:
                result = item
                break

        if not result:
            log.warning('result is empty')
            return selected, 1

        return result, code

    def input(self, prompt: str = constants.PROMPT) -> str:
        raise NotImplementedError

    def supported(self) -> str:
        return '\n'.join(f'{k:<10} {v.type.__name__.upper():<5} {v.help}' for k, v in SUPPORTED_ARGS.items())
