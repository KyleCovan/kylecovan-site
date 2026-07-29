import json, pathlib, re, sys
from playwright.sync_api import sync_playwright

# Runs against the BUILT output, not the source. That is deliberate: what
# matters is the HTML a visitor receives, and Astro minifies the CSS and
# serialises the video array on the way through. Testing the source would
# test something nobody ever loads.
SRC  = (pathlib.Path(__file__).parent.parent / 'dist' / 'index.html').resolve()
URI  = SRC.as_uri()
HTML = SRC.read_text()
BG   = (0xFB, 0xF8, 0xF2)
fails = []

# Astro emits the array via JSON.stringify, so the shape is {"title":"…","url":"…"}
# rather than the hand-written { title: "…", url: "…" }.
TITLES = re.findall(r'\{"title":"((?:[^"\\]|\\.)*)","url":"([^"]+)"\}', HTML)
assert len(TITLES) == 32, f"expected 32 videos, found {len(TITLES)}"
DECODED = [t.replace('\\"', '"') for t, _ in TITLES]
LONGEST = max(DECODED, key=len)

CONTRAST_JS = r"""
() => {
  const lin = c => { c/=255; return c<=0.03928 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4); };
  const L = ([r,g,b]) => 0.2126*lin(r)+0.7152*lin(g)+0.0722*lin(b);
  const parse = s => s.match(/[\d.]+/g).slice(0,3).map(Number);
  const bgL = L([251,248,242]);
  const out = [];
  const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = walk.nextNode())) {
    if (!n.textContent.trim()) continue;
    const el = n.parentElement;
    if (!el || !el.offsetParent && el.tagName !== 'BODY') { }
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const fg = L(parse(cs.color));
    const ratio = (Math.max(fg,bgL)+0.05)/(Math.min(fg,bgL)+0.05);
    const px = parseFloat(cs.fontSize);
    const bold = (parseInt(cs.fontWeight,10) || 400) >= 700;
    const large = px >= 24 || (bold && px >= 18.66);
    out.push({text: n.textContent.trim().slice(0,44), color: cs.color, px,
              ratio: Math.round(ratio*100)/100, threshold: large ? 3 : 4.5,
              pass: ratio >= (large ? 3 : 4.5)});
  }
  return out;
}
"""

with sync_playwright() as pw:
    b = pw.chromium.launch(args=['--disable-lcd-text'])

    # --- 1. Contrast -------------------------------------------------
    pg = b.new_page(viewport={'width': 1440, 'height': 1000})
    pg.goto(URI); pg.wait_for_timeout(200)
    nodes = pg.evaluate(CONTRAST_JS)
    bad = [n for n in nodes if not n['pass']]
    print(f"[contrast]  {len(nodes)} text nodes checked, {len(bad)} failures")
    for n in bad: print("   FAIL", n); fails.append(('contrast', n))
    pg.close()

    # --- 2. Overflow at 320px, longest title forced ------------------
    pg = b.new_page(viewport={'width': 320, 'height': 800})
    pg.goto(URI); pg.wait_for_timeout(150)
    pg.evaluate("t => document.getElementById('watching-link').textContent = t", LONGEST)
    pg.wait_for_timeout(120)
    sw = pg.evaluate("document.documentElement.scrollWidth")
    ok = sw == 320
    print(f"[overflow]  320px w/ longest title forced -> scrollWidth={sw} {'OK' if ok else 'FAIL'}")
    if not ok: fails.append(('overflow', sw))
    pg.close()

    # --- 3. Top bar: containment, left edge, no collision ------------
    #
    # The old assertion was "every watching rect shares the h1's left edge".
    # That stopped describing the design when the nav joined the video line on
    # one row and the portrait moved left of the h1. What matters now:
    #   (a) the video line never escapes the column,
    #   (b) it never collides with the nav,
    #   (c) when it drops to its own flex row it lands flush on the column's
    #       left edge — the surviving half of §5's rule.
    #   (d) below 34rem (544px) the top bar becomes a column and the video
    #       line moves ABOVE the nav, centred in the column. Kyle asked for
    #       this on July 29 after seeing it on iOS. The flush-left assertion
    #       in (c) is therefore desktop-only; asserting it on a phone would
    #       now fail by design, which is exactly the kind of stale test the
    #       July two-page split taught us to update rather than delete.
    wraps = {}
    for w in (1440, 768, 430, 390, 320):
        pg = b.new_page(viewport={'width': w, 'height': 900})
        pg.goto(URI); pg.wait_for_timeout(150)
        n_wrapped, bad = 0, []
        for t in DECODED:
            r = pg.evaluate("""t => {
                const a = document.getElementById('watching-link');
                a.textContent = t;
                const p = a.closest('.watching').getBoundingClientRect();
                const nav = document.querySelector('.topnav').getBoundingClientRect();
                const col = document.querySelector('main').getBoundingClientRect();
                const rects = [...a.getClientRects()];
                const ownRow = p.top >= nav.bottom - 1;
                const aboveNav = p.bottom <= nav.top + 1;
                const collide = !(p.right <= nav.left + 1 || p.left >= nav.right - 1 ||
                                  p.bottom <= nav.top + 1 || p.top >= nav.bottom - 1);
                return {n: rects.length, ownRow, aboveNav, collide,
                        lefts: rects.map(x => Math.round(x.left*100)/100),
                        right: Math.round(Math.max(...rects.map(x => x.right))*100)/100,
                        colL: Math.round(col.left*100)/100,
                        colR: Math.round(col.right*100)/100,
                        colC: Math.round((col.left+col.right)/2*100)/100,
                        centers: rects.map(x => Math.round((x.left+x.right)/2*100)/100)};
            }""", t)
            if r['n'] > 1: n_wrapped += 1
            if r['collide']:
                bad.append(('collision', w, t[:28]))
            if r['right'] > r['colR'] + 0.5 or min(r['lefts']) < r['colL'] - 0.5:
                bad.append(('escapes column', w, t[:28], r['lefts'], r['right'], r['colR']))
            if w <= 544:
                # Phone layout: the line sits above the nav, centred.
                if not r['aboveNav']:
                    bad.append(('phone: video line not above nav', w, t[:28]))
                off = max(abs(c - r['colC']) for c in r['centers'])
                if off > 1.5:
                    bad.append(('phone: video line not centred', w, t[:28], off))
            elif r['ownRow'] and abs(min(r['lefts']) - r['colL']) > 0.5:
                bad.append(('own row not flush left', w, t[:28], min(r['lefts']), r['colL']))
        wraps[w] = n_wrapped
        print(f"[topbar]    {w}px -> {n_wrapped}/32 titles wrap internally | "
              f"{'OK' if not bad else 'FAIL'}")
        for e in bad[:3]: print("   ", e); fails.append(('topbar', e))
        pg.close()

    # --- 3b. Nav anchors all resolve, nav flush with the column -------
    pg = b.new_page(viewport={'width': 1440, 'height': 900})
    pg.goto(URI); pg.wait_for_timeout(150)
    nav = pg.evaluate("""() => {
        const col = document.querySelector('main').getBoundingClientRect();
        const links = [...document.querySelectorAll('.topnav a')];
        return {
          items: links.map(a => {
            const h = a.getAttribute('href');
            // Only in-page anchors can be resolved here. "Building" now points
            // at building.html; cross-page links are verified by verify_site.py.
            return {label: a.textContent.trim(), href: h,
                    target: h.startsWith('#') ? !!document.querySelector(h) : true};
          }),
          navLeft: Math.round(document.querySelector('.topnav').getBoundingClientRect().left*100)/100,
          colLeft: Math.round(col.left*100)/100,
        };
    }""")
    dead = [i for i in nav['items'] if not i['target']]
    print(f"[nav]       {len(nav['items'])} pillars: "
          + ' | '.join(f"{i['label']}{i['href']}" for i in nav['items']))
    print(f"[nav]       {len(dead)} anchors with no target | "
          f"nav left {nav['navLeft']} vs column {nav['colLeft']} "
          f"{'OK' if abs(nav['navLeft']-nav['colLeft']) < 0.5 else 'FAIL'}")
    for d in dead: fails.append(('dead anchor', d))
    if abs(nav['navLeft'] - nav['colLeft']) >= 0.5: fails.append(('nav edge', nav))
    pg.close()

    # --- 4. Randomness, 400 reloads ----------------------------------
    pg = b.new_page(viewport={'width': 1440, 'height': 900})
    seen = set()
    for _ in range(400):
        pg.goto(URI)
        seen.add(tuple(pg.evaluate("""() => {
            const a = document.getElementById('watching-link');
            return [a.textContent, a.getAttribute('href')];
        }""")))
    ok = len(seen) == 32
    print(f"[random]    400 reloads -> {len(seen)}/32 distinct title+url pairs {'OK' if ok else 'FAIL'}")
    if not ok: fails.append(('random', len(seen)))
    urls = {u for _, u in seen}
    bad_url = [u for u in urls if not re.fullmatch(r'https://youtu\.be/[A-Za-z0-9_-]{11}', u)]
    print(f"[urls]      {len(urls)} distinct urls, {len(bad_url)} malformed")
    for u in bad_url: fails.append(('url', u))
    pg.close()

    # --- 5. No-JS fallback -------------------------------------------
    ctx = b.new_context(java_script_enabled=False)
    pg = ctx.new_page(); pg.goto(URI)
    txt = pg.inner_text('#watching-link').strip()
    href = pg.get_attribute('#watching-link', 'href')
    ok = bool(txt) and bool(re.fullmatch(r'https://youtu\.be/[A-Za-z0-9_-]{11}', href or ''))
    print(f"[no-js]     text={txt[:40]!r} href={href} {'OK' if ok else 'FAIL'}")
    if not ok: fails.append(('nojs', (txt, href)))
    ctx.close()

    # --- 6. Closing line in a wide serif ------------------------------
    pg = b.new_page(viewport={'width': 1440, 'height': 900})
    pg.goto(URI); pg.wait_for_timeout(150)
    r = pg.evaluate("""() => {
        const c = document.querySelector('.closing');
        c.style.fontFamily = "'DejaVu Serif', serif";
        const a = c.firstElementChild;
        const range = document.createRange();
        range.setStart(c, 0);
        range.setEndBefore(c.querySelector('.note'));
        const w = range.getBoundingClientRect().width;
        const measure = c.getBoundingClientRect().width;
        const lines = [...range.getClientRects()].length;
        return {w: Math.round(w), measure: Math.round(measure), lines};
    }""")
    pct = round(100 * r['w'] / r['measure'])
    print(f"[closing]   wide serif: {r['w']}px of {r['measure']}px measure = {pct}% (§6 wants <=90%)")
    if pct > 90: fails.append(('closing', pct))
    pg.close()

    # --- 7. Screenshots ----------------------------------------------
    for w, h, name in ((1440, 1000, 'shot-1440.png'), (390, 844, 'shot-390.png')):
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2)
        pg.goto(URI); pg.wait_for_timeout(300)
        pg.screenshot(path=name, full_page=True)
        pg.close()
    print("[visual]    shot-1440.png, shot-390.png written")

    b.close()

print()
print("RESULT:", "ALL CHECKS PASSED" if not fails else f"{len(fails)} FAILURE(S)")
sys.exit(1 if fails else 0)
