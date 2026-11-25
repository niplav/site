# new forum/reddit/twitter daygame datasets (search run 2026-11-21)
# reddit.com and web.archive.org fetches refused; web search returned almost no reddit posts.

DATASETS_NEW_FORUMS = [
	(name="@BroodingSea (twitter, quoted by Refinery29)", urls=["https://www.refinery29.com/en-gb/2019/08/239673/daygame-what-is-it"], from_start=:yes, start_evidence="tweet 2019-08-10: 'Stats on the year', 'started #Daygame in March' (2019)", date_kind=:unknown, lay=[96 8], date=[96 10], numbers=[96 26], idates=[96 5], appr_per_hour=missing, date_cost=missing, date_hours=missing, dates_per_lay=missing, flake_rate=missing, expenditures=missing, hours_total=missing, status=:new, notes="single snapshot. tweet lists Insta 11, idate 5, SDL 3, 'Of the 10 dates' (list says 5 dates, conflict; recorded 10 per tweet notes). Article: '38% of approaches lead to Insta or number close', '27% of these lead to a date', '80% date conversion' (not recorded as matrices, derivable only from counts)."),
]

# ============================================================
# Searched for cost/time/flake data: findings (aggregate/thread-level, NOT per-person)
# ============================================================
#
# actualized.org "how much time per day do I need to work on my dating skills" (topic 92908, page 3), 2023-05-30:
#   hours: "I'd say a few hours per week." (Roy); "3hrs per night x 3 nights/week would be a great foundation." (Leo Gura);
#   "2-3 hours for just 1 day per week" (Miguel1); "30 minutes is more than enough as an intermediate." (StarStruck).
#   approaches/hour: "They would do 10 approaches on a 2 hour season in a busy street." (Karmadhi) -> ~5 approaches/hour, second-hand, unquantified busy-street anecdote.
#   totals: "I know guys that have done 2000 daygame approaches in like 2 years." (Karmadhi) -> third-party, not a personal count.
#   money: none. dates/lays: none.
#   URL: https://www.actualized.org/forum/topic/92908-how-much-time-per-day-do-i-need-to-work-on-my-dating-skills/
#
# actualized.org "day game minimizing flakes" (topic 64923), 2021-04:
#   flake rate: none. approaches/hour: none. hours: none. dates/lay: none.
#   Personal counts (not in requested fields): StarStruck "5-10 approaches for the last 3 weeks" (comment 887181);
#   "5 pickups per patrol, 2 days per week" (comment 887755); Harlen Kelly "slept with over 70+ chicks primarily from cold approach" (comment 887228, lays only, no approach count, excluded).
#   URL: https://www.actualized.org/forum/topic/64923-day-game-minimizing-flakes/
#
# Blog/coach claims (secondhand, not per-person; do not merge):
#   daygamersbible 2018 via niplav.github.io/daygame_cost_benefit.html: 16.9% approaches->numbers, 22.4% numbers->dates, 37.1% dates->lays;
#   beginner 1 lay / 100 approaches, intermediate 1/50, advanced 1/30.
#   Actualized forum (unnamed mentor): 4-5 numbers per 10 approaches, 2 dates and 1 lay; survey of PUAs 3-5 numbers / 10 approaches, ~1 date / 10 numbers.
#   "450 approaches to get your first lay" (Leo's course, quoted on actualized 91592).
#
# Cost per date: no daygame thread found stating money per date, hours per date, dates_per_lay or flake rates.
#   (Only app-dating cost figures from Vice ~$60-70/date, not daygame; excluded.)
#
# Excluded per-person candidates (no approach count or not cumulative):
#   assx95 actualized 91592 ("100+ approaches", 3 number closes "so far", no dates/lays; "100+" is a lower bound).
#   pablo_aka_god actualized 110737 ("8 girls from DG", lays only).
#   Hardkill actualized 17640 (secondhand ratios only).
#   theredquest.substack "field report" ("Only four sets" for one session; "1000s" lifetime, not exact).
#
# Not reachable / not found: r/seduction, r/daygame, r/coldapproach (reddit.com refused); web.archive.org refused;
#   Twitter/X daygame stat accounts (no search hits beyond the BroodingSea tweet above); mPUA, Sosuave, Rooshv, RSD, daygame.com forum: no hits;
#   public Google Sheets trackers and subreddit polls: none found.
