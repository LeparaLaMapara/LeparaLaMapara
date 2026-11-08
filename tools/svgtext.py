"""Turn text into SVG path data so GitHub renders the lettering without web fonts."""
from functools import lru_cache
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

FONTS = Path(__file__).parent / "fonts"


@lru_cache(None)
def font(name, wght=None):
    f = TTFont(FONTS / f"{name}.ttf")
    if "fvar" in f:
        axes = {a.axisTag: a.defaultValue for a in f["fvar"].axes}
        if wght:
            axes["wght"] = wght
        f = instancer.instantiateVariableFont(f, axes)
    return f


def _glyph(f, ch):
    cmap = f.getBestCmap()
    return cmap.get(ord(ch), cmap.get(ord(" ")))


def width(text, name, size, wght=None, spacing=0.0):
    f = font(name, wght)
    scale = size / f["head"].unitsPerEm
    w = sum(f["hmtx"][_glyph(f, ch)][0] * scale + spacing for ch in text)
    return w - spacing if text else 0.0


def path(text, name, size, x, y, wght=None, spacing=0.0, anchor="start"):
    """Path data for text with its baseline at y. anchor: start, middle or end."""
    f = font(name, wght)
    scale = size / f["head"].unitsPerEm
    gs, hmtx = f.getGlyphSet(), f["hmtx"]
    w = width(text, name, size, wght, spacing)
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    out = []
    for ch in text:
        g = _glyph(f, ch)
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
        gs[g].draw(TransformPen(pen, (scale, 0, 0, -scale, x, y)))
        out.append(pen.getCommands())
        x += hmtx[g][0] * scale + spacing
    return " ".join(p for p in out if p)
