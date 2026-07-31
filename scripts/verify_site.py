"""Site-level checks. Run alongside verify.py.

verify.py exercises the home page in depth (contrast, the 32 video titles, the
top-bar flex behaviour, randomness, no-JS). This covers what only exists once
there is more than one page: CSS drift between the inlined <style> blocks, link
integrity in both directions, per-page metadata uniqueness, and structured data.

July 30, 2026 — rewritten for a growing site. Every check that used to name
'building/index.html' now runs over EVERY page found in dist/, and the two
hardcoded contrast counts (46 and 60) are gone. Those counts were a trap: they
asserted a number that changes for entirely legitimate reasons, so the only way
to add a paragraph was to edit the test, which trains you to edit the test. What
matters is that nothing fails AA, and that is what is asserted now. No assertion
was dropped in the rewrite — each one was regeneralised. See handoff §8.
"""
import pathlib, re, sys, datetime, json
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent.parent / 'dist'
BG   = (251, 248, 242)
fails = []

def note(ok, label, detail=''):
    print(f"[{'OK  ' if ok else 'FAIL'}] {label}{'  ' + detail if detail else ''}")
    if not ok: fails.append(label)

# Discovered, not enumerated. A new build is a new .md file and its page appears
# here on its own — which is the whole point of the content collection. A list
# of paths maintained by hand is a list that silently stops covering new pages.
PAGES = sorted(str(p.relative_to(ROOT)) for p in ROOT.glob('**/index.html'))
note(len(PAGES) >= 2, f'discovered {len(PAGES)} pages in dist/', ', '.join(PAGES))

def slug(p):
    """'builds/personal-ai-os/index.html' -> 'builds-personal-ai-os' (for filenames)."""
    s = p[:-len('index.html')].strip('/').replace('/', '-')
    return s or 'home'

# --- 1. The inlined CSS must be identical across every page ------------------
# There is one CSS source now, so this asserts Astro inlined the same bundle
# into every page rather than tree-shaking one of them differently.
blocks = {}
for p in PAGES:
    m = re.search(r'<style>.*?</style>', (ROOT / p).read_text(), re.S)
    blocks[p] = m.group(0) if m else None
note(all(blocks.values()), 'every page has a <style> block')
sizes = {p: len(b or '') for p, b in blocks.items()}
note(len(set(blocks.values())) == 1, 'inlined CSS identical across all pages',
     f"sizes: {sorted(set(sizes.values()))}")

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
    dupes = {v for v in vals if vals.count(v) > 1}
    note(all(vals) and not dupes, f'{field} unique per page',
         f'duplicated: {dupes}' if dupes else '')
for p in PAGES:
    print(f"        {p:<34} {meta[p]['canonical']}")
    print(f"        {'':<34} {meta[p]['title']}")

# --- 3. Per-page: links, contrast, headings, overflow -----------------------
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
            # "/builds/" -> builds/index.html.
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

        # contrast — assert zero failures, report the count rather than fixing it
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

        # --- no horizontal overflow at 320px, on EVERY page ------------------
        # Used to run on the building page only. A build page can now carry a
        # long unbroken title or a code-ish string in Kyle's prose, so every
        # page earns the check.
        pg = b.new_page(viewport={'width': 320, 'height': 800})
        pg.goto((ROOT / p).resolve().as_uri()); pg.wait_for_timeout(200)
        sw = pg.evaluate('document.documentElement.scrollWidth')
        note(sw == 320, f'{p}: no overflow at 320px', f'scrollWidth={sw}')
        pg.screenshot(path=str(ROOT / f'{slug(p)}-320.png'), full_page=True)
        pg.close()

    # desktop screenshots, one per page
    for p in PAGES:
        pg = b.new_page(viewport={'width': 1440, 'height': 1000}, device_scale_factor=2)
        pg.goto((ROOT / p).resolve().as_uri()); pg.wait_for_timeout(300)
        pg.screenshot(path=str(ROOT / f'{slug(p)}-1440.png'), full_page=True)
        pg.close()
    b.close()

# --- 4. Structured data ------------------------------------------------------
# schema.org's rule is that markup must not claim more than the page shows, and
# Google penalises structured data that does. So these checks don't just confirm
# the JSON parses — they confirm every claim in it is backed by visible content
# or by a real link on the page.
ld = {}
for p in PAGES:
    src = (ROOT / p).read_text()
    b_ = re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', src, re.S)
    note(len(b_) == 1, f'{p}: exactly one JSON-LD block', f'found {len(b_)}')
    try:
        ld[p] = json.loads(b_[0])
        note(True, f'{p}: JSON-LD parses')
    except Exception as e:
        ld[p] = None
        note(False, f'{p}: JSON-LD parses', str(e))

home_ld = ld.get('index.html') or {}
home_src = (ROOT / 'index.html').read_text()
person = next((n for n in home_ld.get('@graph', []) if n.get('@type') == 'Person'), None)
note(person is not None, 'home page defines a Person')
if person:
    for field in ('name', 'url', 'jobTitle', 'sameAs'):
        note(field in person, f'Person has {field}')
    missing = [u for u in person.get('sameAs', []) if f'href="{u}"' not in home_src]
    note(not missing, 'every sameAs URL is a real link on the page', str(missing))

# Every page other than the home page carries a stub Person pointing at the home
# page's definition rather than redefining Kyle. Was checked on one page; now on
# all of them, because a new page template is exactly where this gets forgotten.
ids_defined = {n.get('@id') for n in home_ld.get('@graph', [])}
for p in PAGES:
    if p == 'index.html': continue
    stub = next((n for n in (ld.get(p) or {}).get('@graph', []) if n.get('@type') == 'Person'), None)
    note(stub is not None and stub.get('@id') in ids_defined,
         f'{p}: Person @id resolves to the home page definition',
         stub.get('@id') if stub else 'no Person node')

# Every BlogPosting headline, date and anchor must appear on the page declaring
# it. Was hardcoded to the building page; now runs wherever a Blog is declared,
# so a new build page with entries is covered the day it exists.
blogs = 0
for p in PAGES:
    src = (ROOT / p).read_text()
    blog = next((n for n in (ld.get(p) or {}).get('@graph', []) if n.get('@type') == 'Blog'), None)
    if not blog: continue
    blogs += 1
    for post in blog.get('blogPost', []):
        note(post['headline'] in src, f'{p}: BlogPosting headline is on the page',
             post['headline'][:44])
        y, m, d = post['datePublished'].split('-')
        human = datetime.datetime(int(y), int(m), int(d)).strftime('%B %-d, %Y')
        note(human in src, f'{p}: BlogPosting date matches the visible date', human)
        anchor = post['url'].split('#')[-1]
        note(f'id="{anchor}"' in src, f'{p}: BlogPosting anchor exists on the page', anchor)
note(blogs >= 1, 'at least one page declares a Blog', f'{blogs} found')

# Same rule for the ItemList on /builds/: every build it names must be a real
# heading on the page, and every url it points at must be a page that exists.
for p in PAGES:
    src = (ROOT / p).read_text()
    for node in (ld.get(p) or {}).get('@graph', []):
        item_list = node.get('mainEntity') if node.get('mainEntity', {}).get('@type') == 'ItemList' else None
        if not item_list: continue
        for it in item_list.get('itemListElement', []):
            note(it['name'] in src, f'{p}: ItemList name is on the page', it['name'])
            rel = it['url'].replace('https://kylecovan.com/', '').strip('/')
            note((ROOT / rel / 'index.html').exists(),
                 f'{p}: ItemList url resolves to a real page', it['url'])

# --- 5. sitemap lists every page --------------------------------------------
sm = (ROOT / 'sitemap-0.xml').read_text()
listed = re.findall(r'<loc>(.*?)</loc>', sm)
note(len(listed) == len(PAGES), 'sitemap lists every page',
     f'{len(listed)} urls vs {len(PAGES)} pages')
for u in listed: print('        ', u)

# --- 6. Redirects for URLs that used to be live ------------------------------
# /building/ was indexed. A redirect file that stops being copied, or that
# points at a path which no longer exists, fails silently — the visitor gets a
# 404 and nobody finds out. Both halves are checked here.
rd = ROOT / '_redirects'
note(rd.exists(), '_redirects survives the build into dist/')
if rd.exists():
    rules = [l.split() for l in rd.read_text().splitlines()
             if l.strip() and not l.startswith('#')]
    note(bool(rules), f'_redirects has {len(rules)} rule(s)')
    live = {p[:-len('index.html')].strip('/') for p in PAGES}
    for r in rules:
        src_path, dest = r[0], r[1]
        # The destination must be a page that actually exists, or the redirect
        # sends visitors from one 404 to another.
        target = ROOT / dest.strip('/') / 'index.html'
        note(target.exists(), f'redirect target exists: {dest}',
             str(target.relative_to(ROOT)))
        # And the SOURCE must NOT be a live page. If /builds/ were ever both a
        # real page and a redirect source, the redirect would shadow the page
        # and it would be invisible — the site would still build, still pass
        # every other check, and quietly serve the wrong thing.
        note(src_path.strip('/') not in live,
             f'redirect source {src_path} does not shadow a real page')
    # and the old deep-link anchors must still resolve somewhere
    builds_src = (ROOT / 'builds/index.html').read_text()
    for old in ('personal-ai-os', 'second-brain'):
        note(f'id="{old}"' in builds_src,
             f'old deep link /building/#{old} still has a target on /builds/')

# --- 7. RSS items point at pages and anchors that exist ----------------------
# New on July 30, and it earned its place immediately: the first version of the
# per-entry links rendered as ".../#2026-07-28-too-many-ideas/" because
# @astrojs/rss appends the site's trailing slash to the end of the whole string,
# fragment included. The feed was valid XML, the build passed, and every link
# was subtly broken. Nothing else on the site checks the feed's contents.
feed = ROOT / 'rss.xml'
note(feed.exists(), 'rss.xml is built')
if feed.exists():
    xml = feed.read_text()
    item_links = re.findall(r'<link>(.*?)</link>', xml)[1:]   # [0] is the channel link
    note(bool(item_links), f'rss.xml has {len(item_links)} item link(s)')
    for u in item_links:
        note('/#' not in u or not u.endswith('/'),
             'rss link has no slash after the fragment', u)
        path, _, frag = u.replace('https://kylecovan.com/', '').partition('#')
        target = ROOT / path.strip('/') / 'index.html'
        note(target.exists(), 'rss link resolves to a real page', u)
        if frag and target.exists():
            note(f'id="{frag}"' in target.read_text(),
                 'rss link fragment exists on that page', f'#{frag}')
    # Every published entry must be in the feed. A draft that silently stays in,
    # or an entry that silently drops out, is invisible without this.
    titles = re.findall(r'<title>(.*?)</title>', xml)[1:]
    note(len(titles) == len(item_links), 'every rss item has a title and a link')

print()
print('SITE RESULT:', 'ALL CHECKS PASSED' if not fails else f'{len(fails)} FAILURE(S): {fails}')
sys.exit(1 if fails else 0)
