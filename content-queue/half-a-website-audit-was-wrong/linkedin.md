<!-- Source: src/content/writing/half-a-website-audit-was-wrong.md · UNPOSTED · queued 2026-08-06 -->

Someone sent me a twenty page audit of my website. Scored, color coded, ending with an offer to fix it all for fifteen hundred dollars.

I checked it before I fixed anything. About half of it was wrong.

Its number one critical finding was that my sitemap is broken. I opened it. It works fine.

Here's how a tool gets that wrong.

My site had a quiet flaw. Ask it for an address that doesn't exist, and instead of saying "not found," it handed back my homepage and reported success.

The scanner looked for the sitemap in seven places. Six of them don't exist on my site. All six came back looking real, because everything came back looking real. So it got six confusing answers and drew the wrong conclusion about the seventh, which was the one that worked.

The tool didn't lie. It reported exactly what it measured. What it measured wasn't true.

Two other findings didn't hold up either. It flagged six links as pointing to the wrong addresses. All six were already correct. It said my author name was missing from the page data. It's there, written as a reference the scanner didn't follow.

But two findings were real, and one of them I would never have found alone.

My contact link was dead.

Cloudflare has a feature that hides your email from scrapers. It scrambles the link and adds a script to unscramble it for real visitors. The address it rewrote mine to returns an error. So every search engine, every AI assistant, and anyone without that script hit a dead end on the one link I most want people to use.

And it was protecting nothing. My email sits in plain text further up the same page. The scrambled version unscrambles in about a line of code. I tried it. Seconds.

The lesson I'd pass on:

A scanner tells you what it measured. It can't tell the difference between a site that's broken and a site that's arranged differently than it expected.

The expensive mistake isn't the finding you miss. It's the afternoon you spend fixing something that was already right.

Verifying the whole report took about an hour. That hour is the only reason I know which half to trust.
