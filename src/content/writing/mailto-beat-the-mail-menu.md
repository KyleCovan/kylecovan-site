---
title: "Mailto beat the mail menu"
date: 2026-08-10
project: tapocanyon
draft: true
---

I built a polite little menu on the free mini report button. Pick Gmail. Pick Outlook on the web. Pick the mail app. Let the visitor choose where the draft opens.

It felt helpful. Live testing said otherwise.

The web compose links were flaky. Sometimes they opened a browser tab the person did not want. Sometimes they failed in ways that looked like my site was broken. Cloudflare had its own habit of rewriting mailto links, which I had to stop separately. Meanwhile the owners I am writing for mostly live in the mail app on their phone or Mac. They do not want a second web client interposed between "I want this report" and "here is the draft."

So the fancy menu came off. The button is a plain mailto again. Subject and body filled in. One click into the tool they already use.

The lesson is small and I will forget it if I don't write it down: a choice that looks considerate can be friction when the default already works. Test the path a real person takes, not the path that looks complete in a wireframe.
