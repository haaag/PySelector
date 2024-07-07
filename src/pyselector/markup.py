# markup.py
#
# https://docs.gtk.org/Pango/pango_markup.html

from __future__ import annotations

import logging
from dataclasses import dataclass

from pyselector.colors import SUPPORTED_COLORS

log = logging.getLogger(__name__)


def _ansi_foreground(text: str, color: str | None) -> str:
    if not color:
        return text

    if color not in SUPPORTED_COLORS:
        log.error("unknown foreground color '%s'", color)
        return text

    text = f'\033[38;2;{SUPPORTED_COLORS[color]}m{text}'
    return f'{text}\033[0m'


def _ansi_background(text: str, color: str | None) -> str:
    if not color:
        return text

    if color not in SUPPORTED_COLORS:
        log.error("unknown background color '%s'", color)
        return text

    text = f'\033[48;2;{SUPPORTED_COLORS[color]}m{text}'
    return f'{text}\033[0m'


@dataclass
class PangoSpan:
    text: str
    alpha: str | None = None
    background: str | None = None
    background_alpha: str | None = None
    baseline_shift: str | None = None
    bgalpha: str | None = None
    bgcolor: str | None = None
    color: str | None = None
    face: str | None = None
    fallback: str | None = None
    fgalpha: str | None = None
    fgcolor: str | None = None
    font: str | None = None
    font_desc: str | None = None
    font_family: str | None = None
    font_features: str | None = None
    font_scale: str | None = None
    font_size: str | None = None
    font_stretch: str | None = None
    font_style: str | None = None
    font_variant: str | None = None
    font_weight: str | None = None
    foreground: str | None = None
    gravity: str | None = None
    gravity_hint: str | None = None
    lang: str | None = None
    letter_spacing: str | None = None
    overline: str | None = None
    overline_color: str | None = None
    rise: str | None = None
    show: str | None = None
    size: str | None = None
    stretch: str | None = None
    strikethrough: str | None = None
    strikethrough_color: str | None = None
    style: str | None = None
    sub: bool = False
    underline: str | None = None
    underline_color: str | None = None
    variant: str | None = None
    weight: str | None = None
    markup: bool = True
    # ansi codes
    ansi: bool = False
    fg_ansi: str | None = None
    bg_ansi: str | None = None

    def __hash__(self):
        attrs = tuple(self.__dict__[attr] for attr in sorted(self.__dict__.keys()) if attr not in ('text', 'sub'))
        return hash((self.text, attrs))

    def _format_ansi(self) -> str:
        if self.fg_ansi:
            self.text = _ansi_foreground(self.text, self.fg_ansi)
        if self.bg_ansi:
            self.text = _ansi_background(self.text, self.bg_ansi)
        return self.text

    def __str__(self) -> str:
        if self.markup and self.ansi:
            err = 'markup and ansi are mutually exclusive'
            log.error(err)
            raise ValueError(err)

        if self.ansi:
            return self._format_ansi()

        if not self.markup:
            return self.text

        attrs = []
        for attr in self.__dict__:
            if (
                attr != 'text'
                and attr != 'markup'
                and attr != 'sub'
                and attr != 'ansi'
                and attr != 'fg_ansi'
                and attr != 'bg_ansi'
                and self.__dict__[attr] is not None
            ):
                attrs.append(f'{attr}="{self.__dict__[attr]}"')

        text = self.text
        if self.sub:
            text = f'<sub>{text}</sub>'
        return f'<span {"".join(attrs)}>{text}</span>'
