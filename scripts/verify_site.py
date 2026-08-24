"""Site-level checks. Run alongside verify.py.

verify.py exercises the home page in depth (contrast, the video titles, the
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

        # A heading that follows body text must be visibly separated from it.
        # Added August 4 after the rule that provides that space was broken
        # TWICE in one session, both times by a stray `*/` that left comment
        # prose sitting in the stylesheet as live CSS. The browser's error
        # recovery swallowed the rule and resumed at the next one, so the page
        # still rendered, every other suite still passed, and the only symptom
        # was headings sitting flat on the paragraph above them. It shipped
        # once before anyone noticed.
        #
        # Measured, not grepped: asserting the selector exists in the CSS would
        # have passed on both broken builds. What matters is the rendered gap.
        # .eyebrow and .entry-date are excluded because they are LABELS for the
        # heading beneath them and are supposed to be tight; see the note on
        # the rule in site.css.
        flush = pg.evaluate("""() => [...document.querySelectorAll('main h2, main h3')]
            .map(h => {
                const prev = h.previousElementSibling;
                if (!prev) return null;
                if (prev.classList.contains('eyebrow') ||
                    prev.classList.contains('entry-date') ||
                    prev.classList.contains('entry-kind')) return null;
                const gap = h.getBoundingClientRect().top - prev.getBoundingClientRect().bottom;
                return gap < 20 ? [h.textContent.trim().slice(0, 34), Math.round(gap)] : null;
            }).filter(Boolean)""")
        note(not flush, f'{p}: headings have space above them',
             str(flush) if flush else '')

        # Every aria-labelledby target must exist. Added August 4 with the new
        # builds heading, which is the first place on this site where the
        # eyebrow and the h2 are ONE SENTENCE: "Building in public." /
        # "Because explaining it shows me what I understand." The section names
        # both ids so a screen reader announces the whole thought instead of a
        # heading that starts mid-sentence.
        #
        # The failure this catches is silent. Rename or drop an id and the page
        # still renders perfectly; only the accessible name breaks, and no
        # other assertion here looks at it.
        aria = pg.evaluate(r"""() => [...document.querySelectorAll('[aria-labelledby]')]
            .map(el => {
                const ids = el.getAttribute('aria-labelledby').split(/\s+/).filter(Boolean);
                return {
                    el: el.tagName.toLowerCase() + (el.id ? '#' + el.id : ''),
                    missing: ids.filter(id => !document.getElementById(id)),
                    name: ids.map(id => (document.getElementById(id) || {}).textContent || '')
                             .join(' ').replace(/\s+/g, ' ').trim(),
                };
            })""")
        broken = [a for a in aria if a['missing']]
        note(not broken, f'{p}: aria-labelledby targets all exist',
             f'{len(aria)} labelled region(s)')
        for a in broken: print('        ', a['el'], 'missing:', a['missing'])

        # And specifically: the home page must not carry a builds summary.
        # August 24, 2026: Kyle asked for Story → Unless the Lord → Contact.
        # The August 21 one-door merge left a #building block behind; this
        # asserts structure, not words, so copy can change without touching
        # the test.
        if p == 'index.html':
            hp = pg.evaluate("""() => {
                const story = document.getElementById('story');
                const writing = document.getElementById('writing');
                const building = document.getElementById('building');
                return {
                    has_story: !!story,
                    has_writing: !!writing,
                    no_building: !building,
                    story_before_writing: !!(story && writing &&
                        story.compareDocumentPosition(writing) & Node.DOCUMENT_POSITION_FOLLOWING),
                    no_building_in_public: !document.body.textContent.includes('Building in public'),
                };
            }""")
            note(bool(hp) and hp['has_story'] and hp['has_writing'] and hp['no_building']
                 and hp['story_before_writing'] and hp['no_building_in_public'],
                 'home page is Story → Unless the Lord, no builds summary',
                 'ok' if hp and hp['no_building'] else 'still has #building')

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

# Every BlogPosting headline and date must appear on the page declaring it.
# August 21: a log is a full post at /writing/<id>/, not a fragment on a
# product page. The old check required a Blog wrapper on /builds/<id>/.
# That lock is reversed — the assertion now follows the house.
postings = 0
for p in PAGES:
    src = (ROOT / p).read_text()
    for node in (ld.get(p) or {}).get('@graph', []):
        if node.get('@type') != 'BlogPosting':
            continue
        postings += 1
        note(node['headline'] in src, f'{p}: BlogPosting headline is on the page',
             node['headline'][:44])
        y, m, d = node['datePublished'].split('-')
        human = datetime.datetime(int(y), int(m), int(d)).strftime('%B %-d, %Y')
        note(human in src, f'{p}: BlogPosting date matches the visible date', human)
        note(node['url'].startswith('https://kylecovan.com/writing/'),
             f'{p}: BlogPosting url is in the house', node['url'])
note(postings >= 1, 'published writing declares BlogPosting on its own page',
     f'{postings} found')

# Same rule for the ItemList on /writing/: every post it names must be a real
# heading on the page, and every url it points at must be a page that exists.
for p in PAGES:
    src = (ROOT / p).read_text()
    for node in (ld.get(p) or {}).get('@graph', []):
        item_list = node.get('mainEntity') if node.get('mainEntity', {}).get('@type') == 'ItemList' else None
        if not item_list: continue
        for it in item_list.get('itemListElement', []):
            note(it['name'] in src, f'{p}: ItemList name is on the page', it['name'])
            # An ItemList url may carry a fragment. Resolve the page, then
            # confirm the fragment actually exists there rather than stopping
            # at the page — a link to a real page and a dead anchor still
            # lands the reader in the wrong place.
            path, _, frag = it['url'].replace('https://kylecovan.com/', '').partition('#')
            target = ROOT / path.strip('/') / 'index.html'
            note(target.exists(), f'{p}: ItemList url resolves to a real page', it['url'])
            if frag and target.exists():
                note(f'id="{frag}"' in target.read_text(),
                     f'{p}: ItemList url fragment exists on that page', f'#{frag}')

# --- 5. sitemap: every page listed, every URL honestly dated -----------------
# <lastmod> is the only element in this file Google documents itself as using,
# and it is only worth anything if it is true. The checks below assert it is
# DERIVED — each date has to match the content file it claims to describe. A
# sitemap that stamps deploy time on all seven URLs would pass "every URL has a
# lastmod" and still be worthless, so that is deliberately not the only check.
sm = (ROOT / 'sitemap-0.xml').read_text()
listed = re.findall(r'<loc>(.*?)</loc>', sm)
note(len(listed) == len(PAGES), 'sitemap lists every page',
     f'{len(listed)} urls vs {len(PAGES)} pages')

entries = {}
for block in re.findall(r'<url>(.*?)</url>', sm, re.S):
    loc = re.search(r'<loc>(.*?)</loc>', block).group(1)
    lm  = re.search(r'<lastmod>(\d{4}-\d{2}-\d{2})', block)
    entries[loc] = lm.group(1) if lm else None
    print('        ', loc, entries[loc] or '— NO LASTMOD')

note(all(entries.values()), 'every sitemap URL carries a <lastmod>',
     f"{sum(1 for v in entries.values() if v)}/{len(entries)}")

today  = datetime.date.today().isoformat()
future = [u for u, d in entries.items() if d and d > today]
note(not future, 'no <lastmod> is in the future', ', '.join(future) or f'today is {today}')

# Removed on purpose, not forgotten: Google's sitemap documentation states it
# ignores both. A knob that looks like it steers ranking but doesn't is worse
# than no knob, because it invites tuning. This assertion is that decision's
# record — if either element ever comes back, it should be a deliberate act.
note('<priority>' not in sm and '<changefreq>' not in sm,
     'no <priority>/<changefreq> — Google ignores them, so they are not emitted')

# --- 5b. every date traces to the file it describes --------------------------
SRC = pathlib.Path(__file__).parent.parent / 'src' / 'content'

def frontmatter(path):
    m = re.match(r'---\r?\n(.*?)\r?\n---', path.read_text(), re.S)
    return m.group(1) if m else ''

def fm_field(block, key):
    """Top-level scalar only — mirrors the reader in astro.config.mjs."""
    m = re.search(rf'^{key}:[ \t]*[\'"]?([^\'"\n#]+)', block, re.M)
    return m.group(1).strip() if m else None

posts = []
for f in sorted((SRC / 'writing').glob('*.md')):
    b = frontmatter(f)
    posts.append({'id': f.stem, 'date': (fm_field(b, 'date') or '')[:10],
                  'kind': fm_field(b, 'kind') or 'essay',
                  'draft': fm_field(b, 'draft') == 'true',
                  'title': fm_field(b, 'title')})
published = [p for p in posts if p['date'] and not p['draft']]
drafts = [p for p in posts if p['draft']]

# Every published post owns /writing/<id>/, essay or log. lastmod is its date.
for p in published:
    url = f"https://kylecovan.com/writing/{p['id']}/"
    if url not in entries: continue
    note(entries[url] == p['date'], f"/writing/{p['id']}/ lastmod is the authored date",
         f"sitemap {entries[url]} vs frontmatter {p['date']}")

# /builds/ is a redirect, not a page. A sitemap that still lists it would
# tell Google the old door is the document.
for loc in entries:
    note('/builds/' not in loc, 'sitemap does not list /builds/ as a page', loc)

# --- 5c. the share card the meta tags promise actually ships -----------------
# New August 3. The card's filename is versioned on purpose: iMessage, Slack, X
# and LinkedIn cache share images keyed on the image URL, in caches this site
# cannot reach, so shipping a new photo at the old URL leaves everyone texting
# the link looking at the old card. Renaming guarantees a miss.
#
# The cost of that scheme is a rename with a missed reference, which 404s inside
# someone else's text message where nobody would ever see it. Hence this check:
# whatever og:image claims, that file must exist in dist/.
og_refs = set()
for p in PAGES:
    og_refs.update(re.findall(r'<meta property="og:image" content="([^"]+)"', (ROOT / p).read_text()))
    og_refs.update(re.findall(r'<meta name="twitter:image" content="([^"]+)"', (ROOT / p).read_text()))
note(bool(og_refs), 'pages declare a share image', f'{len(og_refs)} distinct url(s)')
for u in sorted(og_refs):
    f = ROOT / u.replace('https://kylecovan.com/', '')
    note(f.exists(), 'share image resolves to a file that ships', u)

# --- 6. Redirects for URLs that used to be live ------------------------------
# /building/ was indexed. /builds/ and /builds/<id>/ were the next door.
# August 21: those URLs lead into the house. A redirect file that stops
# being copied, or that points at a path which no longer exists, fails
# silently — the visitor gets a 404 and nobody finds out.
rd = ROOT / '_redirects'
note(rd.exists(), '_redirects survives the build into dist/')
if rd.exists():
    rules = [l.split() for l in rd.read_text().splitlines()
             if l.strip() and not l.startswith('#')]
    note(bool(rules), f'_redirects has {len(rules)} rule(s)')
    live = {p[:-len('index.html')].strip('/') for p in PAGES}
    note('builds' not in live and not any(p.startswith('builds/') for p in live),
         '/builds/ is not a live page')
    for r in rules:
        src_path, dest = r[0], r[1]
        # Destinations are usually pages (directory + index.html);
        # /sitemap.xml → /sitemap-index.xml is a file target, so check both.
        dest_path = dest.split('#', 1)[0]
        dest_clean = dest_path.strip('/')
        page_target = ROOT / dest_clean / 'index.html'
        file_target = ROOT / dest_clean
        note(page_target.exists() or file_target.is_file(),
             f'redirect target exists: {dest}', dest_clean)
        note(src_path.strip('/') not in live,
             f'redirect source {src_path} does not shadow a real page')
        if src_path.rstrip('/').startswith('/building') or src_path.rstrip('/').startswith('/builds'):
            note(dest_path.rstrip('/') == '/writing',
                 f'{src_path} leads into the house', dest)
    note(any(r[0] == '/sitemap.xml' and r[1] == '/sitemap-index.xml' for r in rules),
         '_redirects maps /sitemap.xml → /sitemap-index.xml')
    writing_src = (ROOT / 'writing/index.html').read_text()
    build_ids = [f.stem for f in (SRC / 'builds').glob('*.md')]
    for bid in build_ids:
        note(f'id="{bid}"' in writing_src, f'/writing/ has an anchor for {bid}')
    # `/building/#personal-ai-os` was published. The server never sees the
    # fragment, so the id has to live on the page the 301 lands on.
    # `/building/#second-brain` does NOT: that build was renamed to llm-wiki
    # on July 30, before /builds/second-brain/ was ever deployed. Recorded
    # rather than silently dropped.
    note('id="personal-ai-os"' in writing_src,
         'old deep link /building/#personal-ai-os still has a target')

# --- 7. RSS items point at pages that exist ----------------------------------
# New on July 30, and it earned its place immediately: the first version of the
# per-entry links rendered as ".../#2026-07-28-too-many-ideas/" because
# @astrojs/rss appends the site's trailing slash to the end of the whole string,
# fragment included. The feed was valid XML, the build passed, and every link
# was subtly broken. Nothing else on the site checks the feed's contents.
#
# August 21: every item links to /writing/<id>/. The channel title names the
# house, not the old "Building in public" door.
feed = ROOT / 'rss.xml'
note(feed.exists(), 'rss.xml is built')
if feed.exists():
    xml = feed.read_text()
    channel_title = re.search(r'<channel>\s*<title>(.*?)</title>', xml, re.S)
    note(channel_title is not None and 'Unless the Lord' in channel_title.group(1),
         'rss channel title names the house',
         channel_title.group(1) if channel_title else 'missing')
    note('Building in public' not in (channel_title.group(1) if channel_title else ''),
         'rss channel title is not "Building in public"')
    item_links = re.findall(r'<link>(.*?)</link>', xml)[1:]   # [0] is the channel link
    note(bool(item_links), f'rss.xml has {len(item_links)} item link(s)')
    for u in item_links:
        note('/#' not in u or not u.endswith('/'),
             'rss link has no slash after the fragment', u)
        note('/writing/' in u and '/builds/' not in u,
             'rss item link is in the house', u)
        path, _, frag = u.replace('https://kylecovan.com/', '').partition('#')
        target = ROOT / path.strip('/') / 'index.html'
        note(target.exists(), 'rss link resolves to a real page', u)
        if frag and target.exists():
            note(f'id="{frag}"' in target.read_text(),
                 'rss link fragment exists on that page', f'#{frag}')
    titles = re.findall(r'<title>(.*?)</title>', xml)[1:]
    note(len(titles) == len(item_links), 'every rss item has a title and a link')
    note(len(titles) == len(published),
         'every published post is in the feed',
         f'{len(titles)} items vs {len(published)} published')
    for d in drafts:
        note(d['title'] not in titles and d['id'] not in xml,
             f'draft stays out of the feed: {d["id"]}')

# --- 8. One house: nav, writing stream, drafts -------------------------------
home_src = (ROOT / 'index.html').read_text()
writing_src = (ROOT / 'writing/index.html').read_text()
nav_labels = re.findall(
    r'<nav class="topnav"[^>]*>.*?</nav>', home_src, re.S)
nav_html = nav_labels[0] if nav_labels else ''
note('Builds' not in nav_html, 'nav has no Builds item')
note('Unless the L' in nav_html or 'Unless the Lord' in nav_html,
     'nav still has Unless the Lord')
note(nav_html.count('href="/writing/"') == 1 and 'href="/builds/"' not in nav_html,
     'nav writing door is /writing/ only')

# Published posts appear on /writing/; drafts do not.
for p in published:
    note(p['title'] in writing_src, f'/writing/ lists published post: {p["id"]}')
    note((ROOT / 'writing' / p['id'] / 'index.html').exists(),
         f'/writing/{p["id"]}/ is a real page')
for d in drafts:
    note(d['title'] not in writing_src,
         f'draft stays off /writing/: {d["id"]}')
    note(not (ROOT / 'writing' / d['id'] / 'index.html').exists(),
         f'draft has no public URL: {d["id"]}')

# Logs are marked; essays are not buried under the same mark.
logs = [p for p in published if p['kind'] == 'log']
essays = [p for p in published if p['kind'] != 'log']
if logs:
    note('entry-kind' in writing_src and '>Log<' in writing_src,
         'logs are marked on /writing/')
if essays:
    note(any(e['title'] in writing_src for e in essays),
         'essays appear on /writing/')

print()
print('SITE RESULT:', 'ALL CHECKS PASSED' if not fails else f'{len(fails)} FAILURE(S): {fails}')
sys.exit(1 if fails else 0)
