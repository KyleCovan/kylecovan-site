---
title: "Check which account your scheduled AI agent bills"
date: 2026-08-06
draft: true
---

This one is short and it might save you a lot of money.

The whole point of my home server build is to have an AI agent do useful work while I am not at my desk. A job that runs at five in the morning, reads the notes I touched yesterday, and leaves something useful in my vault before I wake up.

The mechanics of that are simple. You write a script, you schedule it, the script calls Claude Code in headless mode. That is a few lines of shell.

The part that is not simple is which account pays for it.

## Two accounts that look like one

I pay for Claude Max. I assumed that a scheduled job running Claude Code would draw against that subscription, because that is what I pay for and it is the same tool I use all day.

That assumption is wrong, and it is wrong in an expensive direction.

There are two entirely separate billing systems. There is the Claude subscription, which is a flat monthly fee. And there is the Anthropic API, which is pay per token. They are different accounts. They are different money. Nothing warns you when you cross from one to the other.

Here is the mechanism, straight from the documentation. When you run Claude Code in non interactive mode, the flag you use for any scheduled job, an API key in your environment takes priority over your subscription. The docs say it plainly: in non interactive mode the key "is always used when present."

So if you have `ANTHROPIC_API_KEY` set anywhere, in your shell profile, in a project file, left over from something you were experimenting with months ago, then your scheduled job silently bills the API account. Your subscription sits there unused.

## What that actually costs

There is a filed issue on the Claude Code repository from a Max subscriber who did exactly this. A scheduled job, an API key inherited from the environment, no warning.

Eighteen hundred dollars in two days.

Not because the job was doing anything unreasonable. Because it fired on a schedule, every run sent the full context, and every run billed to an account he was not watching.

The failure mode is specific to automation. When you are sitting at the terminal you notice things. A job that runs at five in the morning is a job nobody is watching, which is exactly why we automate it and exactly why this is dangerous.

## The fix

Two steps, and you need both.

First, generate a token that is actually tied to your subscription:

```
claude setup-token
```

That opens a browser, you approve, and it gives you an OAuth token good for one year. Put it in the environment as `CLAUDE_CODE_OAUTH_TOKEN`.

Second, and this is the part that is easy to skip, explicitly clear the API key inside the script itself:

```
unset ANTHROPIC_API_KEY
unset ANTHROPIC_AUTH_TOKEN
export CLAUDE_CODE_OAUTH_TOKEN="$(cat ~/.config/claude/oauth-token)"
```

Do not rely on it simply not being set. Cron and launchd inherit environments in ways that are not always obvious, and the whole problem is that this fails silently. Clear it in the script, every time.

One more thing worth knowing: there is a `--bare` flag that is otherwise good for scripted runs, and it does not read the OAuth token. If you pass it, you are back on the API key. Do not use it with this setup.

## Go check right now

Before you schedule anything, run this:

```
echo $ANTHROPIC_API_KEY
```

If something comes back, find out where it is being set before you build any automation on top of it.

I have folders in my home directory from four or five different AI tools I have tried over the past year. Any one of them could have exported a key at some point. I would not have known, and I would not have found out until the bill arrived.

## The wider point

I am building a machine that does work while I am asleep. That is the entire goal, and I still think it is the right goal.

But "runs while you are not watching" and "spends money while you are not watching" are the same sentence. The thing that makes automation valuable is the thing that makes it risky, and you get the risk for free whether you plan for it or not.

So the first job I schedule is going to log what it did and what it cost, every single run. Not because I expect a problem. Because five in the morning is a bad time to find out about one.
