<!-- Source: src/content/writing/half-a-website-audit-was-wrong.md · UNPOSTED · queued 2026-08-06 -->

**Thread**

1/
Someone sent me a 20 page audit of my website. Scored, color coded, ending with an offer to fix it all for $1,500.

I checked it before fixing anything.

About half of it was wrong.

2/
Its #1 critical finding: my sitemap is broken.

I opened it. It works. Right file, right content, right response.

So how does a scanner get that wrong?

3/
My site had a quiet flaw.

Ask it for an address that doesn't exist and instead of saying "not found," it handed back my homepage and reported success.

Everything looked real. Including the things that weren't there.

4/
The scanner looked for my sitemap in 7 places.

6 of them don't exist on my site. All 6 came back looking like real pages.

So it got 6 confusing answers and drew the wrong conclusion about the 7th, which was the one that actually worked.

5/
The tool didn't lie.

It reported exactly what it measured.

What it measured wasn't what was true.

6/
Two more findings didn't hold up.

6 links flagged as pointing to wrong addresses. All 6 already correct.

Author name flagged as missing from my page data. It's there, written as a reference the scanner didn't follow.

7/
But two were real, and one I'd never have found alone.

My contact link was dead.

8/
Cloudflare has a feature that hides your email from scrapers. Scrambles the link, adds a script to unscramble it for real visitors.

The address it rewrote mine to returns an error.

Every crawler, every AI assistant, anyone without JS: dead end.

9/
And it was protecting nothing.

My email sits in plain text further up the same page.

The scrambled version unscrambles in about a line of code. I tried it. Took seconds.

A dead link, bought with no privacy.

10/
The lesson:

A scanner tells you what it measured. It can't tell the difference between a site that's broken and a site that's arranged differently than it expected.

The expensive mistake isn't the finding you miss. It's the afternoon you spend fixing what was already right.
