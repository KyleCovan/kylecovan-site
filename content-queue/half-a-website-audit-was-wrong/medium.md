<!-- Source: src/content/writing/half-a-website-audit-was-wrong.md · UNPOSTED · queued 2026-08-06 -->

**Title:** Half a website audit was wrong
**Subtitle:** A scanner tells you what it measured. That is not the same as what is true.
**Tags:** SEO, Web Development, Cloudflare, Building In Public, AI

---

Someone sent me an audit of my site. Twenty pages of it, scored and color coded, ending with an offer to fix everything for fifteen hundred dollars.

I didn't fix anything. I checked it first. About half of it was wrong.

That isn't a complaint about the people who sent it. It's a thing worth knowing if one ever lands in your inbox, because acting on it without checking would have had me editing parts of my site that were already correct.

## The headline error

The report's number one critical finding was that my sitemap is broken. A sitemap is just a file listing every page on a site, so search engines can find them all. Mine, the report said, is advertised but never actually served.

I opened it. It works. Right file, right content, right response.

So how does a scanner get that wrong?

## The trap underneath it

My site sits behind Cloudflare, and until that night it had a quiet flaw. If you asked for an address that doesn't exist, it didn't say "not found." It handed back my homepage and reported success.

The scanner went looking for the sitemap in seven different places. Six of those don't exist on my site. All six came back looking like a real page, because on my site everything came back looking like a real page. So the scanner got six confusing results and drew the wrong conclusion about the seventh, which was the one that actually worked.

The tool didn't lie. It reported exactly what it measured. What it measured wasn't what was true.

## Two more that didn't hold up

It said six pages had links pointing at slightly wrong addresses, forcing an extra hop on every click. Every one of those links was already correct.

It said the machine readable summary of my writing was missing the author's name. The name is there. It's written as a reference pointing to another part of the same block, which is normal and valid, and the scanner didn't follow it.

It also told me to add a security setting my site was already sending.

## What was actually right

Two things, and both were worth the trouble.

The first is that flaw I described. Every made up address returning my homepage with a success code is a real problem. Search engines read it as one page copied across an unlimited number of addresses, and they waste their time confirming each one. That's fixed now.

The second is better, and I wouldn't have found it on my own.

My contact link was dead.

Cloudflare has a feature that hides your email address from scrapers. It rewrites the link into a scrambled version and adds a small script to unscramble it for real visitors. That sounds sensible.

Except the address it rewrote mine to returns a "not found" error. So anyone without that script running, which includes every search engine and every AI assistant, hit a dead end on the one link I most want people to use.

And it was protecting nothing. My email address sits in plain text further up the same page, in the section that describes who I am. Cloudflare doesn't touch that one. The scrambled version also unscrambles in about a line of code. I tried it. It took seconds.

So the feature was costing me a working contact link and buying me no privacy at all.

## The part that stung

Three days before any of this, I'd written that homepage flaw down in my own decision log. Same behavior, same cause, already documented in my own words.

The scanner walked straight into a hole I had already mapped. And I still had to check every one of its claims by hand to work out which half was real.

## What I'd tell you

A scanner tells you what it measured. It doesn't tell you what's true, and it can't tell the difference between a site that's broken and a site that's arranged differently than it expected.

The expensive mistake isn't the finding you miss. It's the afternoon you spend fixing something that was already right.

Check the claim before you touch the code. Verifying the whole report took me about an hour, and that hour is the only reason I know which half to trust.
