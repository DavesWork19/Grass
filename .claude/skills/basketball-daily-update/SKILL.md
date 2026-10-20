---
name: basketball-daily-update
description: Run the backendV2 NBA pipeline for today's games and publish the results (games, parlays, model record) to the Health App frontend - committing AND pushing both the frontend repo and any backendV2 code changes, with no further prompting needed. Use this whenever asked to run backendV2 / the basketball or NBA pipeline, update today's NBA games/picks/parlays, publish the basketball frontend, or anything equivalent to "do the daily basketball update" - including on a recurring/scheduled basis. Encodes what was learned reviving the pipeline for the 2026-27 season (Python interpreter, cold start, DraftKings listing tomorrow's games, idempotent reruns) so none of it needs rediscovering.
---

# backendV2 daily NBA update

Runs the NBA prediction pipeline for today's slate and publishes the output to the
Health App frontend. End to end, with commits pushed, so the user doesn't need to
babysit it or re-explain the process. Unlike football (weekly), this runs **once per
game day** - run it before the day's first tip-off.

## Repos involved

- **Backend**: `/Users/davidcarney/Desktop/NFL_WORKING/Grass` (git branch `superGrassy`) -
  the `backendV2/` pipeline code. Table `BBALL7` in local Postgres.
- **Frontend**: `/Users/davidcarney/Desktop/Health App/health-app` (git branch `main`) -
  receives three generated files: `app/commonComps/todaysGames.js`,
  `todaysParlays.js`, `newPercents.js` (no "Basketball" suffix - the unsuffixed names
  are the NBA ones; the `*Football.js` files belong to football-weekly-update).

Check both repos' `git status`/`git log` before starting - another session may have
changed either one (the football frontend format changed underneath its pipeline once).

## Procedure

1. **Clean up stray Chrome processes** (the DraftKings scrape uses Selenium):
   ```
   pkill -f chromedriver; pkill -f "Chrome for Testing"; pkill -f undetected
   ```

2. **Run the pipeline** - use `/usr/local/bin/python3` explicitly. The `python3` on PATH
   is anaconda's Python 3.8 with sklearn 0.23, which is too old for this code.
   ```
   /usr/local/bin/python3 -u /Users/davidcarney/Desktop/NFL_WORKING/Grass/backendV2/main.py 2>&1
   ```
   - No arguments. The season is derived from the date (`constants.current_season_year()`:
     Basketball Reference names 2026-27 as `2027`, rolling over in August), and "today's
     games" means today's date.
   - Use `-u` and run in the background via `run_in_background`, watching for
     `/ 7|Finished|Traceback|Error|FAILED`. It takes a few minutes on a full slate
     (~4 Basketball Reference pages per team playing, with polite delays).
   - **Rerunning is safe** - `saveData` deletes today's rows before reinserting.

3. **Expected, non-fatal output** - don't "fix" these:
   - `Skipped (next game is not today): [...]` - DraftKings' NBA board lists tomorrow's
     games right after today's. `saveData` keeps only teams whose next Basketball
     Reference game is dated today. A long skipped list is normal.
   - `Table with id='team_game_log_reg' not found!` + `(carried over from last season)` -
     the team hasn't played yet this season, so last season's stats stand in
     (`last_game_in_season = 0`, `days_since_last_game` capped at 9). Expected for each
     team's first game of a season only.
   - `Couldn't save row ...` in stage 1/7 (`updateDBActuals`) - a score couldn't be
     graded this run. Every run re-sweeps all ungraded current-season rows, so it
     self-heals next time.
   - `Skipping X @ Y: ...` in runDaBot/runDaParlays - a team's row failed to save or has
     too little history; that game is just left off the frontend.

4. **Actually-fatal failures** (need a real fix, not a rerun):
   - `FAILED <team>: ...` in stage 0 for many teams, or DraftKings listing 0 games -
     the scraper markup likely changed. Inspect `scrape_todays_gambling_data` /
     Basketball Reference tables in `backendV2/scrapes.py`. Basketball Reference is
     not behind Cloudflare (plain `requests` works) - if that changes, port
     footballV2/scrapes.py's undetected-chromedriver `_fetch_soup`.
   - `home/away mismatch between DraftKings and Basketball Reference` - a team
     abbreviation mapped wrong; fix `DK_TO_BBREF` in `constants.py`.
   - A Chrome/chromedriver version error - see football-weekly-update's notes on
     `_installed_chrome_major_version()`.
   - Any other traceback - read it and fix the root cause in backendV2, verify with a
     small standalone script, then rerun.

5. **Verify before publishing** - read the generated files in
   `Health App/health-app/app/commonComps/`:
   - `todaysGames.js`: header rows `'DayName'`, `'Month DD, YYYY'` for **today**, then one
     row per game `'time,Away Team,Home Team,homeSpread,0|1,overUnder,0|1,awayML,homeML,0|1'`.
     Game count should match today's real NBA slate. Spreads/moneylines use ASCII `-`.
   - `todaysParlays.js`: 3 blocks (`todaysParlay1..3`) with today's date; a block can
     legitimately have no picks.
   - `newPercents.js`: real numbers (includes prior seasons by design). It's fine if it's
     unchanged on a day when no new games were graded (e.g. opening night).
   If the date is wrong or games are missing, don't publish - find out why.

6. **Commit and push BOTH repos** - the user does not want to be asked each time:
   - Frontend (`Health App/health-app`, branch `main`):
     ```
     git add app/commonComps/todaysGames.js app/commonComps/todaysParlays.js app/commonComps/newPercents.js
     git commit -m "Update Frontend - NBA <Month DD, YYYY>

     Generated by backendV2 pipeline: today's games, parlays, and updated
     model record.

     Co-Authored-By: Claude <noreply@anthropic.com>"
     git push origin main
     ```
     Only stage those three files - the repo carries unrelated local changes
     (`.env.local`, `.gitignore`) that aren't yours to commit.
   - Backend (`Grass`, branch `superGrassy`) - **only if backendV2 code changed** this run
     (`git status --short backendV2/`; never add `backendV2/__pycache__/`):
     ```
     git add backendV2/<changed files>
     git commit -m "Update Backend - <what changed and why>

     Co-Authored-By: Claude <noreply@anthropic.com>"
     git push origin superGrassy
     ```

7. **Clean up** stray Chrome processes again, same command as step 1.

## Reporting back

Short summary: which date published, number of games, commit hashes for both repos (if
pushed), the model's current record (`overall_spread`/`overall_overUnder`/
`overall_moneyLine` in `newPercents.js`), and anything noteworthy from steps 3-4.
Don't dump the scrape log.
