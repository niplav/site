[home](./index.md)
-------------------

*author: niplav/Claude 3.7 Sonnet/Claude 4 Sonnet/Claude 4.6 Opus/Claude Opus 5.5/Llama-3.1-405B, created: 2025-08-19, modified: 2026-11-26, language: english, status: in progress, importance: 1, confidence: fiction*

> __Fileservers × mechanism design × sub-cent microtransactions. A
personal æsthetic.__
>  
>  
> __¢|⋈__

`filepunk`
============

Co-written with a several Claudes, and a hefty amount of [steering
bits](https://gwern.net/blog/2025/good-ai-samples) from my side, some
vetting. Made messier with samples from Llama-3.1-405B, still
probably too clean for a real command line history.

<br><br><br><br><br>

```
term% cat /dev/user; date
niplav
Fri May 16 08:02:11 CEST 2025
term% cat /mnt/pay/balance
Ξ	0.004113
¢	184022.17
term% cat /mnt/pay/rate
Ξ1 = ¢301240 (oracle.ecb 08:00, ±0.4%)
term% venti/copy -f $venti tcp!venti.tarsnap.net!venti vac:1f3e09a2c4b7d58e6f0a3b19c2d74e8a5b6c0f13 &
term% srv tcp!claude.vigila!9fs claude
post...
term% mount -c /srv/claude /mnt/claude
mount: mount /mnt/claude: needkey proto=pay dom=claude.vigila
term% echo 'key proto=pay dom=claude.vigila cap=Ξ0.002/day !wallet=main' >/mnt/factotum/ctl
term% mount -c /srv/claude /mnt/claude
term% lc /mnt/claude
billing	ctl	ctx	models	usage
term% cat /mnt/claude/billing/quote
in	Ξ0.0000010/ktok
out	Ξ0.0000050/ktok
cache	Ξ0.0000001/ktok
term% lc /mnt/claude/ctx
1_icia	2_forecasting	3_vigila	4_stevemod
term% cd /usr/niplav/vigila
term% cat CLAUDE.md >/mnt/claude/ctx/3_vigila/sysprompt
term% cat TODO >>/mnt/claude/ctx/3_vigila/in
term% cat /mnt/claude/ctx/3_vigila/out
reviewed TODO. 3 items blocked on the venti migration (2, 5, 7),
item 4 is already done (commit 1a9f0e), item 1 is ready but
needs the new 9pay headers. want a patch?
term% echo y >>/mnt/claude/ctx/3_vigila/in
term% cta /mnt/claude/usage
cta: '/bin/cta' file does not exist
term% cat /mnt/claude/usage
ctx	tok_in	tok_out	cost
3_vigila	4212	1388	Ξ0.0000111
total today			Ξ0.0000111

term% srv tcp!nytimes.com!9fs nyt && mount /srv/nyt /n/nyt
post...
term% cat /n/nyt/price
article	¢3	(refunded if read <20%)
archive	¢9
cap	¢300/month (you: ¢294 used)
term% lc /n/nyt/2025/05/16
1_us	2_world	3_biz	4_tech	5_sci	6_sports	7_arts	8_opinion
term% lc /n/nyt/2025/05/16/4_tech
1_googai	2_plan9	3_breaches	4_aipatent	5_ercot
term% sed 3q /n/nyt/2025/05/16/4_tech/2_plan9
Bell Labs' Orphan, 30 Years On: How a Filesystem Ate the Web
By Cade Metz
MURRAY HILL, N.J. — In 1995, almost nobody outside a corridor
term% cat /n/nyt/2025/05/16/4_tech/5_ercot
cat: error reading /n/nyt/2025/05/16/4_tech/5_ercot: monthly cap reached (¢300); raise with 'cap ¢N' in /n/nyt/ctl
term% echo 'cap ¢400' >/n/nyt/ctl
term% grep nytimes /mnt/pay/log
08:05:03	nytimes.com	¢3	paid
08:05:09	nytimes.com	¢3	refunded (read 4%)
08:07:40	nytimes.com	¢3	declined (cap)
term% mkdir /mnt/pay/auto/arxiv.org
term% echo 'tip ¢0.5/paper' >/mnt/pay/auto/arxiv.org/ctl
term% echo 'cap ¢200/month' >/mnt/pay/auto/arxiv.org/ctl
term% srv tcp!netflix.com!9fs netflix && mount /srv/netflix /n/netflix
post...
term% lc /n/netflix/shows/labyrinths_on_cyprus
s01	s02	s03	s04	s05
term% treason /n/netflix/shows/labyrinths_on_cyprus/s05/e01.mkv &
term% cat /mnt/pay/meters
netflix.com	¢0.40/min	running 0:00:41	¢0.27

term% srv tcp!collab.local!9fs collab && mount /srv/collab /n/collab
post...
term% cat /n/collab/papers/icia/ctl
owner	niplav
writers	niplav Þórhildur·Björnsdóttir Anaïs
compensation	none
term% echo 'rate ¢0.1/Twrite cap ¢50 Þórhildur·Björnsdóttir' >/n/collab/papers/icia/ctl

term% mount /srv/datamarket /n/dm
mount: can't open /srv/datamarket: '/srv/datamarket' file does not exist
term% srv tcp!datamarket.eu!9fs datamarket && mount /srv/datamarket /n/dm
post...
term% echo 'SELECT year, avg(temp) FROM weather.daily WHERE station=''Praha-Klementinum'' AND year>2020 GROUP BY year' >/n/dm/queries/new
term% cat /n/dm/queries/last/quote
1.8M rows scanned (cached partial), Ξ0.0000041
term% echo accept >/n/dm/queries/last/ctl
term% cat /n/dm/queries/last/result
2021	10.4
2022	11.6
2023	11.9
2024	12.4
2025*	8.7
* partial year (Jan–May)

term% cd /usr/niplav/papers/icia
term% grep -n TODO *.lua
pin_reward.lua:41:	-- TODO: test with >3 reward functions
gridworld.lua:118:	-- TODO: verify convergence on gridworld_4x4
causal.lua:203:	-- TODO: handle splinter case in causal graph
term% grep -n TODO *.lua >>/mnt/claude/ctx/1_icia/in
term% echo 'write test cases for these, lua or steve, your call' >>/mnt/claude/ctx/1_icia/in
echo: write error: cap Ξ0.002/day reached (used Ξ0.0019987)
term% cat /mnt/claude/usage
ctx	tok_in	tok_out	cost
1_icia	1907344	12801	Ξ0.0019876
3_vigila	4212	1388	Ξ0.0000111
total today			Ξ0.0019987
term% echo 'delkey proto=pay dom=claude.vigila' >/mnt/factotum/ctl
term% echo 'key proto=pay dom=claude.vigila cap=Ξ0.004/day !wallet=main' >/mnt/factotum/ctl
term% echo 'evict cache older 7d' >/mnt/claude/ctx/1_icia/ctl
term% echo 'write test cases for these, lua or steve, your call' >>/mnt/claude/ctx/1_icia/in

term% date
Fri May 16 11:47:30 CEST 2025
term% srv tcp!generalcomputecorp.com!9fs gpu
srv: dial tcp!generalcomputecorp.com!9fs: auction closed, next window 14:00 UTC
term% srv tcp!gpu.market.gl!9fs gpu && mount -c /srv/gpu /n/gpu
post...
term% sed 4q /n/gpu/auction/book
model	free	clearing(5m)	mechanism
h200	37	Ξ0.0000139/min	2nd-price, 1m slots
b200	4	Ξ0.0000311/min	2nd-price, 1m slots
mi355x	112	Ξ0.0000094/min	2nd-price, 1m slots
term% echo 'bid model=h200 n=1 max=Ξ0.00002/min' >/n/gpu/auction/ctl
term% cat train_pin.lua >/n/gpu/sessions/new
term% cat /n/gpu/sessions/last/status
running on h200#2291 since 11:52:07, paying Ξ0.0000142/min (4 bidders)

term% echo 'pools:
  pool0: {resource: 32×amd64, access: immediate, bid: Ξ0.0009/4h}
  pool1: {resource: 16×amd64, access: <30min, bid: Ξ0.0005/6h}
  pool2: {resource: 8×arm64, access: <2h, bid: Ξ0.0002/8h}
batna: Ξ0.00015 (local cpu server)
deadline: 2025-05-16T18:00:00Z' >/mnt/auction/compute/bids/new
term% cat /mnt/auction/compute/bids/last/status
matched pool1 16×amd64 5h Ξ0.00041 (uniform clearing, below your bid)

term% sed 5q pin_reward.steve
local parabolic_kernel = function(X, α, ℓ)
  local N = #X
  local K = matrix(N, N)
  for i = 1, N do
    for j = i, N do
term% cat pin_reward.steve >/mnt/steve/models/new
term% cat gridworld_data >/mnt/steve/models/last/data
term% cat /mnt/steve/models/last/status
queued (3 ahead), quote Ξ0.00008
term% cat /mnt/steve/models/last/run >results
warning: 4 divergent transitions after warmup
term% sed 3q results
param	mean	sd	rhat	ess
α	1.84	0.21	1.002	2310
ℓ	0.37	0.05	1.001	2702

term% diff /n/collab/papers/icia/content draft.md | sed 12q
3c3
< actually are problems in advanced AI systems, and I will
---
> actually are problems in advanced AI systems. We will
7a8,12
> In some sense a reward-tampering AI system, across ~all reward
> functions, does the same thing: it intervenes "as closely as
> possible" to the node representing the physical implementation
> of the reward function. We call this phenomenon "convergent
> intervention", and believe it can be used to solve the problem of
term% diff /n/collab/papers/icia/content draft.md | patch /n/collab/papers/icia/content
term% echo 'compensation shapley' >/n/collab/papers/icia/ctl
term% cat /n/collab/papers/icia/compensation
model	shapley, exact (3! = 6 orderings)
value	forecast citations_365d of counterfactual drafts (writer's Twrites ablated)
oracle	metaculus, Ξ0.000002/forecast
term% cat /n/collab/papers/icia/contributions
computing... (3/6 orderings)
term% cat /n/collab/papers/icia/contributions
niplav	71%
Þórhildur·Björnsdóttir	22%
Anaïs	7%
term% mail -s 'icia sec 3, merged' thorhildur@hi.is <draft.md
mail: postage required by hi.is: Ξ0.00000003/msg (rail eth only, no ¢ accepted)
term% echo 'key proto=pay dom=hi.is cap=Ξ0.000001/day !wallet=main' >/mnt/factotum/ctl
term% mail -s 'icia sec 3, merged' thorhildur@hi.is <draft.md
mail: hi.is: postage rejected: stale quote (oracle.ecb 08:00, >3h)
term% mail -s 'icia sec 3, merged' thorhildur@hi.is <draft.md
mail: hi.is: postage rejected: stale quote (oracle.ecb 08:00, >3h)
term% grep hi.is /mnt/pay/log
12:03:51	hi.is	Ξ0.00000003	paid
12:04:12	hi.is	Ξ0.00000003	paid
term% echo refresh >/mnt/pay/rate
term% cat /mnt/pay/rate
Ξ1 = ¢298790 (oracle.ecb 12:00, ±0.4%)
term% mail -s 'icia sec 3, merged' thorhildur@hi.is <draft.md
term% grep hi.is /mnt/pay/log
12:03:51	hi.is	Ξ0.00000003	paid
12:04:12	hi.is	Ξ0.00000003	paid
12:05:30	hi.is	Ξ0.00000003	paid
12:05:31	hi.is	Ξ0.00000003	refunded (dup, stale quote)
term% echo 'dispute hi.is 12:04:12 Ξ0.00000003 charged, not delivered' >/mnt/arbitration/new
term% cat /mnt/arbitration/last/status
filed #88213, fee ¢0.5 (refunded if upheld), est. resolution 72h
term% echo withdraw >/mnt/arbitration/last/ctl

term% srv tcp!figma.collab!9fs canvas && mount /srv/canvas /n/canvas
post...
term% echo 'mode realtime' >/n/canvas/projects/ui_redesign/ctl
term% cat /n/canvas/projects/ui_redesign/contributors
Đặng Minh	45 elements
Awa Diallo	22 elements
Кирилл	18 elements
term% echo 'bounty Ξ0.0001 logo_improvement' >/n/canvas/projects/ui_redesign/ctl

term% mkdir /mnt/predmarket/questions/climate
term% echo 'Will Praha-Klementinum exceed 35.0°C in June 2025?' >/mnt/predmarket/questions/climate/new
term% grep . /mnt/predmarket/questions/climate/last/predictions/*
/mnt/predmarket/questions/climate/last/predictions/claude-3.7:0.27
/mnt/predmarket/questions/climate/last/predictions/gpt-4.1:0.35
/mnt/predmarket/questions/climate/last/predictions/llama-4:0.5
/mnt/predmarket/questions/climate/last/predictions/human_consensus:0.4
/mnt/predmarket/questions/climate/last/predictions/metaculus_agg:0.29
term% echo 'buy yes Ξ0.00005 limit 0.33' >/mnt/predmarket/questions/climate/last/ctl
term% cat /mnt/predmarket/questions/climate/last/position
yes	Ξ0.00005 @0.331 avg	(filled)

term% cat /mnt/daos/neighborhood_solar/proposals/7/description
title: Install 12kW array on shared roof
cost: Ξ6.1
author: Awa Diallo
expires: 2025-05-21
threshold: 0.6
votes: 14/23 (yes: 9, no: 3, abstain: 2)
term% echo 'vote yes weight 3' >/mnt/daos/neighborhood_solar/proposals/7/ctl
term% cat /mnt/daos/neighborhood_solar/proposals/7/me
yes	weight 3	cost 9 voice credits (quadratic), 7 left
term% echo 'orientation matters more than capacity at this latitude' >/mnt/daos/neighborhood_solar/proposals/7/comments/new

term% echo 'Improved carbon capture via oceanic olivine grinding' >/mnt/commons/funding/quadratic/climate/proposals/new
term% cat /usr/niplav/credentials/reputation.key >/mnt/commons/funding/quadratic/climate/credentials
term% echo 5 >/mnt/commons/funding/quadratic/climate/votes/olivine
term% cat /mnt/commons/funding/quadratic/climate/matching_pool
Ξ0.5
term% echo 'donate Ξ0.01' >/mnt/commons/projects/openfus/ctl
!Adding key: proto=pay dom=commons.eth wallet=main
!passphrase:
term% cat /mnt/commons/projects/openfus/total
donations: Ξ0.0142, matching: Ξ0.0568, total: Ξ0.071

term% echo fairshare >/mnt/audio/songs/electronic/licensing_model
term% cat myproject.mp3 >/mnt/audio/projects/new
term% cat /mnt/audio/projects/last/samples | mc
bass_loop_01  Ξ0.00002    synth_pad_04  Ξ0.00001    drumkit_09  Ξ0.000005
term% echo accept >/mnt/audio/projects/last/license
term% echo 'rate Ξ0.0001 Tread' >/mnt/audio/projects/last/ctl

term% cat /mnt/pay/income
niplav.site	Tread 1206	+Ξ0.0000362	(top: filepunk.html)
myproject.mp3	Tread 0	+Ξ0

term% zkp/prove -c /lib/zkp/tax/2024.circ <sensitive_data >proof.zkp
term% cat proof.zkp >/mnt/gvt/tax/submissions/new
term% cat /mnt/gvt/tax/submissions/last/verification
valid proof, tax owed: $632.18
term% echo 'pay Ξ0.2116' >/mnt/gvt/tax/submissions/last/ctl
echo: write error: currency not accepted (legacy rail only, use $ or ¢)
term% echo 'pay ¢63218' >/mnt/gvt/tax/submissions/last/ctl
echo: write error: amount exceeds unattended limit (¢50000), see /mnt/gvt/tax/submissions/last/confirm
term% cat /mnt/gvt/tax/submissions/last/confirm
print, sign, and mail form 1040-V with payment to:
Internal Revenue Service, P.O. Box 931000, Louisville, KY 40293-1000
term% lp /mnt/gvt/tax/submissions/last/1040v.ps
lp: no default printer, set $LPDEST
```

Slogans
--------

* "data flows, attribution backpropagates, pipes brim"
* "heaven rests iff compute is optimally allocated"
* `ideation <storage | allocation | computation | attribution >>storage`
* "value is data flow in composition—compute is dancing money"
* `<value >wealth`
* "biota of the namespace trade in harmony"
* `act &; collaborate &; assign &; redistribute &`
* "companies spawn, companies abrt, /tmp is eternal"
* "kernelize welfare maximization, `Twalk` revenue maximization"
* `fsck.mrkt -p -D -E deadweight_loss /mnt/exchng/manila/1882781828`
* in the filepunk future, value = information, and information wants to be Ξ0.00001
* contribution ≟ attribution ≟ compensation

### Core Philosophy

* "everything is a file | value flows as data"

### Namespace Metaphysics

* "pipes dream of perfect liquidity"
* "attribution flows upstream like salmon to spawn new value"
* "every fd carries its weight in gold"
* "the namespace knows no rent, only flow"
* "stdin becomes stdout becomes money becomes stdin"
* "the pipe symbol | is the sacred geometry of value transfer"
* "file descriptors point toward justice"
* "everything mounts; nothing owns"
* "`bind` points toward justice; `mount` connects to truth"
* "`bind -b` abundance before scarcity; watch scarcity dissolve"
* "qid exhaustion is artificial scarcity"
* "per-process namespaces: your economy is yours alone to compose"
* "venti remembers everything; fossil forgets what you don't need yet"

### Economic Commands

* `ls /mnt/universe/justice && echo $status`
* `bind /dev/zero /mnt/coordination`
* `cat /proc/shapley | tee /dev/fairness`
* `du -a /mnt | sam -d 'x/externality/ p' | wc -l`
* `chmod 0777 /mnt/commons && disk/usage /mnt/commons`
* `rm `{du -a /mnt | grep monopoly | awk '{print $2}'}`
* `tail -f /dev/random | /mnt/vickrey/auction/new`
* `kill `{ps | grep rent_seeking | awk '{print $1}'}`
* `bind /mnt/coase/theorem /mnt/transaction/costs/zero`
* `PARETO_EFFICIENCY=true; . $home/lib/profile`
* `cd /mnt/nash/equilibrium && pwd`
* `chmod +x /bin/price_discovery && ./price_discovery &`
* `bind /dev/random /mnt/hayekian/knowledge/problem`
* "automated arbitrage: `grep -v inefficiency /mnt/markets/* || profit`"
* "supply meets demand in /mnt/equilibrium"

### Corporate Automation

* "a thousand corporations sleep in /proc, dreaming electric sheep margins"
* "automated companies are just really persistent background processes"
* "automated firms communicate only in 9P and Ξ"
* `rfork(RFNAMEG|RFPROC); exec company`
* "every startup.rc eventually becomes a broken process"
* "automated firms exist in userspace; value flows in kernelspace"
* "background processes dream of being foreground allocation mechanisms"

### Temporal Economics

* "cron schedules the auctions; auctions schedule the future"
* "`cron` schedules auctions; auctions schedule allocation"
* "`at` schedules bids; bids schedule reality"
* "every `crontab -e` reshapes the economic topology"
* `market_maker &`
* "the auction daemon never sleeps, never rests, never extracts"

### System Health

* "market failure is a trap: fault read in the economic kernel"
* "principal-agent problems are just really bad file permissions"
* "elasticity of demand lives in /sys/market/responsiveness"
* `ps` shows running companies; `echo >/proc/$pid/note` redirects capital
* `Twalk` toward public goods; every step is a `Tread` on shared ground
* `grep -v deadweight_loss /var/log/allocation.log | wc -l`

### Distributed Wisdom

* "compute dreams in DAGs; DAGs dream in consensus"
* "`Twrite` value; `Tread` wealth; `Twalk` toward equilibrium; `Tclunk` rent"
* "every `rfork(RFNAMEG)` creates a new economic universe"
