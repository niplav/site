[home](./index.md)
-------------------

*author: niplav/Claude 3.7 Sonnet/Claude 4 Sonnet/Claude 4.6 Opus, created: 2025-08-19, modified: 2026-02-18, language: english, status: in progress, importance: 1, confidence: fiction*

> __Fileservers × mechanism design × sub-cent microtransactions. A
personal æsthetic.__
>  
>  
> __¢|⋈__

`filepunk`
============

Co-written with a several Claudes, and a hefty amount of [steering
bits](https://gwern.net/blog/2025/good-ai-samples) from my side, some
vetting. Still too clean/uniform for a real command line history.

<br><br><br><br><br>

<!--TODO: Something with sending an email for the price of 0.01 cent, leak of payment infra clashes-->

```
% srv tcp!claude.vigila!9p claude
% mount -c /srv/claude /mnt/claude
% echo 'key proto=eth dom=claude.vigila !secret='^$APIKEY | auth/factotum -g ''
% echo $user `{cat /mnt/claude/auth/challenge} >/mnt/claude/auth/response
% cat /usr/niplav/vigila/CLAUDE.md >/mnt/claude/proj/conf/sysprompt
% chmod 0775 /mnt/claude/proj/usr/niplav/vigila
% venti/copy -f /dev/sdC0/fossil -t tcp!venti.tarsnap.net!venti /usr/niplav/vigila
% echo 'topup Ξ0.008' >/mnt/claude/billing/ctl
% lc /mnt/claude/ctx
1_icia  2_forecasting  3_vigila  4_stevemod
% cat /usr/niplav/vigila/TODO.txt >/mnt/claude/ctx/3_vigila/in
% cat /mnt/claude/ctx/3_vigila/out
reviewed TODO items. 3 blocked on venti migration, 1 ready...

% srv tcp!nytimes.com!9p nytimes
% mount /srv/nytimes /mnt/nytimes
% echo 'rate ¢0.2 Tread' >/mnt/nytimes/ctl
% mkdir /mnt/payments/auto
% mkdir /mnt/payments/auto/arxiv
% echo 'rate ¢0.2 Tread' >/mnt/payments/auto/arxiv/ctl
% echo 'cap $2 month' >/mnt/payments/auto/arxiv/ctl
% srv tcp!netflix.com!9p netflix
% mount /srv/netflix /mnt/netflix
% tail -f /mnt/netflix/shows/labyrinths_on_cyprus/s05e01 |
	tee /dev/video &
% cat /mnt/payments/streaming_meter
¢0.06/min

% srv tcp!collab.local!9p collab
% mount /srv/collab /mnt/collab
% echo 'rate Ξ0.000001 Twrite Þórhildur·Björnsdóttir' >/mnt/collab/papers/icia/ctl

% echo 'SELECT avg_temp FROM weather.historical WHERE city=''Prague'' AND year>2020' >/mnt/datamarket/queries/new
% cat /mnt/datamarket/queries/last/cost
Ξ0.00004
% cat /mnt/datamarket/queries/last/result
2021	11.3
2022	12.1
2023	11.8
2024	12.4
2025	12.7

% cat `{du -a /usr/niplav/papers/icia | grep '\.c$' | awk '{print $2}'} |
	sam -d 'x/TODO[^\n]*/ p'
TODO: test with >3 reward functions
TODO: verify convergence on gridworld_4x4
TODO: handle splinter case in causal graph
% echo 'generate test cases for these TODOs' >>/mnt/claude/ctx/1_icia/in
Twrite /mnt/claude/ctx/1_icia/in: limit exceeded by 1.4kb (Ξ0.00003 remaining)
% echo 'topup Ξ0.001' >/mnt/claude/billing/ctl
% echo 'generate test cases for these TODOs' >>/mnt/claude/ctx/1_icia/in

% srv -e 'tcp!generalcomputecorp.com!9p' gpu
mount: tcp!generalcomputecorp.com!9p: auction closed, next window 14:00
% srv -e 'tcp!gpu.market.gl!9p' gpu
% mount -c /srv/gpu /mnt/gpu
% echo 'bid model=h200 max=Ξ0.0003/min' >/mnt/gpu/auction/ctl
% cat /usr/niplav/papers/icia/train_pin.lua >/mnt/gpu/sessions/new
% cat /mnt/gpu/sessions/last/pricing
Ξ0.00018/min (4 bidders)

% echo 'pools:
  pool0: {resource: 32×amd64, access: immediate, bid: Ξ0.002/4h}
  pool1: {resource: 16×amd64, access: <30min, bid: Ξ0.0015/6h}
  pool2: {resource: 8×arm64, access: <2h, bid: Ξ0.0008/8h}
batna: Ξ0.0005 (local compute fallback)
deadline: 2025-05-16T18:00:00Z' >/mnt/auction/compute/bids/new
% cat /mnt/auction/compute/bids/last/status
matched pool1 16×amd64 5h Ξ0.00135 (cleared below pool0 bid)

% cat /usr/niplav/papers/icia/pin_reward.steve | rlvnt 1
local parabolic_kernel = function(X, α, ℓ)
  local N = #X
  local K = matrix(N, N)
  for i = 1, N do
    for j = i, N do
[…]
  reward_hat ~ parabolic_gp(X_obs, α, ℓ, σ_pin)
  y_intervene ~ bernoulli_logit(intervention_logit)
}
% cat /usr/niplav/papers/icia/pin_reward.steve >/mnt/steve/models/new
% cat /usr/niplav/papers/icia/gridworld_data >/mnt/steve/models/last/data
% cat /mnt/steve/models/last/cost
Ξ0.00008
% cat /mnt/steve/models/last/run >results

% diff /mnt/collab/papers/icia/content /usr/niplav/papers/icia/draft.md | head -12
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
> To solve this would be to solve the problem of [environmental
> goals](tcp!arbital.com/p/environmental_goals/!https).
% diff /mnt/collab/papers/icia/content /usr/niplav/papers/icia/draft.md | patch /mnt/collab/papers/icia/content
% echo shapley >/mnt/collab/papers/icia/compensation_model
% cat /mnt/collab/papers/icia/contributions
computing... (3/7 permutations)
% cat /mnt/collab/papers/icia/contributions
niplav: 71%, Þórhildur: 22%, Anaïs: 7%

% srv tcp!figma.collab!9p canvas
% mount /srv/canvas /mnt/canvas
% echo 'mode realtime' >/mnt/canvas/projects/ui_redesign/ctl
% cat /mnt/canvas/projects/ui_redesign/contributors
Đặng Minh: 45 elements, Awa Diallo: 22 elements, Кирилл: 18 elements
% echo 'bounty Ξ0.0001 logo_improvement' >/mnt/canvas/projects/ui_redesign/ctl

% mkdir /mnt/predmarket/questions/climate
% echo 'Will Prague exceed 35°C in June 2025?' >/mnt/predmarket/questions/climate/new
% echo 'direction yes stake Ξ0.00005' >/mnt/predmarket/questions/climate/last/ctl
% lc /mnt/predmarket/questions/climate/last/predictions
claude_model  gpt4_model  human_consensus  llama3_model  metaculus_aggregate

% cat /mnt/daos/neighborhood_solar/proposals/7/description
title: Install 12kW array on shared roof
cost: Ξ0.015
author: Awa Diallo
expires: 2025-05-21
threshold: 0.6
votes: 14/23 (yes: 9, no: 3, abstain: 2)
% echo 'vote yes weight 3' >/mnt/daos/neighborhood_solar/proposals/7/ctl
% echo 'orientation matters more than capacity at this latitude' >/mnt/daos/neighborhood_solar/proposals/7/comments/new

% echo 'Improved carbon capture via oceanic olivine grinding' >/mnt/commons/funding/quadratic/climate/proposals/new
% cat /usr/niplav/credentials/reputation.key >/mnt/commons/funding/quadratic/climate/credentials
% echo 5 >/mnt/commons/funding/quadratic/climate/votes/olivine
% cat /mnt/commons/funding/quadratic/climate/matching_pool
Ξ0.5
% echo 'donate Ξ0.01' >/mnt/commons/projects/openfus/ctl
password:
% cat /mnt/commons/projects/openfus/total
donations: Ξ0.0142, matching: Ξ0.0568, total: Ξ0.071

% echo fairshare >/mnt/audio/songs/electronic/licensing_model
% cat myproject.mp3 >/mnt/audio/projects/new
% cat /mnt/audio/projects/last/samples | mc
bass_loop_01  Ξ0.00002    synth_pad_04  Ξ0.00001    drumkit_09  Ξ0.000005
% echo accept >/mnt/audio/projects/last/license
% echo 'rate Ξ0.0001 Tread' >/mnt/audio/projects/last/ctl

% cat sensitive_data | /mnt/zkp/generate tax_computation >proof.zkp
% cat proof.zkp >/mnt/gvt/tax/submissions/new
% cat /mnt/gvt/tax/submissions/last/verification
valid proof, tax owed: $632.18
% echo 'pay Ξ0.32' >/mnt/gvt/tax/submissions/last/ctl
Twrite: currency not accepted (legacy rail only, use $ or ¢)
% echo 'pay $632.18 via /mnt/pay/convert' >/mnt/gvt/tax/submissions/last/ctl
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
