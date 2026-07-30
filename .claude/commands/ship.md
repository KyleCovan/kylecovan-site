---
description: Verify, commit and push to main (this deploys)
argument-hint: [commit message]
---

Ship the current changes. **Pushing to `main` deploys to kylecovan.com.**

1. `git status` and `git diff` — show me exactly what is about to go out.
2. Run the full gate:
   ```bash
   source .venv/bin/activate && npm run build && npm run verify
   ```
   **Stop if either suite does not print ALL CHECKS PASSED.** Do not push.
3. Check the diff against the constraints before committing:
   - Did any design rule change without its test changing in the same commit?
     If so, fix that now — the assertion gets rewritten, never deleted.
   - Did any of Kyle's copy get reworded? (`docs/handoff.md` §6.) If so, revert
     that hunk.
   - Any new external request, second executing script, card, border, or
     centred element? (§2, §3.)
   - Is `dist/` staged? It shouldn't be.
4. Commit with: $ARGUMENTS
5. Confirm the branch is `main` and the prompt is in `kylecovan-astro`, then push.
6. Tell me the Cloudflare Pages build is now running and what URL to check.

Afterwards, update `docs/handoff.md` — the revision log in §9, plus any section
whose rules this change touched.
