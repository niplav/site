// Naive metric 合 (gou) from logical.md
//
// 合(p1, p2, γ) = d(o1, o2) + 1 − exp(−Σ_{k=1}^{min(l1,l2)} γ^k · d(t1[l1-k], t2[l2-k]))
//
// We go *backwards* through the trace (from output toward start), with earlier
// steps discounted by higher powers of γ.

use crate::tm::Exec;

/// Hamming distance between two dense slices of equal length.
/// For unequal-length slices the shorter one is zero-padded.
pub fn hamming(a: &[u8], b: &[u8]) -> f64
{
	let len = a.len().max(b.len());
	let zero = &0u8;
	let diff = (0..len).filter(|&i| {
		a.get(i).unwrap_or(zero) != b.get(i).unwrap_or(zero)
	}).count();
	diff as f64
}

/// 合: naive logical-correlation metric.
///
/// `gamma` ∈ (0, 1]: tape-state discount factor.
/// Returns a value in [0, d(o1,o2) + 1); lower = more correlated.
pub fn gou(ex1: &Exec, ex2: &Exec, gamma: f64) -> f64
{
	let (lo, hi) = union_frontier(ex1, ex2);

	let o1 = ex1.output().slice(lo, hi);
	let o2 = ex2.output().slice(lo, hi);
	let out_dist = hamming(&o1, &o2);

	let l1 = ex1.steps(); // number of transitions
	let l2 = ex2.steps();
	let min_l = l1.min(l2);

	let mut sum = 0.0_f64;
	for k in 1..=min_l {
		// trace index going backwards: step l-k from the end
		let s1 = &ex1.snaps[l1 - k];
		let s2 = &ex2.snaps[l2 - k];
		let d  = hamming(&s1.slice(lo, hi), &s2.slice(lo, hi));
		sum   += gamma.powi(k as i32) * d;
	}

	out_dist + 1.0 - (-sum).exp()
}

/// Optional length-difference penalty from logical.md §"Different Trace Lengths".
pub fn gou_prime(ex1: &Exec, ex2: &Exec, gamma: f64) -> f64
{
	let base = gou(ex1, ex2, gamma);
	let diff = (ex1.steps() as i64 - ex2.steps() as i64).unsigned_abs() as f64;
	base + 2_f64.powf(diff)
}

fn union_frontier(ex1: &Exec, ex2: &Exec) -> (i64, i64)
{
	let (l1, r1) = ex1.global_frontier();
	let (l2, r2) = ex2.global_frontier();
	(l1.min(l2), r1.max(r2))
}
