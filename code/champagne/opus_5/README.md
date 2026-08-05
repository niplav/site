Champagne Toasting Problem — Solver (Opus 5)
============================================

A from-scratch solver for the champagne toasting problem (see `notes.md`),
independent of `../champagne.jl`. Julia, no dependencies beyond `Optim`,
`JSON`.

	julia toast.jl -n 8 -t 300 -s 1 -o best_n8.json      # general search
	julia toast.jl -n 8 --radial -t 300                  # radial subfamily
	julia toast.jl --init ../best_n8_w8.json -t 300       # warm start
	julia verify.jl best_n*.json ../best_n8_w8.json      # independent check
	julia svg.jl best_n8.json > best_n8.svg              # static picture
	julia test_grad.jl                                   # gradient regression
	sh collect.sh                                        # collect+verify runs

Output JSON is the same format `anim/champagne/visualize_solution.py` eats
(`initial_positions`, `disk_trajectories`, `waypoints`, `metadata`); n=4 and
n=8 were rendered through it to check. Use the `manimtmp` venv, not `main` —
manim in `/usr/local/etc/uv/venvs/main` is broken on Python 3.14 (`pydub` →
`import pyaudioop` → `ModuleNotFoundError`):

	/usr/local/etc/uv/venvs/manimtmp/bin/manim -ql visualize_solution.py \
		ChampagneSolutionVisualization

Because `pin_touches` adds a waypoint per tangency and the visualizer spends a
flat 1.8 s per step, the videos get long (n=8: 74 s). `svg.jl` is the quick
look.

`collect.sh` expects raw run outputs in `out/`, `out2/`, `out3/`; those were
deleted after collecting, only the winners are kept.

Results
-------

Convention: `edge_length = 3`, `r = 0.3` (the newer of the two conventions in
`../*.json`; the older files use circumradius 3 instead and are not
comparable).

| n | previous best | this solver | change | lower bound | gap to bound |
|---|--------------|-------------|--------|-------------|--------------|
| 3 | 8.3310 | **8.313844** | −0.2% | 7.2000 | +15.5% |
| 4 | — | **14.570563** | — | 14.570563 | **+0.0%** |
| 5 | 28.4076 | **22.800744** | −19.7% | 21.2705 | +7.2% |
| 6 | 42.3978 | **33.643421** | −20.6% | 32.4000 | +3.8% |
| 7 | 70.9907 | **46.381189** | −34.7% | 42.9866 | +7.9% |
| 8 | 90.5040 | **61.218990** | −32.4% | 57.9150 | +5.7% |
| 9 | 127.9344 | **79.076238** | −38.2% | 72.3434 | +9.3% |

All solutions verified with `verify.jl`: every pair tangent to `1e-6`, worst
overlap `≤ 1e-12`, every disk exactly back home.

Note on comparability: re-checking the old files in continuous time, their
tangencies hold only to `~1e-5` (most files) or `~2e-3` (`best_n4_w6`,
`best_n5_w5`, `best_n7_w14`, `best_n8_w10` — in those, only 2–8 of the pairs get
within `1e-4` of tangency), which is presumably that solver's tolerance rather
than a real defect. Mine hold to `1e-13`. Since a loose tangency tolerance is
worth real length, the improvements above are slightly flattered — but not by
much: allowing myself a `2e-3` tolerance is worth `< 0.05%` of the tour.

Credit where due: in the older circumradius-3 convention, `../best_n4_w6.json`
(21.5917, versus a bound of 21.6 at `r=0.3`) already attains the n=4 optimum to
within its own tolerance, i.e. the previous solver did find the right n=4
structure — the `notes.md` write-up just describes a different one.

n=3 and n=4 are (essentially certainly) exact:

* n=3: `6·(edge−2r)/√3 = 8.3138436…` — all three meet in the middle as a
  triplet, which is what `notes.md` already says. Reached from ~10⁵ random
  starts, never beaten.
* n=4: `4·(edge·√2 − 2r) = 14.5705627…` — **provably optimal**, it meets the
  lower bound below. Note this is *not* the construction conjectured in
  `notes.md` (A,B,C triplet, then D pushes through). The optimum is: every
  disk moves in and out along its own diagonal, monotonically; on the way in
  all four pass through the tangent-square configuration (radius
  `2r/√2 ≈ 0.424`, all four adjacent pairs tangent at once); then the two
  diagonal pairs dip to mutual tangency in alternation, one pair retreating to
  radius `≥ √(4r²−r²) ≈ 0.52` while the other is at `r` — no disk ever has to
  backtrack, so total travel is exactly `Σᵢ 2(R − depthᵢ)` with
  `Σᵢ depthᵢ = 4r`.

Method
------

1. **Continuous-time constraints.** A trajectory is a polyline through `w`
   free waypoints (all disks stepping from waypoint `k` to `k+1`
   simultaneously) starting and ending at home. For a pair `(i,j)` the
   difference vector is affine within a time step, so
   `min_t ‖Δ(t)‖` has a closed form; let `m_ij` be its minimum over the whole
   tour. Then `m_ij < 2r` ⟺ overlap and `m_ij > 2r` ⟺ never touched, so
   feasibility is exactly the **equality** `m_ij = 2r` for every pair. Checking
   between waypoints rather than at them is what makes short tours
   representable: a single straight segment can settle many tangencies at once
   (see the comb initializer).
2. **Augmented Lagrangian + L-BFGS** on those `C(n,2)` equalities, plus a
   one-sided per-time-step overlap penalty (so a pair intersecting during
   several steps is pushed apart everywhere, not just at its worst moment).
   Analytic gradients throughout: `m_ij` is differentiated with the envelope
   theorem at its argmin `(k*, t*)`, checked against finite differences to
   `5e-8`. Drives constraint violation to `~1e-13` in ~0.5 s per polish.
3. **Constructive initialization ("comb").** Random inits jam for `n ≥ 6`: the
   tangency penalty pulls *all* pairs together simultaneously, which is
   geometrically impossible for `n ≥ 4` (at most 3 equal disks are mutually
   tangent). Instead, park all disks in a tight row (spacing exactly `2r`, so
   neighbours are already tangent), then let the leftmost remaining disk lift
   off by `2r` and travel in a **straight line at height exactly `2r` above
   the row**: as it passes over row disk `j` their distance is exactly `2r`, so
   one segment makes it touch *every* remaining disk. It then flies home and
   the next disk sweeps. That covers all `C(n,2)` pairs by construction (only
   the gather/return phases overlap, which the polish repairs). For n=8 the raw
   comb already scores ~80, i.e. better than the previous best, before any
   optimization.
4. Multi-start + basin hopping over comb/cluster/row/random inits.
5. **Post-processing.** `pin_touches` splits time steps at tangency times, so
   every touch lands exactly on a waypoint (length unchanged, but nicer
   animations and waypoint-only validators are then happy). This is why the
   reported `w` exceeds the requested one.

Lower bound
-----------

If `i` and `j` are tangent at some time, their displacements from home satisfy
`|aᵢ|+|aⱼ| ≥ d_ij − 2r`, and a closed path through `home+aᵢ` is at least
`2|aᵢ|` long, so `Tᵢ + Tⱼ ≥ 2(d_ij − 2r)`. For any fractional matching `y`
(`y_ij ≥ 0`, `Σⱼ y_ij ≤ 1`),

	Σᵢ Tᵢ ≥ Σ_ij y_ij (Tᵢ+Tⱼ) ≥ Σ_ij y_ij · 2(d_ij − 2r).

The longest chords of a regular n-gon form a perfect matching for even `n`
(take `y=1`) and a single n-cycle for odd `n` (take `y=1/2`); both give

	Σᵢ Tᵢ ≥ n·(d_max − 2r),	d_max = 2R·sin(π⌊n/2⌋/n).

This is what `lowbound` reports. It is tight for `n=2` and `n=4`, weak for
`n=3` (7.2 vs 8.3138), and within 4–10% of the best found for `n=5..9`.

Structural observations
-----------------------

* The exact optima for n=3, n=4 are **purely radial** (each disk moves in and
  out along its home ray). Searching only that subfamily (`--radial`,
  `n·w` unknowns instead of `2n·w`) recovers both exactly, but is clearly
  worse for larger n — n=8: 65.60 vs 61.22, n=9: 87.97 vs 79.08 — so optimal
  solutions are *not* radial for `n ≥ 5`. They are close to radial though:
  in the best n=8 tour the lateral excursions are `≤ 0.78` against `R ≈ 3.92`,
  and most disks dive to within `0.2` of the centre (some just past it). Drawn,
  the n≥5 solutions look like a star: a near-straight plunge to the middle, a
  brief scrum where the tangencies happen, a near-straight return.
* More waypoints do not help beyond a point: search-space size hurts more than
  the added freedom (n=4: w=9 → 14.57 but w=13 → 15.79; n=8: w=21 → 62.5 but
  w=25 → 64.4). `w = 1+3(n−2)+2`, the comb's own requirement, is a good
  default.

Caveats
-------

* Only n≤9, one geometry (`edge=3, r=0.3`), and the piecewise-linear +
  synchronized-waypoint family. Length is invariant under time
  reparametrization, but the *constraints* are not, so the synchronization
  convention (inherited from the JSON format) is a genuine restriction on
  which tours are representable at a given `w`.
* Everything except n=3 and n=4 is an upper bound from local search, not a
  proof.
