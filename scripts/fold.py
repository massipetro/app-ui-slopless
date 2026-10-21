#!/usr/bin/env python3
"""Measure the bottom edge of an HTML mock: is any row cut by the pinned bar?

  fold.py mock.html [--size 390x844] [--bar <css selector>] [--scroll <css selector>]

Looking at a screenshot, a sliver of card border above a tab bar is easy to miss; a run
missed it in three rounds of evals. This script measures it instead. It loads the mock at
the exact phone viewport, finds the pinned bottom bar (the widest element fixed, absolute
or sticky at the bottom edge; or --bar) and the scrolling container (or --scroll), and
reports every row near the bar's top edge in two frames:

  rest  the mock as it opens. Each row whose box comes within 24 px of the bar is
        whole    : fully above the bar (or fully hidden under it)
        cut      : any part of the row shows above the bar's top edge while the rest is under it:
                   a sliver of card, a row sliced through its icon or its text. A fade above the
                   bar doesn't excuse it; blind judges capped every such row in our evals.
                   (A plain divider line peeking out is fine.)
        orphaned : a section heading shows above the bar while its rows start under it (round 14).
  end   the container scrolled to the bottom: the last row must clear the bar by 8 px.

A "row" is the outermost painted box (background, border, shadow, image) inside the
scrolling content, so a card counts once, not once per icon. A line of plain text that
crosses the edge counts too.

Exit 0: no cut row and the end frame clears. Exit 1: a cut row or too little clearance
(fix it: move the fold into a gap between rows, or add a short fade above an opaque bar,
then rerun). Exit 3: no Chromium-based browser here (say "fold not measured").

Standard library only; works on Python 3.9. Uses the same browser lookup as filmstrip.py.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from filmstrip import find_chrome  # noqa: E402

PROBE = r"""<script>/* fold.py probe */(function () {
  var cfg = JSON.parse(decodeURIComponent((location.search.match(/[?&]fold=([^&]*)/) || [, '%7B%7D'])[1]));
  function px(v) { return parseFloat(v) || 0; }
  var PINNED = [];   // the bar and anything stacked on it: never content
  function pinned(node) { return PINNED.some(function (p) { return p.contains(node); }); }
  function painted(el) {
    var cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || px(cs.opacity) === 0 || cs.display === 'none') return false;
    if (/^(IMG|SVG|CANVAS|VIDEO|PICTURE)$/i.test(el.tagName)) return true;
    var bg = cs.backgroundColor, a = bg.match(/rgba?\(([^)]+)\)/);
    if (a && (a[1].split(',')[3] === undefined || px(a[1].split(',')[3]) > 0.05)) return true;
    if (cs.backgroundImage && cs.backgroundImage !== 'none') return true;
    if (cs.boxShadow && cs.boxShadow !== 'none') return true;
    return ['Top', 'Right', 'Bottom', 'Left'].some(function (s) {
      return px(cs['border' + s + 'Width']) > 0 && !/rgba\(.*,\s*0\)$|transparent/.test(cs['border' + s + 'Color']);
    });
  }
  function solid(el) {   // paints an opaque surface (a gradient fade doesn't count)
    var cs = getComputedStyle(el), a = cs.backgroundColor.match(/rgba?\(([^)]+)\)/);
    if (cs.visibility === 'hidden' || px(cs.opacity) < 0.5) return false;
    return !!a && (a[1].split(',')[3] === undefined || px(a[1].split(',')[3]) >= 0.5);
  }
  function cardLike(el) {   // a sliver of this reads as a cut card: own fill, side borders or a shadow
    var cs = getComputedStyle(el);
    if (/^(IMG|SVG|CANVAS|VIDEO|PICTURE)$/i.test(el.tagName)) return true;
    if (cs.boxShadow && cs.boxShadow !== 'none') return true;
    if (px(cs.borderLeftWidth) > 0 || px(cs.borderRightWidth) > 0) return true;
    if (!solid(el) && !(cs.backgroundImage && cs.backgroundImage !== 'none')) return false;
    var p = el.parentElement;
    while (p && !solid(p)) p = p.parentElement;
    return !p || getComputedStyle(p).backgroundColor !== cs.backgroundColor;
  }
  function findBar(vw, vh) {
    if (cfg.bar) return document.querySelector(cfg.bar);
    var best = null;
    document.querySelectorAll('body *').forEach(function (el) {
      var cs = getComputedStyle(el); if (!/fixed|absolute|sticky/.test(cs.position)) return;
      var r = el.getBoundingClientRect();
      if (r.bottom < vh - 40 || r.width < vw * 0.6 || r.height < 36 || r.height > 260 || r.top < vh * 0.5) return;
      if (ownTop(el, vw) === null) return;   // nothing solid: a decoration or an empty wrapper, not a bar
      if (!best || r.top < best.getBoundingClientRect().top) best = el;
    });
    return best;
  }
  function findScroll(bar) {
    if (cfg.scroll) return document.querySelector(cfg.scroll);
    var best = null;
    document.querySelectorAll('body *').forEach(function (el) {
      if (bar && (bar === el || bar.contains(el))) return;
      var cs = getComputedStyle(el);
      if (!/auto|scroll/.test(cs.overflowY) || el.scrollHeight <= el.clientHeight + 1) return;
      if (!best || el.clientHeight > best.clientHeight) best = el;
    });
    return best || document.scrollingElement;
  }
  function fadeTop(bar, scroller, barTop) {
    var top = null;
    var consider = function (t) { if (t !== null && t < barTop - 2 && t > barTop - 80) top = top === null ? t : Math.min(top, t); };
    var pre = getComputedStyle(bar, '::before');
    if (pre.content !== 'none' && /gradient/.test(pre.backgroundImage)) consider(barTop - px(pre.height));
    document.querySelectorAll('body *').forEach(function (el) {
      if (scroller.contains(el)) return;
      var cs = getComputedStyle(el); if (!/gradient/.test(cs.backgroundImage)) return;
      var r = el.getBoundingClientRect();
      if (Math.abs(r.bottom - barTop) <= 6 && r.height <= 80 && r.width > 100) consider(r.top);
    });
    var m = getComputedStyle(scroller).webkitMaskImage || getComputedStyle(scroller).maskImage || '';
    if (/gradient/.test(m)) { var sr = scroller.getBoundingClientRect(); consider(Math.min(barTop, sr.bottom) - 40); }
    return top;
  }
  function textLines(root) {
    var out = [], w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    for (var n = w.nextNode(); n; n = w.nextNode()) {
      if (!n.nodeValue.trim() || pinned(n)) continue;
      var cs = getComputedStyle(n.parentElement); if (cs.visibility === 'hidden' || px(cs.opacity) === 0) continue;
      var rg = document.createRange(); rg.selectNodeContents(n);
      Array.prototype.forEach.call(rg.getClientRects(), function (r) { if (r.height > 4) out.push({ r: r, t: n.nodeValue.trim().slice(0, 40) }); });
    }
    return out;
  }
  function textStyle(el) {   // the computed style of the first visible text inside el
    var w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    for (var n = w.nextNode(); n; n = w.nextNode()) if (n.nodeValue.trim()) return getComputedStyle(n.parentElement);
    return getComputedStyle(el);
  }
  function headingLike(h, next) {   // a title over its section, not just the first of equal rows
    if (/^H[1-6]$/.test(h.tagName) || h.getAttribute('role') === 'heading' || /head|title|label|caption|eyebrow|rule/i.test(String(h.className))) return true;
    var a = textStyle(h), b = textStyle(next);
    return Math.abs(px(a.fontSize) - px(b.fontSize)) >= 1 || Math.abs(px(a.fontWeight) - px(b.fontWeight)) >= 200 || a.textTransform !== b.textTransform;
  }
  function label(el) {
    var t = (el.innerText || el.getAttribute('aria-label') || el.tagName).replace(/\s+/g, ' ').trim();
    return t.slice(0, 48) || el.tagName.toLowerCase();
  }
  function frame(bar, scroller, barTop, fade) {
    var boxes = [];
    (function walk(el) {
      Array.prototype.forEach.call(el.children, function (c) {
        if (pinned(c)) return;
        if (PINNED.some(function (p) { return c.contains(p); })) { walk(c); return; }
        var r = c.getBoundingClientRect();
        var container = r.height > innerHeight * 0.35 && c.children.length >= 2;
        if (r.height >= 12 && r.width >= 24 && painted(c) && !container) boxes.push(c); else walk(c);
      });
    })(scroller === document.scrollingElement ? document.body : scroller);
    var rows = [];
    boxes.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.bottom < barTop - 24 || r.top >= barTop) return;
      var crosses = r.top < barTop - 0.5 && r.bottom > barTop + 0.5;   // even 1 px of a card's top edge shows
      var cutText = textLines(el).filter(function (l) { return l.r.top < barTop - 3 && l.r.bottom > barTop + 3; });
      // Strict: under a pinned bar a row is whole or hidden. A sliver, or a row sliced through its icon or
      // text, reads as cut, with or without a fade (the blind judges capped every one of them).
      var shows = barTop - r.top, state, why = '';
      var cutMedia = Array.prototype.some.call(el.querySelectorAll('img, svg, canvas, video'), function (m) {
        var mr = m.getBoundingClientRect(); return mr.height > 4 && mr.top < barTop - 0.5 && mr.bottom > barTop + 0.5; });
      if (!crosses) state = 'whole';
      else if (cutText.length) { state = 'cut'; why = 'text "' + cutText[0].t + '" crosses the bar'; }
      else if (!cardLike(el) && !cutMedia) { state = 'whole'; why = 'only its divider shows'; }
      else { state = 'cut'; why = Math.round(shows) + ' px of a ' + Math.round(r.height) + ' px row show above the bar' + (cutMedia ? ', its icon sliced' : '') + '; land the fold in a gap'; }
      rows.push({ row: label(el), top: Math.round(r.top), bottom: Math.round(r.bottom), gap: Math.round(barTop - r.bottom), state: state, why: why });
    });
    // Plain text outside any painted box
    textLines(scroller === document.scrollingElement ? document.body : scroller).forEach(function (l) {
      if (l.r.top < barTop - 3 && l.r.bottom > barTop + 3 && !boxes.some(function (b) { var r = b.getBoundingClientRect(); return r.top <= l.r.top && r.bottom >= l.r.bottom && r.left <= l.r.left && r.right >= l.r.right; }))
        rows.push({ row: 'text "' + l.t + '"', top: Math.round(l.r.top), bottom: Math.round(l.r.bottom), gap: Math.round(barTop - l.r.bottom), state: 'cut', why: 'a line of text crosses the bar' });
    });
    // An orphaned heading: a section's title shows above the bar while everything under it starts below the
    // bar's top edge. Nothing crosses the edge, yet the judges read the section as cut (round 14).
    (function sections(el) {
      Array.prototype.forEach.call(el.children, function (c) {
        if (pinned(c)) return;
        var kids = Array.prototype.filter.call(c.children, function (k) { return k.getBoundingClientRect().height > 0; });
        if (kids.length >= 2) {
          var h = kids[0], hr = h.getBoundingClientRect(), nr = kids[1].getBoundingClientRect();
          var lines = textLines(h), textBottom = lines.reduce(function (m, l) { return Math.max(m, l.r.bottom); }, -1);
          // Judge by the heading's text, not its box: padding may run under the bar while every word shows.
          if (lines.length && hr.height <= 48 && textBottom <= barTop + 1 && textBottom > barTop - 64 &&
              nr.top >= barTop - 1 && headingLike(h, kids[1]))
            rows.push({ row: 'heading "' + label(h) + '"', top: Math.round(hr.top), bottom: Math.round(hr.bottom), gap: Math.round(barTop - hr.bottom),
                        state: 'cut', why: 'its section starts under the bar, so the heading is orphaned above it; land the fold above the heading' });
        }
        sections(c);
      });
    })(scroller === document.scrollingElement ? document.body : scroller);
    var last = boxes.reduce(function (m, el) {   // rows only: a full-height backdrop isn't the last row
      var r = el.getBoundingClientRect(); if (r.height > innerHeight * 0.35) return m;
      return !m || r.bottom > m.bottom ? { bottom: r.bottom, row: label(el) } : m; }, null);
    textLines(scroller === document.scrollingElement ? document.body : scroller).forEach(function (l) {
      if (!last || l.r.bottom > last.bottom) last = { bottom: l.r.bottom, row: 'text "' + l.t + '"' };
    });
    return { rows: rows, last: last };
  }
  function surfaceTop(bar, vw) {
    // The pinned stack's visible top edge: a buy bar sitting on a tab bar counts as one bar.
    var top = ownTop(bar, vw), moved = true;
    if (top === null) top = bar.getBoundingClientRect().top;
    if (PINNED.indexOf(bar) < 0) PINNED.push(bar);
    while (moved) {
      moved = false;
      document.querySelectorAll('body *').forEach(function (el) {
        if (el === bar || bar.contains(el) || el.contains(bar)) return;
        var cs = getComputedStyle(el); if (!/fixed|absolute|sticky/.test(cs.position)) return;
        var r = el.getBoundingClientRect();
        if (r.width < vw * 0.5 || r.bottom < top - 6 || r.top >= top || r.height > 200) return;
        var t = ownTop(el, vw); if (t !== null && t < top) { top = t; moved = true; PINNED.push(el); }
      });
    }
    return top;
  }
  function ownTop(bar, vw) {
    // Its own visible top edge: itself if it paints, else its widest solid surface (a wrapper may be transparent).
    if (solid(bar)) return bar.getBoundingClientRect().top;
    var wide = null, any = null;
    bar.querySelectorAll('*').forEach(function (el) {
      if (!solid(el)) return;
      var r = el.getBoundingClientRect(); if (r.height < 8) return;
      if (r.width >= vw * 0.6) wide = wide === null ? r.top : Math.min(wide, r.top);
      any = any === null ? r.top : Math.min(any, r.top);
    });
    return wide !== null ? wide : any;   // null: nothing solid (a fade or an empty wrapper)
  }
  function run() {
    var vw = innerWidth, vh = innerHeight, bar = findBar(vw, vh), res = { viewport: [vw, vh] };
    if (!bar) { res.error = 'no pinned bottom bar found (pass --bar <selector> if there is one)'; return parent.postMessage({ fold: res }, '*'); }
    var scroller = findScroll(bar);
    var barTop = surfaceTop(bar, vw), bcs = getComputedStyle(bar);
    var fade = fadeTop(bar, scroller, barTop);
    res.bar = { label: label(bar).slice(0, 30), top: Math.round(barTop), opaque: ownTop(bar, vw) !== null, position: bcs.position };
    res.fade = fade === null ? null : Math.round(barTop - fade);
    res.scroll = scroller === document.scrollingElement ? 'document' : (scroller.id ? '#' + scroller.id : scroller.tagName.toLowerCase() + (scroller.className ? '.' + String(scroller.className).split(' ')[0] : ''));
    res.rest = frame(bar, scroller, barTop, fade);
    var before = scroller.scrollTop;
    scroller.scrollTop = scroller.scrollHeight;
    var docLocked = scroller === document.scrollingElement &&
      (/hidden|clip/.test(getComputedStyle(document.body).overflowY) || /hidden|clip/.test(getComputedStyle(document.documentElement).overflowY));
    res.scrolls = scroller.scrollTop > before && !docLocked;   // overflow:hidden still scrolls from script, never by hand
    setTimeout(function () {
      var endTop = surfaceTop(bar, vw);
      res.end = frame(bar, scroller, endTop, fade);
      res.end.clearance = res.end.last ? Math.round(endTop - res.end.last.bottom) : null;
      parent.postMessage({ fold: res }, '*');
    }, 60);
  }
  // Measure the settled resting frame, as the screenshot shows it: fonts loaded, one-off animations finished.
  function settle() {
    document.getAnimations().forEach(function (a) {
      var tm = a.effect && a.effect.getComputedTiming(); if (tm && tm.endTime !== Infinity) { try { a.finish(); } catch (e) {} }
    });
    setTimeout(run, 80);
  }
  addEventListener('load', function () {
    setTimeout(function () { (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(settle, settle); }, 300);
  });
})();</script>"""

WRAP = """<!doctype html><meta charset="utf-8"><body style="margin:0"><pre id="out">no result</pre>
<iframe src="{src}" style="width:{w}px;height:{h}px;border:0;display:block"></iframe>
<script>addEventListener('message', function (e) {{ if (e.data && e.data.fold) document.getElementById('out').textContent = JSON.stringify(e.data.fold); }});</script>"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mock")
    ap.add_argument("--size", default="390x844", help="phone viewport in CSS px")
    ap.add_argument("--bar", help="CSS selector of the pinned bottom bar (default: detected)")
    ap.add_argument("--scroll", help="CSS selector of the scrolling container (default: detected)")
    ap.add_argument("--json", action="store_true", help="print the raw measurement too")
    args = ap.parse_args()

    mock = Path(args.mock)
    if not mock.exists():
        print(f"fold: {mock} not found")
        return 2
    chrome = find_chrome()
    if not chrome:
        print("fold: not measured, no Chromium-based browser found (set CHROME=/path). Check the fold by eye and say so.")
        return 3
    vw, vh = (int(v) for v in args.size.lower().split("x"))
    src = mock.read_text(errors="ignore")
    probe = mock.with_name(mock.stem + ".fold-probe.html")
    probe.write_text(src.replace("</body>", PROBE + "</body>") if "</body>" in src else src + PROBE)
    cfg = json.dumps({k: v for k, v in (("bar", args.bar), ("scroll", args.scroll)) if v})
    wrap = mock.with_name(mock.stem + ".fold.html")
    from urllib.parse import quote
    wrap.write_text(WRAP.format(src=html.escape(probe.name + "?fold=" + quote(cfg)), w=vw, h=vh))
    try:
        dom = subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-first-run", "--hide-scrollbars",
                              "--allow-file-access-from-files", "--blink-settings=preferredColorScheme=1",
                              "--force-prefers-reduced-motion",
                              "--virtual-time-budget=6000", f"--window-size={vw + 200},{vh + 200}", "--dump-dom",
                              wrap.resolve().as_uri()], capture_output=True, text=True, timeout=120).stdout
    finally:
        probe.unlink(missing_ok=True)
        wrap.unlink(missing_ok=True)
    m = re.search(r'<pre id="out">(.*?)</pre>', dom, re.S)
    if not m or not m.group(1).startswith("{"):
        print("fold: no measurement (the probe didn't run; is JavaScript blocked?)")
        return 1
    res = json.loads(html.unescape(m.group(1)))
    if args.json:
        print(json.dumps(res, indent=2))
    if res.get("error"):
        print(f"fold: {res['error']}")
        return 0
    bar = res["bar"]
    print(f"fold: bar '{bar['label']}' top at {bar['top']} px ({bar['position']}, {'opaque' if bar['opaque'] else 'TRANSPARENT'}); "
          f"fade above it: {str(res['fade']) + ' px' if res['fade'] else 'none'}; scrolls: {res['scroll']}")
    bad = 0
    print("rest frame:")
    if not res["rest"]["rows"]:
        print("  no row within 24 px of the bar (the fold sits in a gap)")
    for r in res["rest"]["rows"]:
        bad += r["state"] == "cut"
        detail = f"{r['gap']:+d} px clear" if r["state"] == "whole" else r["why"]
        print(f"  {r['state'].upper() if r['state'] == 'cut' else r['state']:5}  {r['row']!r}  ({detail})")
    end = res["end"]
    cl = end.get("clearance")
    print(f"end frame: last row {end['last']['row']!r} clears the bar by {cl} px" if end.get("last") else "end frame: no rows found")
    for r in end["rows"]:
        if r["state"] == "cut":
            bad += 1
            print(f"  CUT    {r['row']!r}  ({r['why']})")
    if cl is not None and cl < 8 and not res.get("scrolls", True):
        bad += 1
        print(f"  FAIL   the mock doesn't scroll, so rows stay under the bar ({-cl} px of content below its top edge): put the "
              "list in a container with overflow-y: auto (id=\"scroll\") and bottom padding of at least the bar's height")
    elif cl is not None and cl < 8:
        bad += 1
        print(f"  FAIL   the last row needs at least 8 px clear of the bar (has {cl}): pad the list's bottom by the bar's height")
    if not bar["opaque"]:
        print("  note: the bar paints no background, so content shows through it; give it an opaque surface with a visible top edge")
    print(f"fold {'pass' if not bad else 'FAIL'}: {bad} problem(s)")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
