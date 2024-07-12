# constants.py
from __future__ import annotations

from typing import NewType

HOMEPAGE_ROFI = 'https://github.com/davatorium/rofi'
HOMEPAGE_DMENU = 'https://tools.suckless.org/dmenu'
HOMEPAGE_FZF = 'https://github.com/junegunn/fzf'

# icons
BULLET = '\u2022'

# others
PROMPT = 'PySelector> '

# return codes
UserConfirms = NewType('UserConfirms', int)
UserCancel = NewType('UserCancel', int)
