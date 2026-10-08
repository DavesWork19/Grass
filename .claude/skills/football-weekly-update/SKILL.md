---
name: football-weekly-update
description: Run the footballV2 NFL pipeline for the current week and publish the results (games, parlays, model record) to the Health App frontend - committing AND pushing both the frontend repo and any footballV2 backend code changes, with no further prompting needed. Use this whenever asked to run footballV2, update this week's games/picks/parlays, publish the football frontend, or anything equivalent to "do the weekly football update" - including on a recurring/scheduled basis. Encodes everything learned running this pipeline live across many real weeks (Chrome driver version pinning, DraftKings scraper quirks, idempotent reruns, PFR flakiness) so none of that needs rediscovering.
---

# footballV2 weekly update

Runs the NFL prediction pipeline for the current week and publishes the output to the
Health App frontend. End to end, with commits pushed, so the user doesn't need to
babysit it or re-explain the process.

## Repos involved

- **Backend**: `/Users/davidcarney/Desktop/NFL_WORKING/Grass` (git branch `superGrassy`) -
  the `footballV2/` pipeline code.
- **Frontend**: `/Users/davidcarney/Desktop/Health App/health-app` (git branch `main`) -
  receives three generated files: `app/commonComps/todaysGamesFootball.js`,
  `todaysParlaysFootball.js`, `newPercentsFootball.js`.

Check both repos' `git status`/`git log` before starting - another session may have
changed either one (this has happened before: the frontend's JS format changed
underneath the pipeline once, and footballV2 itself has been hand-edited directly). Don't
assume this memory's description of either repo's current shape is still accurate without
a quick look first.

## Procedure

1. **Clean up stray Chrome processes** before starting - leftover `chromedriver`/`Google
   Chrome`/`undetected_chromedriver` processes from a prior run can make the browser
   launch hang or attach to the wrong session:
   ```
   pkill -f chromedriver; pkill -f "Chrome for Testing"; pkill -f "Google Chrome"; pkill -f undetected
   ```

2. **Run the pipeline** from `footballV2/`:
   ```
   cd /Users/davidcarney/Desktop/NFL_WORKING/Grass/footballV2
   python3 -u main.py 2>&1
   ```
   - No week argument needed - `main.py` calls `get_current_week(date.today(),
     WEEK_DATE_RANGES)` and figures out the right week itself.
   - Use `-u` (unbuffered) and run in the background via the Bash tool's
     `run_in_background`, then watch the output file / a Monitor grep for
     `/ 7|Finished|Traceback|Error:|Exception`. Buffered output on a background process
     looks identical to "hung" - don't assume a stall without checking.
   - This takes several minutes (32 teams' PFR gamelogs get scraped twice - once in
     `saveData` for the new week, once in `updateDBActuals` to backfill last week's
     results - plus the DraftKings odds scrape and model training). That's normal.
   - **It's safe to just rerun `main.py <week>`** if something fails partway - `saveData`
     clears that week's existing rows before reinserting, so reruns don't duplicate data.

3. **Known non-fatal noise** - don't stop or "fix" these, they're expected and self-heal:
   - `Gamelog table not found for <code> (2026)!` - a PFR fetch came back empty. Happens
     for a handful of teams most runs (Cloudflare flakiness). That team's week stays
     ungraded until the *next* run, because `updateDBActuals` re-sweeps every row with a
     null `actual_spread` every time it runs, not just the current week's.
   - `_fetch_soup ... failed (...); restarting browser` - the scraper detected a wedged
     Chrome session and is recovering on its own (up to 3 attempts per page).
   - `skipping <away> @ <home> - not enough history` / `not enough history` in runDaBot -
     expected for the first several weeks of a season (not enough prior games to train
     on yet).

4. **Actually-fatal failures** to watch for (these need a real fix, not a rerun):
   - `SessionNotCreatedException` / "This version of ChromeDriver only supports Chrome
     version N" - Chrome.app auto-updated past what's cached. Check
     `scrapes.py`'s `_installed_chrome_major_version()` is still correctly detecting the
     installed browser (`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome
     --version`) - it's supposed to self-correct, but if Chrome moved paths or the
     version string format changed, this needs a manual look.
   - DraftKings returns a wildly wrong game count (not ~13-16) - check
     `scrape_weekly_gambling_data` in `scrapes.py`: it stops at the first *repeated* team
     to avoid blending this week's slate with next week's (DK's widget lists both with no
     separator). If DK's markup changed again, this heuristic may need revisiting.
   - Any traceback not covered above - read it, fix the root cause in footballV2 (don't
     patch around it with flags or skips), verify with a small standalone script before
     re-running the full pipeline.

5. **Verify before publishing** - read all three generated files in
   `Health App/health-app/app/commonComps/`:
   - `todaysGamesFootball.js`: should have one `'DayName|Month DD, YYYY'` header row per
     distinct game day (typically Thu/Sun/Mon, sometimes more for a short week), with
     that day's games listed right after it, sorted by kickoff time. Roughly 13-16 games
     total depending on byes.
   - `todaysParlaysFootball.js`: 3 parlay blocks; can legitimately be empty (just header
     rows) early in a season or if no picks clear the confidence threshold - that's not a
     bug.
   - `newPercentsFootball.js`: should have real (non-zero, non-empty) numbers, not `{}`.
   If any of these look wrong, don't publish - go back and find out why instead of
   committing broken output.

6. **Commit and push BOTH repos** - the user does not want to be asked each time:
   - Frontend (`Health App/health-app`, branch `main`):
     ```
     git add app/commonComps/todaysGamesFootball.js app/commonComps/todaysParlaysFootball.js app/commonComps/newPercentsFootball.js
     git commit -m "Update Frontend - NFL Week <N> <year>

     Generated by footballV2 pipeline: this week's games, parlays, and
     updated model record.

     Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
     git push origin main
     ```
     Only stage those three files - this repo tends to carry unrelated local changes
     (`.env.local`, `.gitignore`) that aren't yours to commit.
   - Backend (`Grass`, branch `superGrassy`) - **only if footballV2 code actually
     changed** this run (check `git status --short footballV2/`; ignore
     `footballV2/__pycache__/`, it's a build artifact and shouldn't be added):
     ```
     git add footballV2/<changed files>
     git commit -m "Update Backend - <what changed and why>

     Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
     git push origin superGrassy
     ```
     Push this too - don't leave it local-only waiting to be asked.

7. **Clean up** stray Chrome processes again when done, same command as step 1.

## Reporting back

Give a short summary: which week published, the commit hashes/URLs for both repos (if
pushed), the model's current record (from `newPercentsFootball.js`'s `overall_*` keys),
and anything noteworthy from steps 3-4 (teams that stayed ungraded, bugs fixed). Don't
dump the full scrape log - the user wants to know it worked, not watch it work.
