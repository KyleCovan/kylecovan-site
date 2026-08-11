<!-- Source: src/content/writing/half-a-website-audit-was-wrong.md · UNPOSTED · queued 2026-08-06 -->

**Half a website audit was wrong, and checking it took an hour**

Posting this because I think a lot of us are going to start getting these, and because the failure is more interesting than the findings.

An unsolicited audit of my site showed up. Twenty pages, scored, color coded, ending with a $1,500 offer to fix everything.

I checked every claim before touching anything. About half didn't survive.

The number one critical finding was that my sitemap is broken. It isn't. It returns the right file with the right content.

Here's how it got there. My site had a flaw where any address that doesn't exist returned my homepage with a success code instead of a "not found." The scanner looked for my sitemap in seven places, six of which don't exist, and all six came back looking real. Six confusing answers, and it drew the wrong conclusion about the seventh, the one that actually worked.

Two other findings were also wrong. Six links flagged as broken were already correct. My author name was flagged as missing from the page data when it was there, just written as a reference the scanner didn't follow.

Two findings were real and worth having. The homepage flaw itself, and a dead contact link caused by a Cloudflare privacy feature that was protecting nothing, because my email sits in plain text further up the same page anyway.

What I took from it, and the reason I'm posting:

A scanner tells you what it measured. It can't tell the difference between a site that's broken and a site that's arranged differently than it expected. The expensive mistake isn't the finding you miss. It's the afternoon you spend fixing something that was already right.

Curious whether anyone here has had the same experience, with an SEO report or a security scan or anything similar. Did you check it first, or did you find out the hard way?
