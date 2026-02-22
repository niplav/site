// Less-naive metric 挧 (kuo) from logical.md.
//
// 挧(p1, p2, b1, b2) = 1(b1≠b2) + 1 − max_{σ ∈ Sym} exp(−Σ γ^k · d(σ(ᖫ1_k), ᖫ2_k))
//
// Extension over the paper: γ discount added (matching 合) so that steps far
// from the output contribute negligibly.  With γ=0.9 only the last ~44 steps
// have weight > 0.1%, making the computation tractable for long BF programs.
//
// The permutation σ is found by the Hungarian algorithm (O(n^3)).

use crate::shapley::{shapley_exact, shapley_approx, Continuation};
use crate::tm::{Exec, Snap, TM};
use crate::bf::{BFProg, make_bf_continuation};
use rand::SeedableRng;
use rand::rngs::SmallRng;

/// Strategy for Shapley computation.
pub enum ShapleyMode {
	Exact,
	Approx { n_samples: usize },
}

// ── Continuation factories ────────────────────────────────────────────────────

fn make_tm_continuation(
	tm:          &TM,
	snap:        &Snap,
	lo:          i64,
	target_cell: i64,
	max_steps:   usize,
) -> Continuation
{
	let base_tape = snap.tape.clone();
	let head      = snap.head;
	let state     = snap.state;
	let trans     = tm.trans.clone();
	let halt      = tm.halt_state;

	Box::new(move |slice: &[u8]| {
		let mut tape = base_tape.clone();
		for (i, &v) in slice.iter().enumerate() {
			tape.insert(lo + i as i64, v);
		}
		let mut h = head;
		let mut s = state;
		for _ in 0..max_steps {
			if s == halt { break; }
			let sym = *tape.get(&h).unwrap_or(&0);
			if let Some(tr) = trans.get(&(s, sym)) {
				tape.insert(h, tr.write);
				h = match tr.dir {
					crate::tm::Dir::L => h - 1,
					crate::tm::Dir::R => h + 1,
				};
				s = tr.next_state;
			} else {
				break;
			}
		}
		*tape.get(&target_cell).unwrap_or(&0)
	})
}

// ── Shapley profile ───────────────────────────────────────────────────────────

/// Shapley value profile ᖫ(p, t, k) for step k.
///
/// `make_cont(snap)` returns a Continuation that runs the program from
/// the given snapshot to halt.
///
/// Edge case: at step 0, baseline == current (no preceding state) → all
/// Shapley values are 0.  Known limitation; see logical.md §"Remaining Problem".
fn shapley_profile_with(
	make_cont: &dyn Fn(&Snap) -> Continuation,
	exec:      &Exec,
	step:      usize,
	lo:        i64,
	hi:        i64,
	mode:      &ShapleyMode,
) -> Vec<f64>
{
	let snap = &exec.snaps[step];
	let prev = if step > 0 { &exec.snaps[step - 1] } else { snap };

	let current:  Vec<u8> = (lo..=hi).map(|i| snap.read(i)).collect();
	let baseline: Vec<u8> = (lo..=hi).map(|i| prev.read(i)).collect();

	let cont = make_cont(snap);

	match mode {
		ShapleyMode::Exact => shapley_exact(&baseline, &current, &cont),
		ShapleyMode::Approx { n_samples } => {
			let mut rng = SmallRng::from_entropy();
			shapley_approx(&baseline, &current, &cont, *n_samples, &mut rng)
		}
	}
}

// ── Core metric loop ──────────────────────────────────────────────────────────

/// Inner loop shared by kuo and kuo_bf.
/// `make_cont1/2` close over lo, target_cell, max_steps etc.
fn kuo_core(
	ex1:        &Exec,
	ex2:        &Exec,
	b1_pos:     i64,
	b2_pos:     i64,
	lo:         i64,
	hi:         i64,
	gamma:      f64,
	make_cont1: &dyn Fn(&Snap) -> Continuation,
	make_cont2: &dyn Fn(&Snap) -> Continuation,
	mode:       &ShapleyMode,
) -> f64
{
	let width = (hi - lo + 1) as usize;

	let b1 = ex1.output().read(b1_pos);
	let b2 = ex2.output().read(b2_pos);
	let bit_diff = if b1 != b2 { 1.0_f64 } else { 0.0 };

	let min_steps = ex1.steps().min(ex2.steps());
	let threshold = 1e-3; // skip steps where γ^k contributes < 0.1%

	let mut agg_cost: Vec<Vec<f64>> = vec![vec![0.0; width]; width];

	for k in 1..=min_steps {
		let w = gamma.powi(k as i32);
		if w < threshold { break; }

		let step1 = ex1.steps() - k;
		let step2 = ex2.steps() - k;

		let phi1 = shapley_profile_with(make_cont1, ex1, step1, lo, hi, mode);
		let phi2 = shapley_profile_with(make_cont2, ex2, step2, lo, hi, mode);

		for i in 0..width {
			for j in 0..width {
				agg_cost[i][j] += w * (phi1[i] - phi2[j]).powi(2);
			}
		}
	}

	// Normalise by (1-γ) so the sum converges to the time-average of d_k
	// regardless of γ.  Without this, exp(-sum) → 0 for any γ close to 1.
	let norm = 1.0 - gamma;
	let (min_cost, _) = hungarian(&agg_cost);
	bit_diff + 1.0 - (-(min_cost * norm)).exp()
}

// ── Public API ────────────────────────────────────────────────────────────────

/// 挧 for two Turing machines.
pub fn kuo(
	tm1:       &TM,
	tm2:       &TM,
	ex1:       &Exec,
	ex2:       &Exec,
	b1_pos:    i64,
	b2_pos:    i64,
	gamma:     f64,
	mode:      &ShapleyMode,
	max_steps: usize,
) -> f64
{
	let (l1, r1) = ex1.global_frontier();
	let (l2, r2) = ex2.global_frontier();
	let lo = l1.min(l2);
	let hi = r1.max(r2);

	let mc1 = |snap: &Snap| make_tm_continuation(tm1, snap, lo, b1_pos, max_steps);
	let mc2 = |snap: &Snap| make_tm_continuation(tm2, snap, lo, b2_pos, max_steps);

	kuo_core(ex1, ex2, b1_pos, b2_pos, lo, hi, gamma, &mc1, &mc2, mode)
}

/// 挧 for two BF programs.
pub fn kuo_bf(
	prog1:     &BFProg,
	prog2:     &BFProg,
	ex1:       &Exec,
	ex2:       &Exec,
	input1:    &[u8],
	input2:    &[u8],
	b1_pos:    i64,
	b2_pos:    i64,
	gamma:     f64,
	mode:      &ShapleyMode,
	max_steps: usize,
) -> f64
{
	let (l1, r1) = ex1.global_frontier();
	let (l2, r2) = ex2.global_frontier();
	let lo = l1.min(l2);
	let hi = r1.max(r2);

	let mc1 = |snap: &Snap| make_bf_continuation(prog1, snap, lo, b1_pos, input1, max_steps);
	let mc2 = |snap: &Snap| make_bf_continuation(prog2, snap, lo, b2_pos, input2, max_steps);

	kuo_core(ex1, ex2, b1_pos, b2_pos, lo, hi, gamma, &mc1, &mc2, mode)
}

// ── Hungarian algorithm ───────────────────────────────────────────────────────

fn hungarian(cost: &[Vec<f64>]) -> (f64, Vec<usize>)
{
	let n = cost.len();
	if n == 0 { return (0.0, vec![]); }

	let m   = cost[0].len().max(n);
	let inf = f64::INFINITY;

	let mut u   = vec![0.0_f64; n + 1];
	let mut v   = vec![0.0_f64; m + 1];
	let mut p   = vec![0usize; m + 1];
	let mut way = vec![0usize; m + 1];

	for i in 1..=n {
		p[0] = i;
		let mut j0     = 0usize;
		let mut minval = vec![inf; m + 1];
		let mut used   = vec![false; m + 1];

		loop {
			used[j0] = true;
			let i0        = p[j0];
			let mut delta = inf;
			let mut j1    = 0;

			for j in 1..=m {
				if !used[j] {
					let relax = if i0 > 0 && i0 <= n && j <= cost[i0 - 1].len() {
						cost[i0 - 1][j - 1]
					} else {
						inf
					} - u[i0] - v[j];
					if relax < minval[j] {
						minval[j] = relax;
						way[j]    = j0;
					}
					if minval[j] < delta {
						delta = minval[j];
						j1    = j;
					}
				}
			}

			for j in 0..=m {
				if used[j] { u[p[j]] += delta; v[j] -= delta; }
				else        { minval[j] -= delta; }
			}

			j0 = j1;
			if p[j0] == 0 { break; }
		}

		loop {
			p[j0] = p[way[j0]];
			j0    = way[j0];
			if j0 == 0 { break; }
		}
	}

	let mut assign = vec![0usize; n];
	for j in 1..=m {
		if p[j] > 0 && p[j] <= n { assign[p[j] - 1] = j - 1; }
	}

	let total: f64 = assign.iter().enumerate()
		.map(|(i, &j)| if j < cost[i].len() { cost[i][j] } else { 0.0 })
		.sum();

	(total, assign)
}
