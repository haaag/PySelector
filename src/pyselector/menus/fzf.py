# fzf.py
from __future__ import annotations

import logging
import shlex
import subprocess
import sys
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import Iterable
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
FZF_INTERRUPTED_CODE = 130
FZF_RETURN_CODE_START = 10
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
        self.keybind.code_count = FZF_RETURN_CODE_START

    @property
    def command(self) -> str:
        return helpers.check_command(self.name, self.url)

    def _build_mesg(self, kwargs) -> list[str]:
        header: list[str] = []

        if kwargs.get('mesg'):
            header.extend(shlex.split(shlex.quote(kwargs.pop('mesg'))))

        for keybind in self.keybind.current:
            if not keybind.hidden:
                header.append(f'{constants.BULLET} Use <{keybind.bind}> {keybind.description}')

        if len(header) == 0:
            return header

        mesg = '\n'.join(msg.replace('\n', ' ') for msg in header)
        return shlex.split(shlex.quote(f'--header={mesg}'))

    def _build_keybinds(self) -> list[str]:
        keybinds: list[str] = []

        for keybind in self.keybind.current:
            # FIX: workaround to use keybinds in FZF
            # the `--expect` arg, returns the keybind pressed
            # TODO: read fzf's man and particularly `keybinds/events`
            keybinds.extend(
                [
                    '--bind',
                    f'{keybind.bind}:execute(echo {keybind.code})',
                    f'--expect={keybind.bind}',
                ],
            )

        return keybinds

    def _check_keybind_pressed(self, selected: str, keycode: int) -> tuple[str, int]:
        selected_with_keybind = 2
        if keycode == FZF_INTERRUPTED_CODE:
            return selected, keycode

        for key in self.keybind.current:
            selected_split = selected.split('\n')
            if selected.startswith(key.bind) and len(selected_split) >= selected_with_keybind:
                selected = selected_split[1]
                keycode = key.code
                break

        return selected, keycode

    def fzfrun(
        self,
        args: list[str],
        items: Sequence[T],
        preprocessor: Callable[..., Any],
    ) -> tuple[str | None, int]:
        log.debug('executing: %s', args)

        with subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
        ) as proc:
            input_items = '\n'.join(map(preprocessor, items))
            selected, _ = proc.communicate(input=input_items)
            return_code = proc.wait()

        if not selected:
            return None, return_code

        selected, return_code = self._check_keybind_pressed(selected, return_code)

        selected = selected.strip()
        if return_code == UserCancel(1):
            return selected, return_code

        return selected, return_code

    def _build_args(
        self,
        case_sensitive: bool = False,
        multi_select: bool = False,
        prompt: str = constants.PROMPT,
        **kwargs,
    ) -> list[str]:
        args = shlex.split(self.command)
        args.append('--ansi')
        args.append('--prompt=' + prompt)
        args.append('+i' if case_sensitive else '-i')

        if kwargs.pop('cycle', False):
            args.append('--cycle')

        if not kwargs.pop('preview', None):
            args.append('--no-preview')

        if 'height' in kwargs:
            args.extend(shlex.split(shlex.quote(f"--height={kwargs.pop('height')}")))

        if multi_select:
            args.append('--multi')

        args.extend(self._build_mesg(kwargs))
        args.extend(self._build_keybinds())

        for arg, value in kwargs.items():
            log.debug("'%s=%s' not supported", arg, value)

        if kwargs.pop('input', False):
            args.append('--print-query')

        return args

    def prompt(
        self,
        items: Iterable[T],
        case_sensitive: bool = False,
        multi_select: bool = False,
        prompt: str = constants.PROMPT,
        preprocessor: Callable[..., Any] = lambda x: str(x),
        **kwargs,
    ) -> PromptReturn:
        encoding = sys.getdefaultencoding()
        args = self._build_args(case_sensitive, multi_select, prompt, **kwargs)
        proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None)
        helpers.write_items_to_stdin(proc.stdin, items, encoding, preprocessor)
        if proc.stdin is not None:
            proc.stdin.close()

        output = helpers.read_output_from_stdout(proc.stdout, encoding)
        retcode = proc.wait()

        if not output or retcode in (UserCancel(1), FZF_INTERRUPTED_CODE):
            return None, UserCancel(1)

        keybind_and_selected = 2
        if len(output) == keybind_and_selected:
            keybind, selected = output
        else:
            keybind, selected = '', output[0]

        retcode = self.keybind.get_by_bind(keybind).code if keybind != '' else retcode
        for item in items:
            if helpers.remove_color_codes(preprocessor(item)) == selected:
                selected = item
                break
        return selected, retcode

    def this_prompt_works(
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
        selected, code = self.fzfrun(args, items, preprocessor)

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
