#!/usr/bin/env python3
"""Mascot kit: draw a character or hero glyph once as SVG, ship it natively, animate it as Lottie.

  mascot.py svg2code <file.svg> --swift|--compose [--name Pip] [--package app.mascot] [-o Out.swift]
  mascot.py lottie   <file.svg> <motion.json> -o out.json
  mascot.py preview  <out.json> [-o preview.html] [--size 240] [--frames]
  mascot.py check    <file.svg> [-o sheet.png]

The SVG is a rig: every <g> with data-pivot="x,y" (viewBox units) is a part that can move,
named by its id (body, eyes, lids, mouth, arm-left ...). Nested rig groups are parented, so
moving the body carries the eyes. data-rest="scale:100,0; opacity:0" sets a part's resting
pose (lids hidden until a blink). See references/mascot.md for how to design one.

svg2code  SwiftUI: one Shape per drawn part, a View that nests the rig with each group's pivot
          as its anchor, and a pose type you can animate. Compose: an ImageVector (groups
          carry pivots) and rememberXPainter(pose) for animation. No runtime library.
lottie    shape layers per rig group, parented like the SVG, anchored at the pivot; motion
          states laid end to end with a marker each (play a state by marker name).
          Path morph only between shapes with the same vertex count; anything else is refused.
preview   an HTML page that plays the Lottie with lottie-web (cdnjs, pinned). It drives the
          animation from a Web Animations clock, so scripts/filmstrip.py can pause it at any t
          and measure it; '#play' plays the first non-looping state (the reaction), '#state=x'
          a named one. --frames: no clock, '?t=<ms>' calls goToAndStop directly.
check     the 24 px silhouette, squint and small-size test sheet as one PNG.

Supported SVG: path (M L H V C S Q T A Z, relative too; arcs become cubics), rect (rx/ry),
circle, ellipse, line, polyline, polygon, g, transforms, fill / stroke / width / linecap /
linejoin / fill-rule / opacities, from attributes, style="", or simple <style> rules
(.class, #id, tag). Skipped with a note: gradients, masks, clip paths, filters, images,
text, <use>. Gradients fall back to their first stop colour.

Standard library only; works on Python 3.9.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

LOTTIE_WEB = "https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.12.2/lottie.min.js"
KAPPA = 0.5522847498
INHERITED = ("fill", "fill-opacity", "fill-rule", "stroke", "stroke-width", "stroke-opacity",
             "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "display", "visibility")
SKIPPED = {"text", "image", "use", "mask", "clipPath", "filter", "pattern", "foreignObject", "symbol",
           "linearGradient", "radialGradient", "marker", "switch"}
NAMED = {"black": "#000000", "white": "#ffffff", "red": "#ff0000", "green": "#008000", "blue": "#0000ff",
         "yellow": "#ffff00", "orange": "#ffa500", "gray": "#808080", "grey": "#808080", "transparent": None}
EASES = {"linear": (0, 0, 1, 1), "in": (0.42, 0, 1, 1), "out": (0, 0, 0.58, 1), "inOut": (0.42, 0, 0.58, 1),
         "back": (0.34, 1.56, 0.64, 1), "hold": None}
PROPS = ("position", "scale", "rotation", "opacity", "trim", "path")
notes: list[str] = []


def note(msg: str) -> None:
    if msg not in notes:
        notes.append(msg)


class MascotError(Exception):
    pass


# ---------------------------------------------------------------- geometry

def mul(m, n):
    """Affine matrices as (a, b, c, d, e, f), SVG order: m applied after n."""
    a, b, c, d, e, f = m
    A, B, C, D, E, F = n
    return (a * A + c * B, b * A + d * B, a * C + c * D, b * C + d * D, a * E + c * F + e, b * E + d * F + f)


IDENTITY = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)


def apply(m, p):
    a, b, c, d, e, f = m
    return (a * p[0] + c * p[1] + e, b * p[0] + d * p[1] + f)


def parse_transform(s: str):
    m = IDENTITY
    for name, args in re.findall(r"(\w+)\s*\(([^)]*)\)", s or ""):
        v = [float(x) for x in re.findall(r"[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?", args)]
        if name == "matrix" and len(v) == 6:
            t = tuple(v)
        elif name == "translate":
            t = (1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0)
        elif name == "scale":
            t = (v[0], 0, 0, v[1] if len(v) > 1 else v[0], 0, 0)
        elif name == "rotate":
            r = math.radians(v[0])
            t = (math.cos(r), math.sin(r), -math.sin(r), math.cos(r), 0, 0)
            if len(v) == 3:
                t = mul(mul((1, 0, 0, 1, v[1], v[2]), t), (1, 0, 0, 1, -v[1], -v[2]))
        elif name == "skewX":
            t = (1, 0, math.tan(math.radians(v[0])), 1, 0, 0)
        elif name == "skewY":
            t = (1, math.tan(math.radians(v[0])), 0, 1, 0, 0)
        else:
            note(f"unknown transform {name}() ignored")
            continue
        m = mul(m, t)
    return m


class Sub:
    """One subpath: a start point and segments ('L', p) or ('C', c1, c2, p), all absolute."""

    def __init__(self, start):
        self.start = start
        self.segs: list[tuple] = []
        self.closed = False

    def end(self):
        return self.segs[-1][-1] if self.segs else self.start

    def transformed(self, m):
        s = Sub(apply(m, self.start))
        s.segs = [(seg[0],) + tuple(apply(m, p) for p in seg[1:]) for seg in self.segs]
        s.closed = self.closed
        return s


def arc_to_cubics(p0, rx, ry, phi, large, sweep, p1):
    x1, y1 = p0
    x2, y2 = p1
    if (x1, y1) == (x2, y2):
        return []
    rx, ry = abs(rx), abs(ry)
    if rx == 0 or ry == 0:
        return [("L", p1)]
    cp, sp = math.cos(math.radians(phi)), math.sin(math.radians(phi))
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    x1p, y1p = cp * dx + sp * dy, -sp * dx + cp * dy
    lam = (x1p / rx) ** 2 + (y1p / ry) ** 2
    if lam > 1:
        rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
    num = rx * rx * ry * ry - rx * rx * y1p * y1p - ry * ry * x1p * x1p
    den = rx * rx * y1p * y1p + ry * ry * x1p * x1p
    coef = math.sqrt(max(0.0, num / den)) if den else 0.0
    if large == sweep:
        coef = -coef
    cxp, cyp = coef * rx * y1p / ry, -coef * ry * x1p / rx
    cx, cy = cp * cxp - sp * cyp + (x1 + x2) / 2, sp * cxp + cp * cyp + (y1 + y2) / 2

    def ang(u, v):
        return math.atan2(u[0] * v[1] - u[1] * v[0], u[0] * v[0] + u[1] * v[1])

    th1 = ang((1, 0), ((x1p - cxp) / rx, (y1p - cyp) / ry))
    dth = ang(((x1p - cxp) / rx, (y1p - cyp) / ry), ((-x1p - cxp) / rx, (-y1p - cyp) / ry))
    if not sweep and dth > 0:
        dth -= 2 * math.pi
    elif sweep and dth < 0:
        dth += 2 * math.pi
    n = max(1, math.ceil(abs(dth) / (math.pi / 2) - 1e-9))
    delta = dth / n
    t = 4 / 3 * math.tan(delta / 4)

    def pt(ux, uy):
        return (cx + rx * cp * ux - ry * sp * uy, cy + rx * sp * ux + ry * cp * uy)

    out = []
    for i in range(n):
        a1, a2 = th1 + i * delta, th1 + (i + 1) * delta
        c1 = pt(math.cos(a1) - t * math.sin(a1), math.sin(a1) + t * math.cos(a1))
        c2 = pt(math.cos(a2) + t * math.sin(a2), math.sin(a2) - t * math.cos(a2))
        end = p1 if i == n - 1 else pt(math.cos(a2), math.sin(a2))
        out.append(("C", c1, c2, end))
    return out


NUM = re.compile(r"[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?")


def parse_path(d: str) -> list[Sub]:
    s, i, subs = d or "", 0, []
    cur, start, last_c, last_q, cmd = (0.0, 0.0), (0.0, 0.0), None, None, None
    sub = None

    def skip():
        nonlocal i
        while i < len(s) and (s[i].isspace() or s[i] == ","):
            i += 1

    def number():
        nonlocal i
        skip()
        m = NUM.match(s, i)
        if not m:
            raise MascotError(f"bad path data near {s[i:i + 20]!r}")
        i = m.end()
        return float(m.group())

    def flag():
        nonlocal i
        skip()
        if i < len(s) and s[i] in "01":
            i += 1
            return s[i - 1] == "1"
        raise MascotError(f"bad arc flag near {s[i:i + 20]!r}")

    def ensure():
        nonlocal sub
        if sub is None:
            sub = Sub(cur)
            subs.append(sub)

    while True:
        skip()
        if i >= len(s):
            break
        if s[i].isalpha():
            cmd = s[i]
            i += 1
            if cmd in "Zz":
                if sub is not None:
                    sub.closed = True
                    cur = start
                sub, last_c, last_q = None, None, None
                continue
        elif cmd is None:
            raise MascotError("path data must start with M")
        rel = cmd.islower()
        C = cmd.upper()
        ox, oy = cur if rel else (0.0, 0.0)
        if C == "M":
            cur = (ox + number(), oy + number())
            start = cur
            sub = Sub(cur)
            subs.append(sub)
            cmd = "l" if rel else "L"
            last_c = last_q = None
            continue
        ensure()
        if C == "L":
            cur = (ox + number(), oy + number())
            sub.segs.append(("L", cur))
            last_c = last_q = None
        elif C == "H":
            cur = (ox + number() if rel else number(), cur[1])
            sub.segs.append(("L", cur))
            last_c = last_q = None
        elif C == "V":
            cur = (cur[0], oy + number() if rel else number())
            sub.segs.append(("L", cur))
            last_c = last_q = None
        elif C in "CS":
            if C == "C":
                c1 = (ox + number(), oy + number())
            else:
                c1 = (2 * cur[0] - last_c[0], 2 * cur[1] - last_c[1]) if last_c else cur
            c2 = (ox + number(), oy + number())
            p = (ox + number(), oy + number())
            sub.segs.append(("C", c1, c2, p))
            cur, last_c, last_q = p, c2, None
        elif C in "QT":
            if C == "Q":
                q = (ox + number(), oy + number())
            else:
                q = (2 * cur[0] - last_q[0], 2 * cur[1] - last_q[1]) if last_q else cur
            p = (ox + number(), oy + number())
            c1 = (cur[0] + 2 / 3 * (q[0] - cur[0]), cur[1] + 2 / 3 * (q[1] - cur[1]))
            c2 = (p[0] + 2 / 3 * (q[0] - p[0]), p[1] + 2 / 3 * (q[1] - p[1]))
            sub.segs.append(("C", c1, c2, p))
            cur, last_q, last_c = p, q, None
        elif C == "A":
            rx, ry, phi = number(), number(), number()
            large, sweep = flag(), flag()
            p = (ox + number(), oy + number())
            sub.segs += arc_to_cubics(cur, rx, ry, phi, large, sweep, p)
            cur, last_c, last_q = p, None, None
        else:
            raise MascotError(f"unknown path command {cmd!r}")
    return [x for x in subs if x.segs]


def ellipse_subs(cx, cy, rx, ry) -> list[Sub]:
    k, l = KAPPA * rx, KAPPA * ry
    s = Sub((cx + rx, cy))
    s.segs = [("C", (cx + rx, cy + l), (cx + k, cy + ry), (cx, cy + ry)),
              ("C", (cx - k, cy + ry), (cx - rx, cy + l), (cx - rx, cy)),
              ("C", (cx - rx, cy - l), (cx - k, cy - ry), (cx, cy - ry)),
              ("C", (cx + k, cy - ry), (cx + rx, cy - l), (cx + rx, cy))]
    s.closed = True
    return [s]


def rect_subs(x, y, w, h, rx, ry) -> list[Sub]:
    if rx is None and ry is None:
        rx = ry = 0.0
    rx = ry if rx is None else rx
    ry = rx if ry is None else ry
    rx, ry = min(rx, w / 2), min(ry, h / 2)
    if rx <= 0 or ry <= 0:
        s = Sub((x, y))
        s.segs = [("L", (x + w, y)), ("L", (x + w, y + h)), ("L", (x, y + h))]
        s.closed = True
        return [s]
    k, l = KAPPA * rx, KAPPA * ry
    s = Sub((x + rx, y))
    s.segs = [("L", (x + w - rx, y)), ("C", (x + w - rx + k, y), (x + w, y + ry - l), (x + w, y + ry)),
              ("L", (x + w, y + h - ry)), ("C", (x + w, y + h - ry + l), (x + w - rx + k, y + h), (x + w - rx, y + h)),
              ("L", (x + rx, y + h)), ("C", (x + rx - k, y + h), (x, y + h - ry + l), (x, y + h - ry)),
              ("L", (x, y + ry)), ("C", (x, y + ry - l), (x + rx - k, y), (x + rx, y))]
    s.closed = True
    return [s]


def points_subs(pts: str, closed: bool) -> list[Sub]:
    v = [float(n) for n in NUM.findall(pts or "")]
    p = list(zip(v[0::2], v[1::2]))
    if len(p) < 2:
        return []
    s = Sub(p[0])
    s.segs = [("L", q) for q in p[1:]]
    s.closed = closed
    return [s]


# ---------------------------------------------------------------- styles

def parse_color(v: str | None, gradients: dict):
    """(r, g, b) floats 0-1, or None for no paint."""
    if v is None:
        return None
    v = v.strip()
    if v in ("none", "") or v == "transparent":
        return None
    m = re.match(r"url\(\s*#([^)\s]+)\s*\)", v)
    if m:
        stop = gradients.get(m.group(1))
        note(f"gradient #{m.group(1)} drawn as its first stop colour (gradients aren't supported yet)")
        return parse_color(stop, gradients) if stop else None
    if v == "currentColor":
        note("currentColor drawn as black")
        return (0.0, 0.0, 0.0)
    v = NAMED.get(v.lower(), v)
    if v is None:
        return None
    m = re.match(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$", v)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    m = re.match(r"rgba?\(([^)]*)\)", v)
    if m:
        parts = [p.strip() for p in m.group(1).split(",")]
        return tuple((float(p[:-1]) / 100 if p.endswith("%") else float(p) / 255) for p in parts[:3])
    note(f"colour {v!r} not understood, drawn as black")
    return (0.0, 0.0, 0.0)


def hex_of(c) -> str:
    return "#" + "".join(f"{round(x * 255):02X}" for x in c)


def parse_css(text: str) -> list[tuple[tuple[int, int], int, str, dict]]:
    rules = []
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    for order, (sels, body) in enumerate(re.findall(r"([^{}]+)\{([^}]*)\}", text)):
        decl = parse_decl(body)
        for sel in sels.split(","):
            sel = sel.strip()
            if re.fullmatch(r"\.[\w-]+", sel):
                rules.append(((0, 1), order, sel, decl))
            elif re.fullmatch(r"#[\w-]+", sel):
                rules.append(((1, 0), order, sel, decl))
            elif re.fullmatch(r"[\w-]+", sel):
                rules.append(((0, 0), order, sel, decl))
            elif sel:
                note(f"CSS selector {sel!r} not supported, ignored")
    return sorted(rules, key=lambda r: (r[0], r[1]))


def parse_decl(body: str) -> dict:
    out = {}
    for part in body.split(";"):
        if ":" in part:
            k, v = part.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def local(tag: str) -> str:
    return tag.split("}", 1)[-1]


# ---------------------------------------------------------------- the rig model

class Item:
    """A drawn element: subpaths in viewBox units plus paint."""

    def __init__(self, ident, subs, fill, fill_op, rule, stroke, stroke_op, width, cap, join, miter):
        self.id, self.subs = ident, subs
        self.fill, self.fill_op, self.rule = fill, fill_op, rule
        self.stroke, self.stroke_op, self.width = stroke, stroke_op, width
        self.cap, self.join, self.miter = cap, join, miter


class Node:
    def __init__(self, ident, pivot, rest):
        self.id, self.pivot, self.rest = ident, pivot, rest
        self.children: list = []  # Item | Node, in draw order

    def walk(self):
        yield self
        for c in self.children:
            if isinstance(c, Node):
                yield from c.walk()

    def items(self):
        return [c for c in self.children if isinstance(c, Item)]


class Rig:
    def __init__(self, name, width, height, root, defs):
        self.name, self.w, self.h, self.root, self.defs = name, width, height, root, defs

    def nodes(self):
        return [n for n in self.root.walk() if n is not self.root]

    def node(self, ident):
        for n in self.root.walk():
            if n.id == ident:
                return n
        return None

    def colors(self):
        seen = []
        for n in self.root.walk():
            for it in n.items():
                for c in (it.fill, it.stroke):
                    if c is not None and hex_of(c) not in seen:
                        seen.append(hex_of(c))
        return seen


def parse_rest(s: str | None, ident: str) -> dict:
    rest = {}
    for part in (s or "").split(";"):
        if not part.strip():
            continue
        if ":" not in part:
            raise MascotError(f"data-rest on #{ident}: expected 'prop:value', got {part!r}")
        k, v = (x.strip() for x in part.split(":", 1))
        nums = [float(n) for n in NUM.findall(v)]
        if k not in ("position", "scale", "rotation", "opacity"):
            raise MascotError(f"data-rest on #{ident}: {k!r} isn't one of position, scale, rotation, opacity")
        if k in ("position", "scale") and len(nums) == 1:
            nums = nums * 2 if k == "scale" else nums + [0.0]
        rest[k] = nums if k in ("position", "scale") else nums[0]
    return rest


def load_svg(path: Path) -> Rig:
    try:
        tree = ET.parse(str(path))
    except ET.ParseError as e:
        raise MascotError(f"{path}: not valid XML ({e})")
    svg = tree.getroot()
    if local(svg.tag) != "svg":
        raise MascotError(f"{path}: root element is <{local(svg.tag)}>, not <svg>")
    vb = [float(v) for v in NUM.findall(svg.get("viewBox", ""))]
    if len(vb) == 4:
        minx, miny, w, h = vb
    else:
        minx = miny = 0.0
        w = float(NUM.match(svg.get("width", "24")).group())
        h = float(NUM.match(svg.get("height", "24")).group())
    css = []
    gradients = {}
    for el in svg.iter():
        t = local(el.tag)
        if t == "style":
            css += parse_css("".join(el.itertext()))
        elif t in ("linearGradient", "radialGradient") and el.get("id"):
            for stop in el:
                if local(stop.tag) == "stop":
                    sd = parse_decl(stop.get("style", ""))
                    gradients[el.get("id")] = sd.get("stop-color", stop.get("stop-color"))
                    break
    css.sort(key=lambda r: (r[0], r[1]))

    def own_style(el) -> dict:
        st = {k: el.get(k) for k in INHERITED + ("opacity",) if el.get(k) is not None}
        cls = (el.get("class") or "").split()
        for _, _, sel, decl in css:
            if (sel.startswith(".") and sel[1:] in cls) or (sel.startswith("#") and sel[1:] == el.get("id")) \
                    or sel == local(el.tag):
                st.update(decl)
        st.update(parse_decl(el.get("style", "")))
        return st

    root_m = (1, 0, 0, 1, -minx, -miny)
    root = Node("root", (w / 2, h / 2), {})
    defs: dict[str, Item] = {}

    def make_item(el, st, m) -> Item | None:
        t = local(el.tag)
        g = lambda k, d=0.0: float(NUM.match(el.get(k)).group()) if el.get(k) and NUM.match(el.get(k)) else d
        if t == "path":
            subs = parse_path(el.get("d", ""))
        elif t == "rect":
            subs = rect_subs(g("x"), g("y"), g("width"), g("height"),
                             g("rx") if el.get("rx") else None, g("ry") if el.get("ry") else None)
        elif t == "circle":
            subs = ellipse_subs(g("cx"), g("cy"), g("r"), g("r"))
        elif t == "ellipse":
            subs = ellipse_subs(g("cx"), g("cy"), g("rx"), g("ry"))
        elif t == "line":
            subs = points_subs(f"{g('x1')},{g('y1')} {g('x2')},{g('y2')}", False)
        elif t in ("polyline", "polygon"):
            subs = points_subs(el.get("points", ""), t == "polygon")
        else:
            return None
        if st.get("display") == "none" or st.get("visibility") == "hidden":
            return None
        subs = [s.transformed(m) for s in subs]
        op = float(st.get("opacity", 1))
        fill = parse_color(st.get("fill", "#000000"), gradients)
        stroke = parse_color(st.get("stroke"), gradients)
        scale = math.sqrt(abs(m[0] * m[3] - m[1] * m[2]))
        width = float(NUM.match(st.get("stroke-width", "1")).group()) * scale
        if stroke is not None and width <= 0:
            stroke = None
        if fill is None and stroke is None:
            return None
        return Item(el.get("id"), subs, fill, float(st.get("fill-opacity", 1)) * op,
                    st.get("fill-rule", "nonzero"), stroke, float(st.get("stroke-opacity", 1)) * op, width,
                    st.get("stroke-linecap", "butt"), st.get("stroke-linejoin", "miter"),
                    float(st.get("stroke-miterlimit", 4)))

    def visit(el, inherited: dict, m, node: Node, in_defs: bool):
        t = local(el.tag)
        if t in ("style", "title", "desc", "metadata", "stop"):
            return
        if t in SKIPPED:
            if t not in ("linearGradient", "radialGradient"):
                note(f"<{t}> skipped (not supported)")
            return
        st = {k: v for k, v in inherited.items() if k in INHERITED}
        own = own_style(el)
        if t == "g" and "opacity" in own:
            # Group opacity is folded into its children; overlapping children will look slightly different.
            st["_op"] = str(float(inherited.get("_op", 1)) * float(own.pop("opacity")))
        else:
            st["_op"] = inherited.get("_op", "1")
        st.update(own)
        m = mul(m, parse_transform(el.get("transform", "")))
        if t == "defs":
            for c in el:
                visit(c, st, m, node, True)
            return
        if t in ("g", "svg", "a"):
            target = node
            if t == "g" and el.get("data-pivot") is not None and not in_defs:
                ident = el.get("id")
                if not ident:
                    raise MascotError("a <g> with data-pivot needs an id (it names the part)")
                pv = [float(n) for n in NUM.findall(el.get("data-pivot"))]
                if len(pv) != 2:
                    raise MascotError(f"#{ident}: data-pivot must be 'x,y'")
                target = Node(ident, (pv[0] - minx, pv[1] - miny), parse_rest(el.get("data-rest"), ident))
                node.children.append(target)
            for c in el:
                visit(c, st, m, target, in_defs)
            return
        st = dict(st)
        st["opacity"] = str(float(st.get("_op", 1)) * float(own.get("opacity", 1)))
        it = make_item(el, st, m)
        if it is None:
            if t not in ("path", "rect", "circle", "ellipse", "line", "polyline", "polygon"):
                note(f"<{t}> skipped (not supported)")
            return
        if in_defs:
            if it.id:
                defs[it.id] = it
        else:
            node.children.append(it)

    for c in svg:
        visit(c, {}, root_m, root, False)
    ids = [n.id for n in root.walk()]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        raise MascotError(f"rig group ids must be unique: {', '.join(dup)}")
    return Rig(path.stem, w, h, root, defs)


# ---------------------------------------------------------------- helpers for code output

def fmt(v: float) -> str:
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def pascal(s: str) -> str:
    out = "".join(p[:1].upper() + p[1:] for p in re.split(r"[^0-9A-Za-z]+", s) if p)
    return out if out and not out[0].isdigit() else "M" + out


def camel(s: str) -> str:
    p = pascal(s)
    return p[:1].lower() + p[1:]


SWIFT_KEYWORDS = {"default", "case", "class", "func", "import", "init", "let", "var", "return", "self", "struct",
                  "enum", "extension", "protocol", "static", "switch", "where", "while", "for", "in", "if", "else",
                  "repeat", "do", "is", "as", "nil", "true", "false", "operator", "public", "private", "internal"}


def swift_case(s: str) -> str:
    c = camel(s)
    return f"`{c}`" if c in SWIFT_KEYWORDS else c


def rest_pose(node: Node) -> dict:
    r = node.rest
    pos = r.get("position", [0.0, 0.0])
    sc = r.get("scale", [100.0, 100.0])
    return {"dx": pos[0], "dy": pos[1], "sx": sc[0] / 100, "sy": sc[1] / 100,
            "rot": r.get("rotation", 0.0), "op": r.get("opacity", 100.0) / 100}


def color_name(h: str) -> str:
    return "c" + h[1:]


# ---------------------------------------------------------------- svg2code: SwiftUI

def swift_path_lines(subs: list[Sub], indent: str) -> list[str]:
    P = lambda p: f"CGPoint(x: {fmt(p[0])}, y: {fmt(p[1])})"
    out = []
    for s in subs:
        out.append(f"{indent}p.move(to: {P(s.start)})")
        for seg in s.segs:
            if seg[0] == "L":
                out.append(f"{indent}p.addLine(to: {P(seg[1])})")
            else:
                out.append(f"{indent}p.addCurve(to: {P(seg[3])}, control1: {P(seg[1])}, control2: {P(seg[2])})")
        if s.closed:
            out.append(f"{indent}p.closeSubpath()")
    return out


def to_swift(rig: Rig, name: str, source: str) -> str:
    N = name
    caps = {"butt": ".butt", "round": ".round", "square": ".square"}
    joins = {"miter": ".miter", "round": ".round", "bevel": ".bevel"}
    nodes = rig.nodes()
    o = [f"// Generated by app-ui-slopless scripts/mascot.py svg2code from {source}. Edit the SVG, then regenerate.",
         "import SwiftUI", "",
         f"/// The {N} palette, taken from the SVG.",
         f"enum {N}Palette {{"]
    for h in rig.colors():
        r, g, b = parse_color(h, {})
        o.append(f"    static let {color_name(h)} = Color(red: {fmt(r)}, green: {fmt(g)}, blue: {fmt(b)})")
    o += ["}", "",
          f"/// A rig part's pose. Offsets are in viewBox units, scale is 1 = 100%, rotation is degrees clockwise.",
          f"/// Opacity and trim apply to the part's own shapes, not to the parts nested in it (as in Lottie).",
          f"struct {N}Pose: Equatable {{",
          "    var offset: CGSize = .zero",
          "    var scale: CGSize = CGSize(width: 1, height: 1)",
          "    var rotation: Double = 0",
          "    var opacity: Double = 1",
          "    var trimStart: CGFloat = 0",
          "    var trimEnd: CGFloat = 1",
          "}", ""]
    if nodes:
        o += [f"/// The rig: each movable part, its pivot (viewBox units) and its resting pose.",
              f"enum {N}Rig: String, CaseIterable {{"]
        for n in nodes:
            o.append(f"    case {swift_case(n.id)} = \"{n.id}\"")
        o += ["", "    var pivot: CGPoint {", "        switch self {"]
        for n in nodes:
            o.append(f"        case .{swift_case(n.id).strip('`')}: return CGPoint(x: {fmt(n.pivot[0])}, y: {fmt(n.pivot[1])})")
        o += ["        }", "    }", "", f"    var rest: {N}Pose {{", "        switch self {"]
        for n in nodes:
            r = rest_pose(n)
            args = []
            if r["dx"] or r["dy"]:
                args.append(f"offset: CGSize(width: {fmt(r['dx'])}, height: {fmt(r['dy'])})")
            if (r["sx"], r["sy"]) != (1, 1):
                args.append(f"scale: CGSize(width: {fmt(r['sx'])}, height: {fmt(r['sy'])})")
            if r["rot"]:
                args.append(f"rotation: {fmt(r['rot'])}")
            if r["op"] != 1:
                args.append(f"opacity: {fmt(r['op'])}")
            o.append(f"        case .{swift_case(n.id).strip('`')}: return {N}Pose({', '.join(args)})")
        o += ["        }", "    }", "}", ""]
    o += [f"enum {N}Geometry {{",
          f"    static let viewBox = CGSize(width: {fmt(rig.w)}, height: {fmt(rig.h)})", "",
          "    /// Scales a viewBox path to fit `rect` (centred, aspect kept), trims it, and outlines strokes.",
          "    static func fit(_ path: Path, in rect: CGRect, trimStart: CGFloat, trimEnd: CGFloat, stroke: StrokeStyle? = nil) -> Path {",
          "        let s = min(rect.width / viewBox.width, rect.height / viewBox.height)",
          "        let move = CGAffineTransform(translationX: rect.midX - viewBox.width * s / 2, y: rect.midY - viewBox.height * s / 2)",
          "        var p = (trimStart > 0 || trimEnd < 1) ? path.trimmedPath(from: max(0, trimStart), to: min(1, trimEnd)) : path",
          "        p = p.applying(move.scaledBy(x: s, y: s))",
          "        if var style = stroke {",
          "            style.lineWidth *= s",
          "            p = p.strokedPath(style)",
          "        }",
          "        return p",
          "    }",
          "}", "",
          f"/// Moves a rig part about its pivot, in the coordinate space of the mascot's frame.",
          f"struct {N}PoseEffect: GeometryEffect {{",
          f"    var pose: {N}Pose",
          "    let pivot: CGPoint", "",
          "    var animatableData: AnimatablePair<AnimatablePair<CGFloat, CGFloat>, AnimatablePair<AnimatablePair<CGFloat, CGFloat>, Double>> {",
          "        get {",
          "            AnimatablePair(AnimatablePair(pose.offset.width, pose.offset.height),",
          "                           AnimatablePair(AnimatablePair(pose.scale.width, pose.scale.height), pose.rotation))",
          "        }",
          "        set {",
          "            pose.offset = CGSize(width: newValue.first.first, height: newValue.first.second)",
          "            pose.scale = CGSize(width: newValue.second.first.first, height: newValue.second.first.second)",
          "            pose.rotation = newValue.second.second",
          "        }",
          "    }", "",
          "    func effectValue(size: CGSize) -> ProjectionTransform {",
          f"        let vb = {N}Geometry.viewBox",
          "        let s = min(size.width / vb.width, size.height / vb.height)",
          "        let px = (size.width - vb.width * s) / 2 + pivot.x * s",
          "        let py = (size.height - vb.height * s) / 2 + pivot.y * s",
          "        // SwiftUI ignores a transform it can't invert, so a part scaled to 0 (lids at rest) keeps a sliver.",
          "        let sx = abs(pose.scale.width) < 0.001 ? 0.001 : pose.scale.width",
          "        let sy = abs(pose.scale.height) < 0.001 ? 0.001 : pose.scale.height",
          "        let t = CGAffineTransform(translationX: px + pose.offset.width * s, y: py + pose.offset.height * s)",
          "            .rotated(by: pose.rotation * .pi / 180)",
          "            .scaledBy(x: sx, y: sy)",
          "            .translatedBy(x: -px, y: -py)",
          "        return ProjectionTransform(t)",
          "    }",
          "}", ""]

    parts = []  # (node, item, struct name)
    for n in rig.root.walk():
        for k, it in enumerate(n.items(), 1):
            sname = f"{N}{pascal(n.id)}Part{k}"
            parts.append((n, it, sname))
            if it.fill is not None:
                o += part_struct(it, sname, N, None)
            if it.stroke is not None:
                style = (f"StrokeStyle(lineWidth: {fmt(it.width)}, lineCap: {caps.get(it.cap, '.butt')}, "
                         f"lineJoin: {joins.get(it.join, '.miter')}, miterLimit: {fmt(it.miter)})")
                o += part_struct(it, sname + "Stroke", N, style)

    def view_lines(n: Node, indent: str) -> list[str]:
        lines = []
        pose = "rest" if n is rig.root else f"pose(.{swift_case(n.id).strip('`')})"
        own = [x for x in parts if x[0] is n]
        k = 0
        for c in n.children:
            if isinstance(c, Item):
                _, it, sname = own[k]
                k += 1
                trim = "" if n is rig.root else f"trimStart: {pose}.trimStart, trimEnd: {pose}.trimEnd"
                op = "" if n is rig.root else f".opacity({pose}.opacity)"
                if it.fill is not None:
                    style = ", style: FillStyle(eoFill: true)" if it.rule == "evenodd" else ""
                    alpha = f".opacity({fmt(it.fill_op)})" if it.fill_op < 1 else ""
                    lines.append(f"{indent}{sname}({trim}).fill({N}Palette.{color_name(hex_of(it.fill))}{alpha}{style}){op}")
                if it.stroke is not None:
                    alpha = f".opacity({fmt(it.stroke_op)})" if it.stroke_op < 1 else ""
                    lines.append(f"{indent}{sname}Stroke({trim}).fill({N}Palette.{color_name(hex_of(it.stroke))}{alpha}){op}")
            else:
                lines.append(f"{indent}ZStack {{")
                lines += view_lines(c, indent + "    ")
                lines.append(f"{indent}}}")
                lines.append(f"{indent}.modifier({N}PoseEffect(pose: pose(.{swift_case(c.id).strip('`')}), "
                             f"pivot: {N}Rig.{swift_case(c.id).strip('`')}.pivot))")
        return chunk_swift(lines, indent)

    o += [f"/// {N}, drawn from the SVG rig. Pass a pose per part to animate it, e.g.",
          f"/// `withAnimation(.spring(duration: 0.3, bounce: 0.5)) {{ pose[.body] = {N}Pose(scale: CGSize(width: 1.1, height: 0.9)) }}`.",
          f"struct {N}Mascot: View {{"]
    if nodes:
        o += [f"    var pose: [{N}Rig: {N}Pose] = [:]", "",
              f"    private func pose(_ part: {N}Rig) -> {N}Pose {{ pose[part] ?? part.rest }}", ""]
    o += ["    var body: some View {", "        ZStack {"]
    o += view_lines(rig.root, "            ")
    o += ["        }", f"        .aspectRatio({N}Geometry.viewBox, contentMode: .fit)", "    }", "}", ""]
    return "\n".join(o)


def part_struct(it: Item, sname: str, N: str, stroke: str | None) -> list[str]:
    """One drawn part as a Shape: its path in viewBox units, fitted to the frame; strokes come out outlined."""
    o = [f"struct {sname}: Shape {{",
         "    var trimStart: CGFloat = 0",
         "    var trimEnd: CGFloat = 1",
         "    var animatableData: AnimatablePair<CGFloat, CGFloat> {",
         "        get { AnimatablePair(trimStart, trimEnd) }",
         "        set { trimStart = newValue.first; trimEnd = newValue.second }",
         "    }", "",
         "    func path(in rect: CGRect) -> Path {",
         "        var p = Path()"]
    o += swift_path_lines(it.subs, "        ")
    tail = f", stroke: {stroke}" if stroke else ""
    o += [f"        return {N}Geometry.fit(p, in: rect, trimStart: trimStart, trimEnd: trimEnd{tail})",
          "    }", "}", ""]
    return o


def chunk_swift(lines: list[str], indent: str) -> list[str]:
    """Keep each ViewBuilder block at 10 children or fewer by wrapping runs in Group { }."""
    blocks, cur, depth = [], [], 0
    for ln in lines:
        stripped = ln.strip()
        if depth == 0 and cur and not stripped.startswith("."):
            blocks.append(cur)
            cur = []
        cur.append(ln)
        depth += stripped.count("{") - stripped.count("}")
    if cur:
        blocks.append(cur)
    if len(blocks) <= 10:
        return lines
    out = []
    for i in range(0, len(blocks), 9):
        out.append(f"{indent}Group {{")
        for b in blocks[i:i + 9]:
            out += ["    " + ln for ln in b]
        out.append(f"{indent}}}")
    return chunk_swift(out, indent)


# ---------------------------------------------------------------- svg2code: Compose

def kt_path_lines(subs: list[Sub], indent: str) -> list[str]:
    F = lambda v: fmt(v) + "f"
    out = []
    for s in subs:
        out.append(f"{indent}moveTo({F(s.start[0])}, {F(s.start[1])})")
        for seg in s.segs:
            if seg[0] == "L":
                out.append(f"{indent}lineTo({F(seg[1][0])}, {F(seg[1][1])})")
            else:
                (a, b), (c, d), (e, f) = seg[1], seg[2], seg[3]
                out.append(f"{indent}curveTo({F(a)}, {F(b)}, {F(c)}, {F(d)}, {F(e)}, {F(f)})")
        if s.closed:
            out.append(f"{indent}close()")
    return out


def to_compose(rig: Rig, name: str, package: str | None, source: str) -> str:
    N = name
    F = lambda v: fmt(v) + "f"
    caps = {"butt": "StrokeCap.Butt", "round": "StrokeCap.Round", "square": "StrokeCap.Square"}
    joins = {"miter": "StrokeJoin.Miter", "round": "StrokeJoin.Round", "bevel": "StrokeJoin.Bevel"}
    nodes = rig.nodes()
    o = [f"// Generated by app-ui-slopless scripts/mascot.py svg2code from {source}. Edit the SVG, then regenerate."]
    if package:
        o += [f"package {package}", ""]
    o += ["import androidx.compose.runtime.Composable",
          "import androidx.compose.runtime.Immutable",
          "import androidx.compose.ui.graphics.Color",
          "import androidx.compose.ui.graphics.PathFillType",
          "import androidx.compose.ui.graphics.SolidColor",
          "import androidx.compose.ui.graphics.StrokeCap",
          "import androidx.compose.ui.graphics.StrokeJoin",
          "import androidx.compose.ui.graphics.vector.Group",
          "import androidx.compose.ui.graphics.vector.ImageVector",
          "import androidx.compose.ui.graphics.vector.Path",
          "import androidx.compose.ui.graphics.vector.PathData",
          "import androidx.compose.ui.graphics.vector.VectorPainter",
          "import androidx.compose.ui.graphics.vector.group",
          "import androidx.compose.ui.graphics.vector.rememberVectorPainter",
          "import androidx.compose.ui.unit.dp", "",
          f"/** The {N} palette, taken from the SVG. */",
          f"object {N}Palette {{"]
    for h in rig.colors():
        o.append(f"    val {pascal(color_name(h))} = Color(0xFF{h[1:]})")
    o += ["}", "",
          "/**",
          " * A rig part's pose. Offsets are in viewport units, scale is 1 = 100%, rotation is degrees clockwise.",
          " * Alpha and trim apply to the part's own paths, not to the parts nested in it (as in Lottie).",
          " */",
          "@Immutable",
          f"data class {N}Pose(",
          "    val offsetX: Float = 0f,",
          "    val offsetY: Float = 0f,",
          "    val scaleX: Float = 1f,",
          "    val scaleY: Float = 1f,",
          "    val rotation: Float = 0f,",
          "    val alpha: Float = 1f,",
          "    val trimStart: Float = 0f,",
          "    val trimEnd: Float = 1f,",
          ")", ""]
    if nodes:
        o += [f"/** The rig: each movable part, its pivot (viewport units) and its resting pose. */",
              f"enum class {N}Rig(val id: String, val pivotX: Float, val pivotY: Float, val rest: {N}Pose) {{"]
        for i, n in enumerate(nodes):
            r = rest_pose(n)
            args = []
            for key, kt, default in (("dx", "offsetX", 0), ("dy", "offsetY", 0), ("sx", "scaleX", 1),
                                     ("sy", "scaleY", 1), ("rot", "rotation", 0), ("op", "alpha", 1)):
                if r[key] != default:
                    args.append(f"{kt} = {F(r[key])}")
            end = "," if i < len(nodes) - 1 else ";"
            o.append(f"    {pascal(n.id)}(\"{n.id}\", {F(n.pivot[0])}, {F(n.pivot[1])}, {N}Pose({', '.join(args)})){end}")
        o += ["}", ""]

    parts = []
    for n in rig.root.walk():
        for k, it in enumerate(n.items(), 1):
            vname = f"{camel(N)}{pascal(n.id)}Part{k}"
            parts.append((n, it, vname))
            o.append(f"private val {vname} = PathData {{")
            o += kt_path_lines(it.subs, "    ")
            o += ["}", ""]

    def path_args(it: Item, vname: str, alpha: str, trim: tuple[str, str] | None) -> str:
        a = [f"pathData = {vname}"]
        if it.rule == "evenodd":
            a.append("pathFillType = PathFillType.EvenOdd")
        if it.fill is not None:
            a.append(f"fill = SolidColor({N}Palette.{pascal(color_name(hex_of(it.fill)))})")
            fa = mul_alpha(fmt(it.fill_op), alpha)
            if fa != "1f":
                a.append(f"fillAlpha = {fa}")
        if it.stroke is not None:
            a.append(f"stroke = SolidColor({N}Palette.{pascal(color_name(hex_of(it.stroke)))})")
            sa = mul_alpha(fmt(it.stroke_op), alpha)
            if sa != "1f":
                a.append(f"strokeAlpha = {sa}")
            a.append(f"strokeLineWidth = {F(it.width)}")
            a.append(f"strokeLineCap = {caps.get(it.cap, 'StrokeCap.Butt')}")
            a.append(f"strokeLineJoin = {joins.get(it.join, 'StrokeJoin.Miter')}")
            a.append(f"strokeLineMiter = {F(it.miter)}")
        if trim:
            a += [f"trimPathStart = {trim[0]}", f"trimPathEnd = {trim[1]}"]
        return ", ".join(a)

    def mul_alpha(item_alpha: str, alpha: str) -> str:
        if alpha in ("", "1f"):
            return item_alpha + "f" if not item_alpha.endswith("f") else item_alpha
        return alpha if item_alpha == "1" else f"{item_alpha}f * {alpha}"

    # Static ImageVector at the rest pose.
    def builder_lines(n: Node, indent: str) -> list[str]:
        lines = []
        own = [x for x in parts if x[0] is n]
        k = 0
        for c in n.children:
            if isinstance(c, Item):
                _, it, vname = own[k]
                k += 1
                alpha = "1f" if n is rig.root else F(rest_pose(n)["op"])
                lines.append(f"{indent}addPath({path_args(it, vname, alpha, None)})")
            else:
                r = rest_pose(c)
                lines.append(f"{indent}group(name = \"{c.id}\", rotate = {F(r['rot'])}, pivotX = {F(c.pivot[0])}, "
                             f"pivotY = {F(c.pivot[1])}, scaleX = {F(r['sx'])}, scaleY = {F(r['sy'])}, "
                             f"translationX = {F(r['dx'])}, translationY = {F(r['dy'])}) {{")
                lines += builder_lines(c, indent + "    ")
                lines.append(f"{indent}}}")
        return lines

    o += [f"/** {N} at rest, as a static ImageVector (an icon, a placeholder, a widget). */",
          f"val {N}Vector: ImageVector by lazy {{",
          f"    ImageVector.Builder(name = \"{N}\", defaultWidth = {fmt(rig.w)}.dp, defaultHeight = {fmt(rig.h)}.dp, "
          f"viewportWidth = {F(rig.w)}, viewportHeight = {F(rig.h)}).apply {{"]
    o += builder_lines(rig.root, "        ")
    o += ["    }.build()", "}", ""]

    def painter_lines(n: Node, indent: str) -> list[str]:
        lines = []
        own = [x for x in parts if x[0] is n]
        k = 0
        v = None if n is rig.root else "p" + pascal(n.id)
        for c in n.children:
            if isinstance(c, Item):
                _, it, vname = own[k]
                k += 1
                alpha = "1f" if v is None else f"{v}.alpha"
                trim = None if v is None else (f"{v}.trimStart", f"{v}.trimEnd")
                lines.append(f"{indent}Path({path_args(it, vname, alpha, trim)})")
            else:
                cv = "p" + pascal(c.id)
                lines.append(f"{indent}val {cv} = pose[{N}Rig.{pascal(c.id)}] ?: {N}Rig.{pascal(c.id)}.rest")
                lines.append(f"{indent}Group(name = \"{c.id}\", rotation = {cv}.rotation, pivotX = {F(c.pivot[0])}, "
                             f"pivotY = {F(c.pivot[1])}, scaleX = {cv}.scaleX, scaleY = {cv}.scaleY, "
                             f"translationX = {cv}.offsetX, translationY = {cv}.offsetY) {{")
                lines += painter_lines(c, indent + "    ")
                lines.append(f"{indent}}}")
        return lines

    pose_param = f"pose: Map<{N}Rig, {N}Pose> = emptyMap()" if nodes else ""
    o += ["/**",
          f" * {N} as a painter you can animate: pass a pose per rig part, e.g. from animateFloatAsState",
          " * or an Animatable, and draw it with Image(painter, contentDescription = null).",
          " */",
          "@Composable",
          f"fun remember{N}Painter({pose_param}): VectorPainter =",
          f"    rememberVectorPainter(defaultWidth = {fmt(rig.w)}.dp, defaultHeight = {fmt(rig.h)}.dp, "
          f"viewportWidth = {F(rig.w)}, viewportHeight = {F(rig.h)}, name = \"{N}\", autoMirror = false) {{ _, _ ->"]
    o += painter_lines(rig.root, "        ")
    o += ["    }", ""]
    return "\n".join(o)


# ---------------------------------------------------------------- Lottie

def lottie_shape(subs_one: Sub) -> dict:
    s = subs_one
    verts = [s.start]
    ins = [[0, 0]]
    outs = []
    for seg in s.segs:
        prev = verts[-1]
        if seg[0] == "C":
            outs.append([seg[1][0] - prev[0], seg[1][1] - prev[1]])
            ins.append([seg[2][0] - seg[3][0], seg[2][1] - seg[3][1]])
        else:
            outs.append([0, 0])
            ins.append([0, 0])
        verts.append(seg[-1])
    outs.append([0, 0])
    if s.closed and len(verts) > 1 and abs(verts[-1][0] - verts[0][0]) < 1e-6 and abs(verts[-1][1] - verts[0][1]) < 1e-6:
        ins[0] = ins.pop()
        verts.pop()
        outs.pop()
    r = lambda pts: [[round(p[0], 3), round(p[1], 3)] for p in pts]
    return {"i": r(ins), "o": r(outs), "v": r(verts), "c": bool(s.closed)}


def rgba(c) -> list:
    return [round(c[0], 4), round(c[1], 4), round(c[2], 4), 1]


def lottie_group(it: Item, trim: dict | None, path_prop: dict | None) -> dict:
    items = []
    for k, s in enumerate(it.subs):
        ks = path_prop if (path_prop is not None and k == 0) else {"a": 0, "k": lottie_shape(s)}
        items.append({"ty": "sh", "nm": f"path {k + 1}", "ks": ks})
    if trim:
        items.append({"ty": "tm", "nm": "trim", "s": trim["s"], "e": trim["e"], "o": {"a": 0, "k": 0}, "m": 1})
    if it.stroke is not None:
        items.append({"ty": "st", "nm": "stroke", "c": {"a": 0, "k": rgba(it.stroke)}, "o": {"a": 0, "k": round(it.stroke_op * 100, 2)},
                      "w": {"a": 0, "k": round(it.width, 3)}, "lc": {"butt": 1, "round": 2, "square": 3}.get(it.cap, 1),
                      "lj": {"miter": 1, "round": 2, "bevel": 3}.get(it.join, 1), "ml": it.miter})
    if it.fill is not None:
        items.append({"ty": "fl", "nm": "fill", "c": {"a": 0, "k": rgba(it.fill)}, "o": {"a": 0, "k": round(it.fill_op * 100, 2)},
                      "r": 2 if it.rule == "evenodd" else 1})
    items.append({"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]},
                  "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}, "sk": {"a": 0, "k": 0}, "sa": {"a": 0, "k": 0}})
    return {"ty": "gr", "nm": it.id or "shape", "it": items}


def vertex_signature(it: Item) -> list[tuple[int, bool]]:
    return [(len(lottie_shape(s)["v"]), s.closed) for s in it.subs]


def build_lottie(rig: Rig, spec: dict) -> dict:
    fr = float(spec.get("fr", 60))
    states = spec.get("states")
    if not isinstance(states, list) or not states:
        raise MascotError("motion spec needs a non-empty 'states' list")
    nodes = {n.id: n for n in rig.nodes()}
    by_id_items = {}
    for n in rig.root.walk():
        for it in n.items():
            if it.id:
                by_id_items[it.id] = it
    by_id_items.update(rig.defs)

    # Lay the states end to end, one frame apart, so no two keys share a frame.
    timeline, start = [], 0
    for st in states:
        name = st.get("name")
        if not name:
            raise MascotError("every state needs a name")
        ms = float(st.get("ms", 0))
        if ms <= 0:
            raise MascotError(f"state {name!r}: 'ms' (its duration) must be > 0")
        dur = max(1, round(ms * fr / 1000))
        for layer, props in (st.get("tracks") or {}).items():
            if layer not in nodes:
                raise MascotError(f"state {name!r}: no rig group #{layer} (groups: {', '.join(nodes) or 'none'})")
            for prop, keys in props.items():
                if prop not in PROPS:
                    raise MascotError(f"state {name!r}, #{layer}: unknown property {prop!r} (use {', '.join(PROPS)})")
                if not keys:
                    raise MascotError(f"state {name!r}, #{layer}.{prop}: no keyframes")
                ts = [float(k["t"]) for k in keys]
                if ts != sorted(ts) or len({round(t * fr / 1000) for t in ts}) != len(ts):
                    raise MascotError(f"state {name!r}, #{layer}.{prop}: keyframe times must increase and be "
                                      f"at least one frame ({1000 / fr:.1f} ms) apart")
                if ts[-1] > ms:
                    raise MascotError(f"state {name!r}, #{layer}.{prop}: key at {ts[-1]:g} ms is past the state's {ms:g} ms")
                for k in keys:
                    e = k.get("ease", "inOut")
                    if not (e in EASES or (isinstance(e, list) and len(e) == 4)):
                        raise MascotError(f"state {name!r}, #{layer}.{prop}: ease {e!r} isn't one of "
                                          f"{', '.join(EASES)} or [x1, y1, x2, y2]")
                if st.get("loop") and keys[0]["v"] != keys[-1]["v"]:
                    note(f"state {name!r} loops but #{layer}.{prop} ends on a different value than it starts: it will jump")
                if st.get("loop") and ts[-1] < ms:
                    note(f"state {name!r} loops but #{layer}.{prop} stops at {ts[-1]:g} of {ms:g} ms: it holds, then jumps")
        timeline.append({"name": name, "loop": bool(st.get("loop")), "ms": ms, "start": start, "dur": dur, "st": st})
        start += dur + 1
    op = start

    def rest_value(node: Node, prop: str):
        r = node.rest
        if prop == "position":
            return r.get("position", [0.0, 0.0])
        if prop == "scale":
            return r.get("scale", [100.0, 100.0])
        if prop == "rotation":
            return r.get("rotation", 0.0)
        if prop == "opacity":
            return r.get("opacity", 100.0)
        if prop == "trim":
            return [0.0, 100.0]
        return None

    def morph_item(node: Node) -> Item:
        own = node.items()
        if len(own) != 1 or len(own[0].subs) < 1:
            raise MascotError(f"#{node.id}: a path morph needs the group to hold exactly one shape (it holds {len(own)})")
        return own[0]

    def lottie_value(node: Node, prop: str, v):
        if prop == "position":
            v = v if isinstance(v, list) else [v, 0]
            return [round(node.pivot[0] + v[0], 3), round(node.pivot[1] + v[1], 3), 0]
        if prop == "scale":
            v = v if isinstance(v, list) else [v, v]
            return [v[0], v[1], 100]
        if prop in ("rotation", "opacity"):
            return [v]
        if prop == "path":
            base = morph_item(node)
            target = by_id_items.get(v) if isinstance(v, str) else None
            if target is None:
                raise MascotError(f"#{node.id}: morph target #{v} not found (put it in <defs> with that id)")
            if vertex_signature(target) != vertex_signature(base):
                raise MascotError(f"#{node.id}: can't morph to #{v}: {vertex_signature(base)} vs "
                                  f"{vertex_signature(target)} (vertex count, closed) per subpath. Redraw the target "
                                  "with the same number of points in the same order, or swap shapes with opacity instead.")
            return [lottie_shape(target.subs[0])]
        raise AssertionError(prop)

    def ease_obj(e, dims: int):
        x1, y1, x2, y2 = EASES[e] if isinstance(e, str) else e
        return {"o": {"x": [x1] * dims, "y": [y1] * dims}, "i": {"x": [x2] * dims, "y": [y2] * dims}}

    def channel(node: Node, prop: str, sub: int | None = None):
        """An animated Lottie property for this node, or None if no state animates it."""
        if not any(prop in (s["st"].get("tracks") or {}).get(node.id, {}) for s in timeline):
            return None
        dims = 1
        keys_out = []
        for s in timeline:
            keys = (s["st"].get("tracks") or {}).get(node.id, {}).get(prop)
            pick = (lambda v: [v[sub]]) if sub is not None else (lambda v: v)
            if prop == "path":
                rest_v = [lottie_shape(morph_item(node).subs[0])]
            elif sub is not None:
                rest_v = [rest_value(node, prop)[sub]]
            else:
                rest_v = lottie_value(node, prop, rest_value(node, prop))
            if not keys:
                keys_out.append({"t": s["start"], "s": rest_v, "h": 1})
                continue
            seq = []
            if float(keys[0]["t"]) > 0:
                seq.append((0.0, rest_v, "inOut"))
            for k in keys:
                v = pick(k["v"]) if sub is not None else lottie_value(node, prop, k["v"])
                seq.append((float(k["t"]), v, k.get("ease", "inOut")))
            for j, (t, v, e) in enumerate(seq):
                kf = {"t": s["start"] + round(t * fr / 1000), "s": v}
                if j == len(seq) - 1 or e == "hold":
                    kf["h"] = 1
                else:
                    kf.update(ease_obj(e, dims))
                keys_out.append(kf)
        return {"a": 1, "k": keys_out}

    def static(v):
        return {"a": 0, "k": v}

    layers = []  # in draw order (bottom first); reversed at the end
    index = {"n": 0}

    def new_ind():
        index["n"] += 1
        return index["n"]

    def emit(node: Node, parent_ind: int | None):
        is_root = node is rig.root
        trim = None
        opacity = static(100) if is_root else (channel(node, "opacity") or static(rest_value(node, "opacity")))
        path_prop = None if is_root else channel(node, "path")
        if not is_root:
            ts, te = channel(node, "trim", 0), channel(node, "trim", 1)
            if ts or te:
                trim = {"s": ts or static(0), "e": te or static(100)}
        px, py = node.pivot
        if is_root:
            ks_main = {"a": static([px, py, 0]), "p": static([px, py, 0]), "s": static([100, 100, 100]),
                       "r": static(0), "o": static(100)}
        else:
            ks_main = {"a": static([px, py, 0]),
                       "p": channel(node, "position") or static(lottie_value(node, "position", rest_value(node, "position"))),
                       "s": channel(node, "scale") or static(lottie_value(node, "scale", rest_value(node, "scale"))),
                       "r": channel(node, "rotation") or static(rest_value(node, "rotation")),
                       "o": opacity}
        # Runs: consecutive own shapes between nested groups. The first run is the group's layer;
        # later runs are identity children of it, so z-order matches the SVG.
        runs, cur = [], []
        for c in node.children:
            if isinstance(c, Item):
                cur.append(c)
            else:
                runs.append(cur)
                runs.append(c)
                cur = []
        runs.append(cur)
        main_ind = None
        k = 0
        for r in runs:
            if isinstance(r, Node):
                emit(r, None if is_root else main_ind)
                continue
            if main_ind is not None and not r:
                continue
            if main_ind is None and is_root and not r:
                main_ind = None
                continue
            ind = new_ind()
            shapes = [lottie_group(it, trim, path_prop) for it in reversed(r)]
            name = node.id if k == 0 else f"{node.id}+{k}"
            base = {"ddd": 0, "ind": ind, "nm": name, "sr": 1, "ao": 0, "ip": 0, "op": op, "st": 0, "bm": 0}
            if main_ind is None:
                base["ty"] = 4 if r else 3
                base["ks"] = ks_main
                if parent_ind is not None:
                    base["parent"] = parent_ind
                main_ind = ind
            else:
                base["ty"] = 4
                base["ks"] = {"a": static([px, py, 0]), "p": static([px, py, 0]), "s": static([100, 100, 100]),
                              "r": static(0), "o": opacity}
                base["parent"] = main_ind
            if base["ty"] == 4:
                base["shapes"] = shapes
            layers.append(base)
            k += 1

    emit(rig.root, None)
    return {"v": "5.7.4", "fr": fr, "ip": 0, "op": op, "w": round(rig.w), "h": round(rig.h), "nm": rig.name, "ddd": 0,
            "assets": [], "layers": list(reversed(layers)),
            "markers": [{"tm": s["start"], "cm": s["name"], "dr": s["dur"]} for s in timeline],
            "meta": {"g": "app-ui-slopless mascot.py",
                     "states": [{"name": s["name"], "loop": s["loop"], "ms": s["ms"]} for s in timeline]}}


def bezier_ease(x1, y1, x2, y2, x):
    """y for x on cubic-bezier(x1, y1, x2, y2), by bisection (x is monotonic for 0 <= x1, x2 <= 1)."""
    lo, hi = 0.0, 1.0
    for _ in range(40):
        t = (lo + hi) / 2
        bx = 3 * (1 - t) ** 2 * t * x1 + 3 * (1 - t) * t * t * x2 + t ** 3
        lo, hi = (t, hi) if bx < x else (lo, t)
    t = (lo + hi) / 2
    return 3 * (1 - t) ** 2 * t * y1 + 3 * (1 - t) * t * t * y2 + t ** 3


def prop_at(prop: dict, f: float):
    if not prop.get("a"):
        return prop["k"]
    ks = prop["k"]
    if f <= ks[0]["t"]:
        return ks[0]["s"]
    for a, b in zip(ks, ks[1:]):
        if a["t"] <= f < b["t"]:
            if a.get("h") or not isinstance(a["s"][0], (int, float)):
                return a["s"]
            x = (f - a["t"]) / (b["t"] - a["t"])
            y = bezier_ease(a["o"]["x"][0], a["o"]["y"][0], a["i"]["x"][0], a["i"]["y"][0], x)
            return [va + (vb - va) * y for va, vb in zip(a["s"], b["s"])]
    return ks[-1]["s"]


def canvas_overflow(data: dict) -> list[str]:
    """Where drawn shapes leave the Lottie canvas (players clip there), per state."""
    layers = {l["ind"]: l for l in data["layers"]}

    def local(l, f):
        ks = l["ks"]
        a, p, s, r = prop_at(ks["a"], f), prop_at(ks["p"], f), prop_at(ks["s"], f), prop_at(ks["r"], f)
        r = math.radians(r[0] if isinstance(r, list) else r)
        m = (1, 0, 0, 1, p[0], p[1])
        m = mul(m, (math.cos(r), math.sin(r), -math.sin(r), math.cos(r), 0, 0))
        m = mul(m, (s[0] / 100, 0, 0, s[1] / 100, 0, 0))
        return mul(m, (1, 0, 0, 1, -a[0], -a[1]))

    def world(l, f):
        m = local(l, f)
        while "parent" in l:
            l = layers[l["parent"]]
            m = mul(local(l, f), m)
        return m

    def points(l):
        pts = []
        for g in l.get("shapes", []):
            pad = max([it["w"]["k"] / 2 for it in g["it"] if it["ty"] == "st"] or [0])
            for it in g["it"]:
                if it["ty"] != "sh":
                    continue
                shapes = [it["ks"]["k"]] if not it["ks"].get("a") else [k["s"][0] for k in it["ks"]["k"]]
                for sh in shapes:
                    for v, i, o in zip(sh["v"], sh["i"], sh["o"]):
                        for q in (v, (v[0] + i[0], v[1] + i[1]), (v[0] + o[0], v[1] + o[1])):
                            pts += [(q[0] - pad, q[1] - pad), (q[0] + pad, q[1] + pad),
                                    (q[0] - pad, q[1] + pad), (q[0] + pad, q[1] - pad)]
        return pts

    w, h = data["w"], data["h"]
    out = []
    for mk in data.get("markers", []):
        hits = {}
        for f in range(mk["tm"], mk["tm"] + mk["dr"] + 1):
            for l in data["layers"]:
                if l.get("ty") != 4:
                    continue
                o = prop_at(l["ks"]["o"], f)
                if (o[0] if isinstance(o, list) else o) <= 0:
                    continue
                m = world(l, f)
                over = 0.0
                for q in points(l):
                    x, y = apply(m, q)
                    over = max(over, -x, -y, x - w, y - h)
                if over > 0.5:
                    first, last, worst = hits.get(l["nm"], (f, f, 0.0))
                    hits[l["nm"]] = (first, f, max(worst, over))
        for nm, (first, last, worst) in hits.items():
            ms = lambda fr_: round((fr_ - mk["tm"]) * 1000 / data["fr"])
            out.append(f"state {mk['cm']!r}: #{nm} leaves the {w}x{h} canvas at {ms(first)}-{ms(last)} ms by about "
                       f"{worst:.0f} units (players clip it): add headroom to the viewBox or move less")
    return out


REQUIRED = ("v", "fr", "ip", "op", "w", "h", "layers")


def validate_lottie(d: dict) -> list[str]:
    problems = [f"missing top-level key {k!r}" for k in REQUIRED if k not in d]
    inds = {l.get("ind") for l in d.get("layers", [])}
    for l in d.get("layers", []):
        if "parent" in l and l["parent"] not in inds:
            problems.append(f"layer {l.get('nm')} has a parent {l['parent']} that doesn't exist")
        if l.get("ty") == 4 and not isinstance(l.get("shapes"), list):
            problems.append(f"shape layer {l.get('nm')} has no shapes list")
    if d.get("op", 0) <= d.get("ip", 0):
        problems.append("op must be after ip")
    return problems


# ---------------------------------------------------------------- preview

PREVIEW = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Lottie preview</title>
<script src="{lottie}"></script>
<style>
  html, body {{ margin: 0; background: {bg}; font: 14px/1.4 -apple-system, system-ui, sans-serif; color: #1b1a17; }}
  #stage {{ position: absolute; left: 0; top: 0; width: {size}px; height: {size}px; }}
  #clock {{ position: absolute; left: 0; top: 0; width: 1px; height: 1px; opacity: 0; pointer-events: none; }}
  #ui {{ position: absolute; left: 12px; top: {ui_top}px; display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
  button {{ font: inherit; padding: 8px 14px; min-height: 44px; border: 2px solid #1b1a17; border-radius: 10px; background: #fff; }}
</style></head>
<body>
<div id="stage"></div><div id="clock"></div>
<div id="ui"></div>
<script>
/* Written by app-ui-slopless scripts/mascot.py preview. Mode: {mode}.
   clock:  a Web Animation on #clock drives lottie-web each frame, so document.getAnimations() sees the
           motion and scripts/filmstrip.py can pause it at time t and measure it.
   frames: no clock; ?t=<ms> calls goToAndStop(t) once, for stepping frame by frame.
   #play plays the first non-looping state (the reaction); #state=<name> plays that state; else the first. */
var DATA = {data};
var MODE = "{mode}";
(function () {{
  var states = (DATA.meta && DATA.meta.states) || DATA.markers.map(function (m, i) {{ return {{ name: m.cm, loop: i === 0, ms: m.dr / DATA.fr * 1000 }}; }});
  var h = decodeURIComponent(location.hash.slice(1));
  var pick = h === 'play' ? states.filter(function (s) {{ return !s.loop; }})[0] : null;
  if (h.indexOf('state=') === 0) pick = states.filter(function (s) {{ return s.name === h.slice(6); }})[0];
  var state = pick || states[0];
  var marker = DATA.markers.filter(function (m) {{ return m.cm === state.name; }})[0];
  var anim = lottie.loadAnimation({{ container: document.getElementById('stage'), renderer: 'svg', loop: false, autoplay: false, animationData: DATA }});
  var ready = false, lastT = -1;
  function frameAt(t) {{
    var ms = marker.dr / DATA.fr * 1000;
    var local = state.loop ? (t % ms) : Math.min(Math.max(t, 0), ms);
    return marker.tm + local / 1000 * DATA.fr;
  }}
  function show(t) {{ if (ready) anim.goToAndStop(frameAt(t), true); }}
  var q = location.search.match(/[?&]t=(\\d+(?:\\.\\d+)?)/);
  var tq = q ? +q[1] : null;
  var clock = null;
  if (MODE === 'clock') {{
    clock = document.getElementById('clock').animate([{{ transform: 'translateX(0px)' }}, {{ transform: 'translateX(1px)' }}],
      {{ duration: state.ms, iterations: state.loop ? Infinity : 1, fill: 'forwards' }});
    if (tq !== null) {{ clock.pause(); clock.currentTime = tq; }}
    (function tick() {{
      var t = clock.currentTime || 0;
      if (t !== lastT) {{ lastT = t; show(t); }}
      requestAnimationFrame(tick);
    }})();
  }}
  anim.addEventListener('DOMLoaded', function () {{
    ready = true;
    show(MODE === 'clock' ? (clock.currentTime || 0) : (tq || 0));
    document.documentElement.setAttribute('data-mascot', JSON.stringify({{ state: state.name, loop: state.loop, ms: state.ms }}));
  }});
  var ui = document.getElementById('ui');
  states.forEach(function (s) {{
    var b = document.createElement('button');
    b.textContent = 'Play ' + s.name + (s.loop ? ' (loop)' : '') + ' · ' + Math.round(s.ms) + ' ms';
    b.onclick = function () {{ location.hash = s.loop ? 'state=' + s.name : (s === states.filter(function (x) {{ return !x.loop; }})[0] ? 'play' : 'state=' + s.name); location.reload(); }};
    ui.appendChild(b);
  }});
}})();
</script>
</body></html>
"""


def write_preview(data: dict, out: Path, size: int, frames: bool, bg: str) -> None:
    out.write_text(PREVIEW.format(title=data.get("nm", "mascot"), lottie=LOTTIE_WEB, size=size, ui_top=size + 12,
                                  data=json.dumps(data, separators=(",", ":")), mode="frames" if frames else "clock",
                                  bg=bg))


# ---------------------------------------------------------------- check sheet (silhouette, squint, sizes)

def svg_path_d(subs: list[Sub]) -> str:
    out = []
    for s in subs:
        out.append(f"M{fmt(s.start[0])} {fmt(s.start[1])}")
        for seg in s.segs:
            if seg[0] == "L":
                out.append(f"L{fmt(seg[1][0])} {fmt(seg[1][1])}")
            else:
                out.append("C" + " ".join(f"{fmt(p[0])} {fmt(p[1])}" for p in seg[1:]))
        if s.closed:
            out.append("Z")
    return "".join(out)


def rest_svg(rig: Rig) -> str:
    """The rig at its rest pose as a flat, normalised SVG (absolute paths, no classes)."""

    def items_svg(n: Node, op: float) -> str:
        out = []
        for c in n.children:
            if isinstance(c, Item):
                a = [f'd="{svg_path_d(c.subs)}"']
                a.append(f'fill="{hex_of(c.fill)}"' if c.fill is not None else 'fill="none"')
                if c.fill is not None and c.fill_op * op < 1:
                    a.append(f'fill-opacity="{fmt(c.fill_op * op)}"')
                if c.rule == "evenodd":
                    a.append('fill-rule="evenodd"')
                if c.stroke is not None:
                    a += [f'stroke="{hex_of(c.stroke)}"', f'stroke-width="{fmt(c.width)}"',
                          f'stroke-linecap="{c.cap}"', f'stroke-linejoin="{c.join}"']
                    if c.stroke_op * op < 1:
                        a.append(f'stroke-opacity="{fmt(c.stroke_op * op)}"')
                out.append(f"<path {' '.join(a)}/>")
            else:
                r = rest_pose(c)
                px, py = c.pivot
                tf = (f"translate({fmt(px + r['dx'])} {fmt(py + r['dy'])}) rotate({fmt(r['rot'])}) "
                      f"scale({fmt(r['sx'])} {fmt(r['sy'])}) translate({fmt(-px)} {fmt(-py)})")
                out.append(f'<g id="{c.id}" transform="{tf}">{items_svg(c, r["op"])}</g>')
        return "".join(out)

    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(rig.w)} {fmt(rig.h)}">'
            f"{items_svg(rig.root, 1.0)}</svg>")


CHECK = """<!doctype html><meta charset="utf-8"><style>
  html, body {{ margin: 0; background: {bg}; font: 13px/1.3 -apple-system, system-ui, sans-serif; color: #1b1a17; }}
  #grid {{ display: flex; gap: 28px; padding: 20px; align-items: flex-end; }}
  .cell {{ display: flex; flex-direction: column; gap: 8px; align-items: flex-start; }}
  .cell svg {{ display: block; }}
  .cell > div:last-child {{ white-space: nowrap; }}
  .sil svg {{ filter: brightness(0); }}
  .squint svg {{ filter: grayscale(1) blur({blur}px); }}
  .on-ink {{ background: {ink}; padding: 8px; border-radius: 8px; }}
</style>
<div id="grid">
  <div class="cell"><div>{svg160}</div><div>160 px</div></div>
  <div class="cell squint"><div>{svg160}</div><div>squint (grey + blur)</div></div>
  <div class="cell"><div>{svg48}</div><div>48 px</div></div>
  <div class="cell"><div>{svg24}</div><div>24 px</div></div>
  <div class="cell sil"><div>{svg48}</div><div>silhouette 48</div></div>
  <div class="cell sil"><div>{svg24}</div><div>silhouette 24</div></div>
  <div class="cell on-ink"><div>{svg48}</div></div>
</div>"""


def check_sheet(rig: Rig, out_png: Path, bg: str) -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from filmstrip import find_chrome  # noqa: E402

    svg = rest_svg(rig)
    sized = lambda px: svg.replace("<svg ", f'<svg width="{px}" height="{round(px * rig.h / rig.w)}" ', 1)
    colors = rig.colors()
    ink = max(colors, key=lambda h: -sum(parse_color(h, {}))) if colors else "#1b1a17"
    html_path = out_png.with_suffix(".html")
    html_path.write_text(CHECK.format(bg=bg, svg160=sized(160), svg48=sized(48), svg24=sized(24), blur=3, ink=ink))
    chrome = find_chrome()
    print(f"mascot check: {len(colors)} colour(s): {', '.join(colors)}"
          + ("  (more than 3: does each one earn its place?)" if len(colors) > 3 else ""))
    parts = rig.nodes()
    print(f"mascot check: {len(parts)} rig part(s): {', '.join(n.id for n in parts) or 'none (a static glyph)'}")
    if not chrome:
        print(f"mascot check: not rendered, no Chromium-based browser (set CHROME=/path). Sheet: {html_path}")
        return 3
    r = subprocess.run([chrome, "--headless=new", "--hide-scrollbars", "--no-first-run", "--disable-gpu",
                        "--window-size=780,240", "--force-device-scale-factor=2", "--force-color-profile=srgb", f"--screenshot={out_png.resolve()}",
                        html_path.resolve().as_uri()], capture_output=True, text=True, timeout=120)
    if r.returncode != 0 or not out_png.exists():
        print(f"mascot check: screenshot failed: {(r.stderr or '').strip()[-300:]}")
        return 1
    html_path.unlink()
    print(f"mascot check: wrote {out_png}. Judge it with references/mascot.md: the silhouette names the character at 24 px, "
          "the squint keeps the face, the eyes read at 24 px.")
    return 0


# ---------------------------------------------------------------- single-file briefs

BEGIN = "// ---- mascot.py svg2code: {name} (generated from {svg}; edit the SVG and rerun, not this block) ----"
END = "// ---- end mascot.py svg2code: {name} ----"


def merge_into(target: Path, code: str, name: str, svg: str) -> str:
    """Put generated code into an existing screen file: imports merged, package line dropped,
    body in a marked block at the end. Rerunning replaces the block, so it stays regenerable."""
    text = target.read_text()
    lines = code.splitlines()
    imports = [l for l in lines if l.startswith("import ")]
    body = [l for l in lines if not l.startswith(("import ", "package ")) and not l.startswith("// Generated by")]
    while body and not body[0].strip():
        body.pop(0)
    begin, end = BEGIN.format(name=name, svg=svg), END.format(name=name)
    if begin.split(" (")[0] in text:   # replace the earlier block for this mascot
        start = text.index(begin.split(" (")[0])
        stop = text.index(end, start) + len(end) if end in text[start:] else len(text)
        text = text[:start].rstrip("\n") + "\n" + text[stop:].lstrip("\n")
    have = set(re.findall(r"^import .+$", text, re.M))
    missing = [l for l in imports if l not in have]
    if missing:
        last = list(re.finditer(r"^import .+$", text, re.M))
        if last:
            at = last[-1].end()
            text = text[:at] + "\n" + "\n".join(missing) + text[at:]
        else:
            pkg = re.search(r"^package .+$", text, re.M)
            at = pkg.end() if pkg else 0
            text = text[:at] + ("\n\n" if pkg else "") + "\n".join(missing) + ("\n" if not pkg else "") + text[at:]
    return text.rstrip("\n") + "\n\n" + begin + "\n" + "\n".join(body).rstrip("\n") + "\n" + end + "\n"


# ---------------------------------------------------------------- CLI

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("svg2code", help="SVG to a SwiftUI view or a Compose ImageVector + painter")
    a.add_argument("svg")
    g = a.add_mutually_exclusive_group(required=True)
    g.add_argument("--swift", action="store_true")
    g.add_argument("--compose", action="store_true")
    a.add_argument("--name", help="type prefix (default: the file name in PascalCase)")
    a.add_argument("--package", help="Kotlin package line (Compose)")
    a.add_argument("-o", "--out", help="output file (default: stdout)")
    a.add_argument("--into", help="an existing screen file to add the code to (single-file briefs): imports merged, "
                                  "code in a marked block at the end, replaced on rerun")
    b = sub.add_parser("lottie", help="rig SVG + motion spec to Lottie JSON")
    b.add_argument("svg")
    b.add_argument("motion")
    b.add_argument("-o", "--out", required=True)
    c = sub.add_parser("preview", help="HTML page that plays a Lottie and can be paused at time t")
    c.add_argument("lottie")
    c.add_argument("-o", "--out", help="default: <lottie>.preview.html")
    c.add_argument("--size", type=int, default=240, help="stage size in CSS px (default 240)")
    c.add_argument("--bg", default="#FFFFFF", help="page colour (use the direction's ground)")
    c.add_argument("--frames", action="store_true", help="no Web Animations clock: ?t=<ms> calls goToAndStop")
    d = sub.add_parser("check", help="silhouette / squint / small-size sheet as a PNG")
    d.add_argument("svg")
    d.add_argument("-o", "--out", help="default: <svg>-check.png")
    d.add_argument("--bg", default="#FFFFFF")
    args = ap.parse_args()

    try:
        if args.cmd == "svg2code":
            src = Path(args.svg)
            rig = load_svg(src)
            name = pascal(args.name or rig.name)
            code = to_swift(rig, name, src.name) if args.swift else to_compose(rig, name, args.package, src.name)
            if args.into:
                target = Path(args.into)
                if not target.exists():
                    raise MascotError(f"--into: {target} not found")
                target.write_text(merge_into(target, code, name, src.name))
                args.out = f"{target} (block {name})"
            elif args.out:
                Path(args.out).write_text(code)
            else:
                sys.stdout.write(code)
            n_items = sum(len(n.items()) for n in rig.root.walk())
            msg = (f"mascot svg2code: {n_items} shape(s), {len(rig.nodes())} rig part(s), {len(rig.colors())} colour(s)"
                   + (f" -> {args.out}" if args.out else ""))
            print(msg, file=sys.stderr)
        elif args.cmd == "lottie":
            rig = load_svg(Path(args.svg))
            try:
                spec = json.loads(Path(args.motion).read_text())
            except json.JSONDecodeError as e:
                raise MascotError(f"{args.motion}: not valid JSON ({e})")
            data = build_lottie(rig, spec)
            problems = validate_lottie(data)
            if problems:
                raise MascotError("; ".join(problems))
            for msg in canvas_overflow(data):
                note(msg)
            Path(args.out).write_text(json.dumps(data, separators=(",", ":")))
            st = data["meta"]["states"]
            print(f"mascot lottie: {len(data['layers'])} layer(s), {data['op']} frames at {data['fr']:g} fps, states: "
                  + ", ".join(f"{s['name']} {s['ms']:g} ms{' loop' if s['loop'] else ''}" for s in st)
                  + f" -> {args.out}")
        elif args.cmd == "preview":
            src = Path(args.lottie)
            data = json.loads(src.read_text())
            problems = validate_lottie(data)
            if problems:
                raise MascotError(f"{src}: " + "; ".join(problems))
            out = Path(args.out) if args.out else src.with_name(src.stem + ".preview.html")
            write_preview(data, out, args.size, args.frames, args.bg)
            here = Path(__file__).resolve().parent
            print(f"mascot preview: wrote {out} (lottie-web {LOTTIE_WEB.split('/')[-2]} from cdnjs; needs network)")
            print(f"  filmstrip: python3 {here / 'filmstrip.py'} {out} --crop 0,0,{args.size},{args.size} "
                  f"--times 0,80,160,240,320,480,640,880")
        elif args.cmd == "check":
            src = Path(args.svg)
            rig = load_svg(src)
            out = Path(args.out) if args.out else src.with_name(src.stem + "-check.png")
            rc = check_sheet(rig, out, args.bg)
            for n in notes:
                print(f"mascot: note: {n}", file=sys.stderr)
            return rc
    except MascotError as e:
        print(f"mascot: error: {e}", file=sys.stderr)
        return 1
    for n in notes:
        print(f"mascot: note: {n}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
