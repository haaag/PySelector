# markup.py
# https://docs.gtk.org/Pango/pango_markup.html

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class PangoSpan:
    text: str
    alpha: Optional[str] = None
    background: Optional[str] = None
    background_alpha: Optional[str] = None
    baseline_shift: Optional[str] = None
    bgalpha: Optional[str] = None
    bgcolor: Optional[str] = None
    color: Optional[str] = None
    face: Optional[str] = None
    fallback: Optional[str] = None
    fgalpha: Optional[str] = None
    fgcolor: Optional[str] = None
    font: Optional[str] = None
    font_desc: Optional[str] = None
    font_family: Optional[str] = None
    font_features: Optional[str] = None
    font_scale: Optional[str] = None
    font_size: Optional[str] = None
    font_stretch: Optional[str] = None
    font_style: Optional[str] = None
    font_variant: Optional[str] = None
    font_weight: Optional[str] = None
    foreground: Optional[str] = None
    gravity: Optional[str] = None
    gravity_hint: Optional[str] = None
    lang: Optional[str] = None
    letter_spacing: Optional[str] = None
    overline: Optional[str] = None
    overline_color: Optional[str] = None
    rise: Optional[str] = None
    show: Optional[str] = None
    size: Optional[str] = None
    stretch: Optional[str] = None
    strikethrough: Optional[str] = None
    strikethrough_color: Optional[str] = None
    style: Optional[str] = None
    sub: bool = False
    underline: Optional[str] = None
    underline_color: Optional[str] = None
    variant: Optional[str] = None
    weight: Optional[str] = None

    def __hash__(self):
        attrs = tuple(
            self.__dict__[attr]
            for attr in sorted(self.__dict__.keys())
            if attr != "text" and attr != "sub"
        )
        return hash((self.text, attrs))

    def __str__(self):
        attrs = []
        for attr in self.__dict__:
            if attr != "text" and attr != "sub" and self.__dict__[attr] is not None:
                attrs.append(f'{attr}="{self.__dict__[attr]}"')
        text = self.text
        if self.sub:
            text = f"<sub>{text}</sub>"
        return f'<span {"".join(attrs)}>{text}</span>'
