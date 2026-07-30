# kylecovan.com — verified DNS record inventory

**Captured July 29, 2026,** and updated the same day after the migration
completed. **This table is the authoritative record inventory** — the shorter one
in `docs/deploy-status.md` Step 4 is a narrative, not a list.

⚠️ **Kyle's email runs on Google Workspace through these records. Read this
whole file before touching DNS.**

---

## Current state — DNS is on Cloudflare

| | |
|---|---|
| Nameservers | `heather.ns.cloudflare.com`, `oswald.ns.cloudflare.com` |
| Registrar | GoDaddy (unchanged — only DNS moved) |
| Old GoDaddy zone | **left in place deliberately** as a one-move rollback |
| Apex | Cloudflare Pages custom domain → `kylecovan-site` |
| `www` | 301 redirect rule → apex, path and query preserved |

---

## The pre-migration zone, as captured from GoDaddy

Queried from the authoritative nameservers (`97.74.102.3`, `173.201.70.3`);
both agreed on every answer. **But see the ⚠️ caveat on measurement below —
these queries went through an intercepting cache, and the dashboard was the
thing that actually settled disputes.**

| Name | Type | Value | Migrated? |
|---|---|---|---|
| `kylecovan.com` | A | `3.33.130.190` | No — GoDaddy parking, deleted |
| `kylecovan.com` | A | `15.197.148.33` | No — GoDaddy parking, deleted |
| `kylecovan.com` | MX | `1 aspmx.l.google.com.` | **Yes** |
| `kylecovan.com` | MX | `5 alt1.aspmx.l.google.com.` | **Yes** |
| `kylecovan.com` | MX | `5 alt2.aspmx.l.google.com.` | **Yes** |
| `kylecovan.com` | MX | `10 alt3.aspmx.l.google.com.` | **Yes** |
| `kylecovan.com` | MX | `10 alt4.aspmx.l.google.com.` | **Yes** |
| `kylecovan.com` | TXT | `v=spf1 include:_spf.google.com ~all` | **Yes** |
| `kylecovan.com` | TXT | `v=spf1include:_spf.google.com` | No — malformed, deleted |
| `kylecovan.com` | TXT | `google-site-verification=KOFbPwCsibpufcBcVaDZ7T93F3e4eFKZe4UzSbrO80Q` | **Yes** |
| `google._domainkey` | TXT | DKIM public key — below | **Yes ⚠️** |
| `www` | CNAME | `kylecovan.com.` | Kept, now redirected |
| `_domainconnect` | CNAME | `_domainconnect.gd.domaincontrol.com.` | No — GoDaddy plumbing |
| `_dmarc` | TXT | *(none — no DMARC policy exists)* | Still missing |
| `kylecovan.com` | CAA | *(none)* | Fine |

Confirmed absent: `mail`, `smtp`, `webmail`, `autodiscover`, `ftp`, `email`,
`calendar`, `drive`, `docs`, `sites`, `groups`, `blog`, `shop`, `m`, `start`,
`_acme-challenge`, and the `k1` / `default` / `selector1` DKIM selectors.

---

## ⚠️ The DKIM record the old table missed

`google._domainkey.kylecovan.com` TXT — Google Workspace's DKIM signing key.
Stored as two quoted strings because a TXT string caps at 255 characters;
**they concatenate into one value.** Cloudflare accepts it as a single unbroken
string and re-splits it itself.

```
v=DKIM1;k=rsa;p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhg1bLo/iQ7PkmE2OyuDJnqW6BJurIf+VsMV8UYnOXebZdqPfdFfKO7YX+FFEpPJIJhFnkNdknV5KB8K2tmq83ffOuzfmpj4Qri3ArozNWQFQC8oSgoo6Sss8uWXn15rcMUpOnAdpLHO/YKxjBJx4/CJv1lNl3o/kXVuZFzG6/GOHjKdYEQd1kMysr+p50OuhqfaLBkymfrQ7CJtMgC9Vw+6V00dxjE0MqjOMddGOFKfow+BGSeZVBzj8nQdH95RDmMZMxZDk0YeLUkoLG9eZPtYr9jhCxx63Px3eyFmb+oCmYHWorP5Nse3ZAwmvZHLUFDDrkqQ3tVVRUa3vJqmr9wIDAQAB
```

408 characters. Base64-decodes to a valid **2048-bit RSA public key** — that
check is worth re-running after any move, because a truncated key still *looks*
like a key.

**Why losing it would have been worse than losing MX.** A missing MX bounces
mail loudly. A missing DKIM breaks nothing visibly: mail still sends, still
arrives, and just authenticates one factor weaker, so more of it lands in spam
over the following weeks with no error anywhere.

**Verified after the migration: byte-identical, same SHA-256.**

---

## Cloudflare rewrote `robots.txt` — discovered July 29, TURNED OFF July 30

**Update, July 30, 2026: Kyle disabled this deliberately.** Managed robots.txt
was toggled off in AI Crawl Control; "Block AI bots Scope" set to "Do not
block"; per-crawler blocking confirmed off (AI Crawl Control showed 14/14
requests allowed, 0 blocked); the September 15 mixed-purpose-crawler preference
was already "continue to be allowed." **Training crawlers are now allowed by
choice** — the goal is to be known by models as well as cited by them, and the
site's premise is building in public. Retrieval agents were never blocked.
Bot fight mode and AI Labyrinth were confirmed off and should stay off: both
modify what Cloudflare serves (an injected script; AI-generated decoy links),
which the verify suites cannot catch because they test `dist/`.

The section below is kept as the historical record of what the injection was
and what it did and didn't cost.

---

**This was caused by putting the domain behind Cloudflare, and it was
not in the repo.** Found by comparing the two hostnames:

`https://kylecovan-site.pages.dev/robots.txt` — the repo's actual file:

```
User-agent: *
Allow: /

Sitemap: https://kylecovan.com/sitemap-index.xml
```

`https://kylecovan.com/robots.txt` — the same file with a **Cloudflare Managed
content** block injected above it:

```
User-agent: *
Content-Signal: search=yes,ai-train=no,use=reference
Allow: /

User-agent: Amazonbot                       Disallow: /
User-agent: Applebot-Extended               Disallow: /
User-agent: Bytespider                      Disallow: /
User-agent: CCBot                           Disallow: /
User-agent: ClaudeBot                       Disallow: /
User-agent: CloudflareBrowserRenderingCrawler   Disallow: /
User-agent: Google-Extended                 Disallow: /
User-agent: GPTBot                          Disallow: /
User-agent: meta-externalagent              Disallow: /
```

(plus a long comment header declaring the Content Signals policy as a
reservation of rights under Article 4 of EU Directive 2019/790.)

### What it does and does not cost, precisely

**Classic SEO: unaffected.** Googlebot and Bingbot are not in the block list.
Google's own documentation states Google-Extended *"does not impact a site's
inclusion in Google Search nor is it used as a ranking signal in Google
Search."*

**Live AI retrieval: largely unaffected.** Every blocked agent is a *training*
crawler. The retrieval-time agents are not blocked:

| Blocked (training) | Not blocked (retrieval / citation) |
|---|---|
| `GPTBot` — OpenAI model training | `OAI-SearchBot` — ChatGPT search results |
| | `ChatGPT-User` — live user-initiated browsing |
| `ClaudeBot` — Anthropic model training | `Claude-User`, `Claude-SearchBot` |
| `Google-Extended` — Gemini training/grounding | `Googlebot` |
| `CCBot` — Common Crawl (feeds many training sets) | `PerplexityBot` |

**What it does cost: ingestion into model training corpora.** If the goal is for
a model to *already know who Kyle is* without looking him up, that pathway is
switched off. If the goal is to be *found and cited* when someone asks, that
pathway is intact.

**Minor wart:** the file now contains two `User-agent: *` groups (Cloudflare's
and the repo's). The robots spec merges groups with the same user-agent, so this
is not broken — just untidy.

**The toggle lives in the Cloudflare dashboard**, not in the repo — editing
`public/robots.txt` will not remove it. It is the **Managed robots.txt** toggle
on the AI Crawl Control → Overview page. **Kyle turned it off on July 30, 2026**
(see the update at the top of this section). If `kylecovan.com/robots.txt` ever
again differs from `kylecovan-site.pages.dev/robots.txt`, that toggle — or the
"Display Content Signals Policy" checkbox on the zone Overview — is where to
look first.

---

## ⚠️ How to verify DNS honestly — read before trusting any probe

A false alarm was raised during this migration: the malformed SPF record
appeared to be back on 5 of 60 queries. **It wasn't.** The measuring instrument
was broken — the sandbox running those queries transparently intercepts all UDP
port 53 traffic and answers from a cache no matter which nameserver IP is
addressed. The stale answers were pre-deletion cached copies.

**Three checks that catch this instantly:**

1. **`AA` (authoritative answer) flag** — a real authoritative server sets it.
   Those responses had `AA=False`, `RA=True`.
2. **Ask the nameserver about a domain it doesn't host** — a genuine
   authoritative server refuses. That "Cloudflare nameserver" resolved
   `google.com` happily.
3. **TTL should be constant** from an authoritative server. A cache counts down.
   Those were counting down.

**Use DNS-over-HTTPS instead** — encrypted end to end, cannot be transparently
intercepted:

```
https://dns.google/resolve?name=kylecovan.com&type=TXT
https://dns.google/resolve?name=google._domainkey.kylecovan.com&type=TXT
```

**For anything HTTP, use a real browser.** A sandboxed egress proxy may return
403 for `kylecovan.com` and `kylecovan-site.pages.dev`, in which case `curl`
from there proves nothing about the site.

**General rule: positive results from a cache can be trusted; absence and
staleness cannot. The dashboard beats every remote probe, because it is the
zone rather than a copy of it.**

---

## The strongest post-migration check

Not a DNS query — **real mail arriving.** Cloudflare's own zone-activation
notice was delivered to `kyle@kylecovan.com` at 03:47 UTC on July 29, which by
definition was sent after the nameservers moved and therefore arrived through
the Cloudflare-served MX records. Record inspection proves records exist;
delivered mail proves the path works.
