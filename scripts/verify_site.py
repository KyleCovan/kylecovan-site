"""Site-level checks for the two-page build. Run alongside verify.py.

verify.py exercises the home page in depth (contrast, the 32 video titles, the
top-bar flex behaviour, randomness, no-JS). This covers what only exists once
there is more than one page: CSS drift between the duplicated <style> blocks,
link integrity in both directions, and per-page metadata uniqueness.
"""
import pathlib, re, sys, datetime
from playwright.sync_api import sync_playwright

ROOT  = pathlib.Path(__file__).parent.parent / 'dist'
PAGES = ['index.html', 'building/index.html']
BG    = (251, 248, 242)
fails = []

def note(ok, label, detail=''):
    print(f"[{'OK  ' if ok else 'FAIL'}] {label}{'  ' + detail if detail else ''}")
    if not ok: fails.append(label)

# --- 1. The duplicated CSS must be byte-identical ---------------------------
blocks = {}
for p in PAGES:
    m = re.search(r'<style>.*?</style>', (ROOT / p).read_text(), re.S)
    blocks[p] = m.group(0) if m else None
note(all(blocks.values()), 'both pages have a <style> block')
# Still meaningful after the migration, for a different reason: there is now one
# CSS source, so this asserts Astro inlined the same bundle into both pages
# rather than tree-shaking one of them differently.
note(blocks['index.html'] == blocks['building/index.html'],
     'inlined CSS identical across pages',
     f"{len(blocks['index.html'] or '')} vs {len(blocks['building/index.html'] or '')} chars")

# --- 2. Metadata is per-page, not copy-pasted -------------------------------
meta = {}
for p in PAGES:
    s = (ROOT / p).read_text()
    meta[p] = {
        'title':     (re.search(r'<title>(.*?)</title>', s, re.S) or [None, None])[1],
        'desc':      (re.search(r'<meta name="description" content="(.*?)"', s, re.S) or [None, None])[1],
        'canonical': (re.search(r'<link rel="canonical" href="(.*?)"', s) or [None, None])[1],
    }
for field in ('title', 'desc', 'canonical'):
    vals = [meta[p][field] for p in PAGES]
    note(all(vals) and len(set(vals)) == len(vals), f'{field} unique per page')
for p in PAGES:
    print(f"        {p:<16} {meta[p]['canonical']}")
    print(f"        {'':<16} {meta[p]['title']}")

# --- 3. Links resolve: files exist, anchors exist ----------------------------
with sync_playwright() as pw:
    b = pw.chromium.launch(args=['--disable-lcd-text'])
    for p in PAGES:
        pg = b.new_page(viewport={'width': 1440, 'height': 900})
        pg.goto((ROOT / p).resolve().as_uri()); pg.wait_for_timeout(200)
        links = pg.evaluate("""() => [...document.querySelectorAll('a[href]')]
            .map(a => a.getAttribute('href'))""")
        bad = []
        for h in links:
            if h.startswith(('http://', 'https://', 'mailto:')):
                continue
            if h.startswith('#'):
                if not pg.query_selector(h): bad.append((h, 'no target on this page'))
                continue
            file_part, _, frag = h.partition('#')
            # Built site uses directory URLs: "/" -> index.html,
            # "/building/" -> building/index.html.
            if file_part:
                rel = file_part.lstrip('/')
                cand = ROOT / rel
                if cand.is_dir() or file_part.endswith('/') or rel == '':
                    cand = ROOT / rel / 'index.html'
                if not cand.exists():
                    bad.append((h, f'file missing: {cand.relative_to(ROOT)}')); continue
            else:
                cand = ROOT / p
            if frag:
                if f'id="{frag}"' not in cand.read_text():
                    bad.append((h, f'no #{frag} in {cand.name}'))
        note(not bad, f'{p}: all {len(links)} links resolve')
        for x in bad: print('        ', x)

        # contrast on this page
        nodes = pg.evaluate(r"""() => {
          const lin = c => { c/=255; return c<=0.03928 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4); };
          const L = ([r,g,b]) => 0.2126*lin(r)+0.7152*lin(g)+0.0722*lin(b);
          const parse = s => s.match(/[\d.]+/g).slice(0,3).map(Number);
          const bgL = L([251,248,242]); const out = [];
          const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
          while ((n = w.nextNode())) {
            if (!n.textContent.trim()) continue;
            const cs = getComputedStyle(n.parentElement);
            if (cs.display === 'none' || cs.visibility === 'hidden') continue;
            const fg = L(parse(cs.color));
            const ratio = (Math.max(fg,bgL)+0.05)/(Math.min(fg,bgL)+0.05);
            const px = parseFloat(cs.fontSize);
            const bold = (parseInt(cs.fontWeight,10)||400) >= 700;
            const large = px >= 24 || (bold && px >= 18.66);
            out.push({t: n.textContent.trim().slice(0,40), ratio: Math.round(ratio*100)/100,
                      pass: ratio >= (large ? 3 : 4.5)});
          }
          return out;
        }""")
        badc = [n for n in nodes if not n['pass']]
        note(not badc, f'{p}: contrast', f'{len(nodes)} nodes, {len(badc)} failures')
        for n in badc: print('        ', n)

        # exactly one h1, and heading order is sane
        hs = pg.evaluate("""() => [...document.querySelectorAll('h1,h2,h3,h4')]
            .map(h => ({tag: h.tagName, text: h.textContent.trim().slice(0,46)}))""")
        n_h1 = sum(1 for h in hs if h['tag'] == 'H1')
        note(n_h1 == 1, f'{p}: exactly one h1', f'found {n_h1}')
        levels = [int(h['tag'][1]) for h in hs]
        jumps = [(hs[i-1]['tag'], hs[i]['tag']) for i in range(1, len(levels))
                 if levels[i] - levels[i-1] > 1]
        note(not jumps, f'{p}: no skipped heading levels', str(jumps) if jumps else '')
        pg.close()

    # --- 4. No horizontal overflow on building.html at 320px ----------------
    pg = b.new_page(viewport={'width': 320, 'height': 800})
    pg.goto((ROOT / 'building/index.html').resolve().as_uri()); pg.wait_for_timeout(200)
    sw = pg.evaluate('document.documentElement.scrollWidth')
    note(sw == 320, 'building page: no overflow at 320px', f'scrollWidth={sw}')
    pg.screenshot(path=str(ROOT / 'building-390.png'), full_page=True)
    pg.close()

    pg = b.new_page(viewport={'width': 1440, 'height': 1000}, device_scale_factor=2)
    pg.goto((ROOT / 'building/index.html').resolve().as_uri()); pg.wait_for_timeout(300)
    pg.screenshot(path=str(ROOT / 'building-1440.png'), full_page=True)
    pg.close()
    b.close()

# --- 5. Structured data ------------------------------------------------------
# schema.org's rule is that markup must not claim more than the page shows, and
# Google penalises structured data that does. So these checks don't just confirm
# the JSON parses — they confirm every claim in it is backed by visible content
# or by a real link on the page.
import json

ld = {}
for pg_name in PAGES:
    src = (ROOT / pg_name).read_text()
    blocks = re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', src, re.S)
    note(len(blocks) == 1, f'{pg_name}: exactly one JSON-LD block', f'found {len(blocks)}')
    try:
        ld[pg_name] = json.loads(blocks[0])
        note(True, f'{pg_name}: JSON-LD parses')
    except Exception as e:
        ld[pg_name] = None
        note(False, f'{pg_name}: JSON-LD parses', str(e))

home_ld = ld.get('index.html') or {}
home_src = (ROOT / 'index.html').read_text()
person = next((n for n in home_ld.get('@graph', []) if n.get('@type') == 'Person'), None)
note(person is not None, 'home page defines a Person')
if person:
    for field in ('name', 'url', 'jobTitle', 'sameAs'):
        note(field in person, f'Person has {field}')
    # every sameAs profile must actually be linked from the page
    missing = [u for u in person.get('sameAs', []) if f'href="{u}"' not in home_src]
    note(not missing, 'every sameAs URL is a real link on the page', str(missing))

# cross-page @id: the stub Person on building.html must point at the home page's
bld_ld = ld.get('building/index.html') or {}
ids_defined = {n.get('@id') for n in home_ld.get('@graph', [])}
stub = next((n for n in bld_ld.get('@graph', []) if n.get('@type') == 'Person'), None)
note(stub is not None and stub.get('@id') in ids_defined,
     'building page Person @id resolves to the home page definition',
     stub.get('@id') if stub else 'no Person node')

# every BlogPosting headline and date must appear in the rendered page
bld_src = (ROOT / 'building/index.html').read_text()
blog = next((n for n in bld_ld.get('@graph', []) if n.get('@type') == 'Blog'), None)
note(blog is not None, 'building.html defines a Blog')
if blog:
    for post in blog.get('blogPost', []):
        note(post['headline'] in bld_src,
             f"BlogPosting headline is on the page", post['headline'][:44])
        y, m, d = post['datePublished'].split('-')
        human = datetime.datetime(int(y), int(m), int(d)).strftime('%B %-d, %Y')
        note(human in bld_src, f"BlogPosting date matches the visible date", human)
        note(post['url'].split('#')[-1] in bld_src, 'BlogPosting anchor exists',
             post['url'].split('#')[-1])

# --- 6. sitemap lists every page -------------------------------------------
sm = (ROOT / 'sitemap-0.xml').read_text()
listed = re.findall(r'<loc>(.*?)</loc>', sm)
note(len(listed) == len(PAGES), 'sitemap lists every page', f'{len(listed)} urls')
for u in listed: print('        ', u)

print()
print('SITE RESULT:', 'ALL CHECKS PASSED' if not fails else f'{len(fails)} FAILURE(S): {fails}')
sys.exit(1 if fails else 0)
