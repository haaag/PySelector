# markup.py
# https://docs.gtk.org/Pango/pango_markup.html

from __future__ import annotations

from dataclasses import dataclass

COLORS = {
    'black': '0;0;0',
    'red': '255;0;0',
    'green': '0;255;0',
    'yellow': '255;255;0',
    'blue': '0;0;255',
    'magenta': '255;0;255',
    'cyan': '0;255;255',
    'white': '255;255;255',
    'gray': '128;128;128',
    'grey': '128;128;128',
    'orange': '255;165;0',
    'purple': '128;0;128',
    'brown': '165;42;42',
    'lime': '0;255;0',
    'olive': '128;128;0',
    'teal': '0;128;128',
    'navy': '0;0;128',
    'fuchsia': '255;0;255',
    'aqua': '0;255;255',
    'maroon': '128;0;0',
    'silver': '192;192;192',
}


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
    # ansi
    ansi: bool = False
    fg_ansi: str | None = None
    bg_ansi: str | None = None

    def _format_ansi(self, text: str) -> str:
        if self.fg_ansi in COLORS:
            text = f'\033[38;2;{COLORS[self.fg_ansi]}m{text}'
        if self.bg_ansi in COLORS:
            text = f'\033[48;2;{COLORS[self.bg_ansi]}m{text}'
        return f'{text}\033[0m'

    def __hash__(self):
        attrs = tuple(self.__dict__[attr] for attr in sorted(self.__dict__.keys()) if attr not in ('text', 'sub'))
        return hash((self.text, attrs))

    def __str__(self) -> str:
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
