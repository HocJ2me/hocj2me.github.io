# -*- coding: utf-8 -*-
"""Trợ giúp vẽ SVG minh hoạ (dùng lớp CSS .illus trong course_template.html)."""
from html import escape

_n = [0]


def svg(w, h, body, label):
    _n[0] += 1
    mid = f"ah{_n[0]}"
    defs = (f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ah"/></marker></defs>')
    return (f'<svg class="illus" viewBox="0 0 {w} {h}" style="max-width:{w}px" role="img" aria-label="{escape(label)}" '
            f'xmlns="http://www.w3.org/2000/svg">{defs}{body.replace("MARK", mid)}</svg>')


def box(x, y, w, h, cls="bx", rx=8, text=None, tcls="s", sub=None):
    out = f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/>'
    if text is not None:
        ty = y + h / 2 + (0 if sub else 5)
        out += f'<text class="{tcls}" x="{x + w / 2}" y="{ty - (4 if sub else 0)}" text-anchor="middle">{escape(text)}</text>'
        if sub:
            out += f'<text class="xs mute" x="{x + w / 2}" y="{ty + 12}" text-anchor="middle">{escape(sub)}</text>'
    return out


def text(x, y, s, cls="s", anchor="start"):
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{escape(s)}</text>'


def arrow(x1, y1, x2, y2, cls="ln", label=None, lx=None, ly=None):
    out = f'<line class="{cls}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" marker-end="url(#MARK)"/>'
    if label:
        out += text(lx if lx is not None else (x1 + x2) / 2, ly if ly is not None else (y1 + y2) / 2 - 6, label, "xs mute", "middle")
    return out


def path(d, cls="ln", arrow_end=True):
    return f'<path class="{cls}" d="{d}" fill="none"{" marker-end=" + chr(34) + "url(#MARK)" + chr(34) if arrow_end else ""}/>'
