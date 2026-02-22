// Shapley value computation for tape cells.
//
// Players: cells in the active range [lo, hi].
// "Play" = the cell's actual value at this timestep.
// "Not play" (null action) = the cell's value at the *preceding* timestep.
//
// The characteristic function v(S) runs the TM from the modified tape
// until it halts, then reads target_bit from the output.

use rand::seq::SliceRandom;
use rand::Rng;

/// Run the TM from a given tape (dense slice over [lo,hi]) and return
/// the value of the output bit at position `target_bit` (0-indexed within
/// the slice).  This is the closure callers supply.
pub type Continuation = Box<dyn Fn(&[u8]) -> u8>;

/// Exact Shapley values via powerset enumeration — O(2^n * eval_cost).
/// `baseline[i]` = preceding-step value (null action).
/// `current[i]`  = this-step value (play action).
/// Returns one Shapley value per cell.
pub fn shapley_exact(
	baseline:    &[u8],
	current:     &[u8],
	cont:        &Continuation,
) -> Vec<f64>
{
	let n = baseline.len();
	let mut phi = vec![0.0_f64; n];

	for j in 0..n {
		let mut val = 0.0;
		// iterate over all subsets S ⊆ {0..n} \ {j}
		for mask in 0u64..(1 << (n - 1)) {
			// map mask bits to indices in {0..n}\{j}
			let s: Vec<usize> = (0..n)
				.filter(|&i| i != j)
				.enumerate()
				.filter(|(bit, _)| (mask >> bit) & 1 == 1)
				.map(|(_, i)| i)
				.collect();
			let s_size = s.len();

			// tape with S playing (but not j)
			let mut tape_s = baseline.to_vec();
			for &i in &s { tape_s[i] = current[i]; }

			// tape with S ∪ {j}
			let mut tape_sj = tape_s.clone();
			tape_sj[j] = current[j];

			let v_s  = cont(&tape_s)  as f64;
			let v_sj = cont(&tape_sj) as f64;

			let coeff = factorial(s_size) * factorial(n - s_size - 1);
			val += (coeff as f64 / factorial(n) as f64) * (v_sj - v_s);
		}
		phi[j] = val;
	}

	phi
}

/// Monte-Carlo Shapley approximation (Strumbelj & Kononenko, 2014).
/// Samples `n_samples` random permutations; O(n_samples * n * eval_cost).
pub fn shapley_approx(
	baseline:  &[u8],
	current:   &[u8],
	cont:      &Continuation,
	n_samples: usize,
	rng:       &mut impl Rng,
) -> Vec<f64>
{
	let n = baseline.len();
	let mut phi = vec![0.0_f64; n];
	let mut order: Vec<usize> = (0..n).collect();

	for _ in 0..n_samples {
		order.shuffle(rng);
		let mut tape = baseline.to_vec();

		for (pos, &j) in order.iter().enumerate() {
			// tape before j "joins"
			let v_without = cont(&tape) as f64;
			tape[j] = current[j];
			let v_with = cont(&tape) as f64;
			let _ = pos; // permutation position implicit via tape
			phi[j] += v_with - v_without;
		}
	}

	phi.iter_mut().for_each(|x| *x /= n_samples as f64);
	phi
}

fn factorial(n: usize) -> usize
{
	(1..=n).product()
}
