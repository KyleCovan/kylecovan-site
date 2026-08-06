> Source: `src/content/writing/scheduled-agent-billing-trap.md` · X / Twitter · **unposted**
> Conversational register (voice.md Sample 3). No em dashes. Edit before posting.
> Machine-agnostic — survived the August 5 iMac-to-M1-Pro reversal unchanged.

I almost set up a scheduled AI agent that would have billed the wrong account.

I pay for Claude Max. Figured a cron job running Claude Code would draw on that.

It does not. If you have ANTHROPIC_API_KEY set anywhere, headless mode uses the key and ignores your subscription.

Someone filed an issue after doing this. $1,800 in two days.

Go run this before you automate anything:

echo $ANTHROPIC_API_KEY

Full writeup in today's build log.
