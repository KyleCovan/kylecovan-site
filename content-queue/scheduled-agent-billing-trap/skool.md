> Source: `src/content/writing/scheduled-agent-billing-trap.md` · Skool · **unposted**
> Conversational register (voice.md Sample 3). No em dashes. Edit before posting.
>
> ⚠️ NEEDS AN EDIT BEFORE POSTING. The billing content is machine-agnostic and
> survives, but paragraphs 2 and 4 frame the whole post around the 2019 iMac, which
> Kyle reversed on August 5 in favour of the clamshelled M1 Pro. Strip or update the
> iMac framing. The forgotten-decision-log anecdote still happened and still stands.

Started a build this week that I think a few of you will find useful, and I want to share the mistakes as much as the plan.

I am taking a 2019 iMac that has been sitting around doing nothing and making it an always on server. The goal is simple: my Obsidian vault syncs across my phone, laptop and iPad no matter which one is awake, and my AI setup can run jobs while I am not at my desk.

Two things from day one.

The first is a little embarrassing and probably relatable. I spent real time working out which machine to use, and then found a decision log entry in my own vault from two weeks earlier where I had already decided it and written down all my reasoning. I keep the log specifically so I do not redo work. It only helps if I open it.

The second one matters more, especially for anyone here running automations.

If you schedule Claude Code to run unattended, it does not necessarily bill your subscription. In non interactive mode, an API key in your environment takes priority. So if you have ANTHROPIC_API_KEY set anywhere, even from something you tried months ago and forgot, your scheduled job quietly bills the API account instead of the plan you are already paying for.

There is a filed issue from someone this happened to. $1,800 in two days.

The fix is two steps. Run `claude setup-token` to get a token tied to your subscription, and then explicitly `unset ANTHROPIC_API_KEY` inside the script itself. Do not just assume it is not set, because the failure is silent and cron inherits environments in ways that are not obvious.

If you take one thing from this, take this: run `echo $ANTHROPIC_API_KEY` right now, before you automate anything.

Happy to answer questions on any of it. I will keep posting as the build goes.
