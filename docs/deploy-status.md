# Deploy and DNS — where things stand

**As of August 9, 2026: Steps 1–5 are DONE. The DMARC record is the one thing
still open.** The August 6 audit branch (`audit-fixes-2026-08-06`) is merged to
`main` and live — real `/404.html`, `/privacy/`, content-signal `robots.txt`,
contact `mailto:` with Cloudflare `email_off`, and build `shareDescription`.

**kylecovan.com is live.** DNS is served by Cloudflare, the site is served by
Cloudflare Pages, and Google Workspace email survived the move intact.

| Thing | Where |
|---|---|
| Local project | `~/Projects/kylecovan-astro` |
| Repo | https://github.com/KyleCovan/kylecovan-site (public) |
| Host | Cloudflare Pages project `kylecovan-site` |
| Live URL | **https://kylecovan.com** |
| Also live | https://kylecovan-site.pages.dev (build/preview URL) |
| `www` | 301 redirects to the apex |
| DNS | Cloudflare — `heather.ns.cloudflare.com`, `oswald.ns.cloudflare.com` |
| Registrar | still GoDaddy (unchanged, and that's fine) |

Full record inventory: **`docs/dns-records.md`.**

---

## Step 1 — Run it locally ✅ DONE

```bash
npm install
npm run dev        # http://localhost:4321
npm run build      # writes dist/
npm run verify     # both suites — ALL CHECKS PASSED twice
```

### Four snags, all resolved — these recur on any new machine

1. **The tarball lived on an external drive.** Unpacked to `~/Projects` on the
   internal drive instead: external volumes are flaky with `npm` and Git and may
   not be mounted.

2. **"permission denied" was a false alarm** — the bare path was pasted as a
   command and zsh tried to execute the tarball. Diagnose this before sending
   anyone into System Settings → Privacy.

3. **npm blocked install scripts** for `esbuild`, `sharp`, `fsevents` (newer npm
   `allow-scripts` default). Approved with
   `npm approve-scripts --allow-scripts-pending`. `npm install` also reports 3
   vulnerabilities — **ignore them, never run `npm audit fix --force`.** They
   are build-time tooling; the deployed output is static HTML.

4. **`npm run verify` failed on `ModuleNotFoundError: No module named 'playwright'`.**
   Both suites need Playwright plus a real Chromium in the project venv.
   `package.json` now calls `./.venv/bin/python3` directly (so the documented
   `npm run verify` works without a prior `activate`), but the venv still has
   to exist and have Playwright installed:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install playwright
   playwright install chromium      # ~150 MB
   ```

   `npm run dev` and `npm run build` don't need the venv. `.venv/` and
   `shot-*.png` are in `.gitignore`.

---

## Step 2 — GitHub ✅ DONE

Repo: **https://github.com/KyleCovan/kylecovan-site**, public, branch `main`.

**Auth:** no Homebrew and no `gh` on this Mac, so the route was a classic
Personal Access Token (`repo` scope) pasted at the `Password:` prompt, with
`git config --global credential.helper osxkeychain` so it is stored once.

**Two traps worth writing down:**

- The token is **not** a command. It is only ever typed in response to a
  `Password:` prompt that `git push` produces. Pasting it on its own line runs
  it as a program, and it then sits in `~/.zsh_history` in plain text. That
  happened once on July 29; that token was revoked and replaced.
- `git init` acts on whatever directory you are standing in. It was once run in
  `~`, creating a repo that claimed the entire home folder. Fix was
  `rm -rf /Users/kylecovan/.git`. **Check the prompt ends in `kylecovan-astro %`
  before any git command.**

**Commit identity:** `122067564+KyleCovan@users.noreply.github.com` — GitHub's
masked address, so Kyle's real email never appears in the public repo.

---

## Step 3 — Cloudflare Pages ✅ DONE

Project `kylecovan-site`, connected to the GitHub repo, GitHub App scoped to
**only that repository**.

| Setting | Value |
|---|---|
| Production branch | `main` |
| Framework preset | Astro |
| Build command | `npm run build` |
| Build output directory | `dist` |

**Cloudflare runs `npm run build` only, never `npm run verify`** — the
Python/Playwright setup is local-only and does not need to exist on the build
server.

**Two dashboard traps.** Cloudflare's current UI opens on a Workers-flavoured
"Ship something new" screen. **"Upload your static files" is the wrong branch** —
it deploys once and never updates. The Pages/Git flow is behind the small
*"Looking to deploy Pages? Get started"* link at the bottom. Also, backing out of
the upload flow can leave an empty project holding the name, which then collides
("A project with this name already exists"); delete the stray project rather
than renaming around it.

---

## Step 4 — Point kylecovan.com at it ✅ DONE — July 29, 2026

Done in five moves, in this order, deliberately. **The order is the method:**
every email record was replicated and verified inside Cloudflare *before* the
nameservers moved, so there was never a moment when the two DNS providers
disagreed about where mail should go.

### 1. Deleted the malformed SPF record at GoDaddy, first

```
"v=spf1 include:_spf.google.com ~all"      ← kept
"v=spf1include:_spf.google.com"            ← deleted
```

Missing space after `v=spf1`, no qualifier, and two SPF records at all is a
`permerror` at the receiving server, which pushes mail toward spam. Deleting it
**before** Cloudflare scanned the zone meant it was never imported. Fixing it at
the source is always cheaper than fixing a copy.

### 2. Added the domain to Cloudflare and checked what it imported

Current UI path: **Domains → Overview → Connect a domain.**
(Not "Add a site", not "+ Add", not "Onboard a domain". Not *Transfer* or *Buy*
— those move the registration, which we did not want.)

Cloudflare scanned GoDaddy and reported **2 A, 2 CNAME, 5 MX, 3 TXT**. Those
counts were checked against the verified inventory rather than trusted:

- 3 TXT is correct **because** the malformed SPF was already gone. 4 would have
  meant it came across; 2 would have meant DKIM was dropped.
- The DKIM value was compared character by character against the source and
  hashed — identical, 408 characters, and it base64-decodes to a valid 2048-bit
  RSA public key.

Deleted at this point: both GoDaddy parking A records (`3.33.130.190`,
`15.197.148.33`) and the `_domainconnect` CNAME. Left `www` alone.

### 3. Switched nameservers at GoDaddy

To `heather.ns.cloudflare.com` / `oswald.ns.cloudflare.com`. Confirmed by asking
a `.com` TLD server what the registry delegation says, which is the only answer
that actually settles it.

**The old GoDaddy zone was deliberately left in place, not deleted.** While it
exists, switching the nameservers back is a complete instant rollback.

### 4. Attached the domain to Pages

**Workers & Pages → kylecovan-site → Custom domains → Set up a custom domain.**
Cloudflare creates the DNS record itself — don't hand-write one.

### 5. Redirected `www` to the apex

Immediately after step 4, `www.kylecovan.com` served a **Cloudflare error page**:
the hostname was proxied but Pages had no route for it. Caught by loading it in
a real browser, not by assuming.

Fixed with **Rules → Overview → Create rule → Redirect Rule**, using the
*"Redirect from WWW to root"* template:

- Match: **Wildcard pattern**, Request URL `https://www.kylecovan.com/*`
- Target: `https://kylecovan.com/${1}`
- **301**, preserve query string

`${1}` carries the path, so `www.kylecovan.com/building/` lands on
`kylecovan.com/building/` rather than dumping everyone on the homepage. The rule
only fires on proxied traffic, so **the `www` CNAME must stay orange-clouded.**

Redirect chosen over adding `www` as a second Pages custom domain: the site's
canonical tags and JSON-LD `@id` both say `kylecovan.com`, and serving identical
content on two hostnames splits ranking signals.

### Verified after the cutover

*Historical record of the July 29 cutover — left as it was written. Note that
`/building/` was retired on July 30 and now 301s to `/builds/` via
`public/_redirects`; the `www` rule below still preserves the path, so
`www.kylecovan.com/building/` chains correctly through to `/builds/`.*

- `https://kylecovan.com/` → **Kyle Covan — AI Builder**, HTTPS, no cert warning
- `https://kylecovan.com/building/` → **Building in public — Kyle Covan**
- Page content spot-checked against the copy rules: creed reads **"put"**,
  four nav pillars present, Tapo Canyon is **plain text not a link**,
  canonical `https://kylecovan.com/`
- `www.kylecovan.com/?t=2` → `kylecovan.com/?t=2` (query preserved)
- `www.kylecovan.com/building/` → `kylecovan.com/building/` (path preserved)
- MX 5/5, one correct SPF, Workspace verification TXT, DKIM byte-identical
- **Real mail delivered to `kyle@kylecovan.com` after the switch** — including
  Cloudflare's own zone-activation notice at 03:47 UTC, which by definition was
  sent after the nameservers moved and arrived through the new MX path. That is
  the end-to-end proof; the DNS queries only prove the records exist.

⚠️ **Before trusting any DNS measurement, read the "How to verify DNS honestly"
section in `docs/dns-records.md`.** A false alarm during this migration cost real
time, and the cause was the measuring instrument, not the zone.

---

## Step 5 — Turn on the feedback loop — DONE August 3, 2026

- **Cloudflare Analytics** — already on, dashboard → the Pages project.
  Server-side, so nothing on the page and no break to zero-external-requests.
- ~~**Google Search Console**~~ — **done.** `kylecovan.com` is verified as a
  **Domain** property and `https://kylecovan.com/sitemap-index.xml` is
  submitted.

  **Submit the full URL, not a path.** A Domain property's "Add a new sitemap"
  field has no greyed-out prefix, so `sitemap-index.xml` on its own is rejected
  with *"Invalid sitemap address."* That check runs in the browser before
  Google fetches anything — it is never evidence that the sitemap is broken.

   **And it is `sitemap-index.xml`, never `sitemap.xml`.** Astro's integration
  emits the former. Unknown paths used to answer **HTTP 200** with the home page
  (Pages' no-`404.html` fallback); as of the August 6 audit merge they return a
  real **404**. Still verify by content-type when checking a URL that should be
  XML — status alone is not enough.

  Before submitting, all seven URLs in the sitemap were confirmed to return 200,
  and the deployed XML was confirmed byte-identical to the local `dist/` build.

**Worth doing at the same time, while the DNS knowledge is fresh:**

- **Add a DMARC record.** There is currently none. With SPF and DKIM both in
  place and correct, DMARC is the piece that tells receiving servers what to do
  when they fail. A safe starting policy is monitor-only:
  `_dmarc` TXT → `v=DMARC1; p=none; rua=mailto:kyle@kylecovan.com`.
  Start at `p=none`, read the reports, tighten later. Do **not** start at
  `p=reject`.

---

## Publishing, from here on

```bash
# create src/content/log/2026-08-15-what-broke.md with frontmatter + Kyle's words
source .venv/bin/activate      # only needed for verify
npm run build && npm run verify
git add -A && git commit -m "log: what broke" && git push
```

Cloudflare rebuilds and deploys on push. The entry appears on its build's page at
`/builds/<build>/`, in the structured data, in the sitemap and in the RSS feed.
Nothing else to touch. (The frontmatter field is `build:`, not `project:`, and
`/building/` became `/builds/` on July 30 — see handoff §4.)

---

## Still open

1. **DMARC record** (see Step 5). Search Console is done; this is the leftover.
2. **Dark mode.** Decision recorded in `docs/handoff.md` §7: automatic via
   `prefers-color-scheme`, no toggle. Deferred; it is a real design pass.
3. **Restore the Tapo Canyon link** the day tapocanyon.com resolves. The anchor
   was removed July 29 because it was a dead end; Kyle's sentence is untouched
   and a comment in `src/pages/index.astro` says to put it back.
4. **"What broke" entry for Project 01**, and Project 02's first entry.
5. **Branch `content/audit-triage-post`** — still unmerged. Queues the drafted
   “half a website audit was wrong” post plus `content-queue/` platform drafts.
6. **The old GoDaddy zone** can be left alone indefinitely — there is no cost to
   leaving it, and it is the rollback. Don't delete it just to tidy up.

*(Item about `headshot.jpg` missing from the repo is closed — source photos and
`build_assets.py` shipped with handoff §53.)*
