mod tm;
mod metrics;
mod shapley;
mod less_naive;
mod bf;

use std::collections::HashMap;
use tm::{TM, Trans, Dir};
use metrics::{gou, gou_prime};
use less_naive::{kuo, ShapleyMode};
use bf::{BFProg, BUBBLE_SORT, INSERTION_SORT, QUICKSORT};
use less_naive::kuo_bf;

// ── demo TMs ─────────────────────────────────────────────────────────────────

/// Identity: reads tape[0], writes it back, halts.
fn tm_identity() -> TM
{
	let mut trans = HashMap::new();
	trans.insert((0, 0), Trans { write: 0, dir: Dir::R, next_state: 1 });
	trans.insert((0, 1), Trans { write: 1, dir: Dir::R, next_state: 1 });
	TM { trans, halt_state: 1, init_state: 0 }
}

/// Negation: flips tape[0], halts.
fn tm_not() -> TM
{
	let mut trans = HashMap::new();
	trans.insert((0, 0), Trans { write: 1, dir: Dir::R, next_state: 1 });
	trans.insert((0, 1), Trans { write: 0, dir: Dir::R, next_state: 1 });
	TM { trans, halt_state: 1, init_state: 0 }
}

/// Copy: tape[0] → tape[1], halts.
fn tm_copy() -> TM
{
	let mut trans = HashMap::new();
	trans.insert((0, 0), Trans { write: 0, dir: Dir::R, next_state: 1 });
	trans.insert((0, 1), Trans { write: 1, dir: Dir::R, next_state: 2 });
	trans.insert((1, 0), Trans { write: 0, dir: Dir::R, next_state: 3 });
	trans.insert((2, 0), Trans { write: 1, dir: Dir::R, next_state: 3 });
	TM { trans, halt_state: 3, init_state: 0 }
}

/// Same output as identity (returns tape[0]), but computes it by first
/// computing NOT and then NOT again — two extra steps, different trace.
/// 合 should be > identity vs identity, < identity vs not.
fn tm_double_not() -> TM
{
	let mut trans = HashMap::new();
	// step 0: flip bit, move R, state 1
	trans.insert((0, 0), Trans { write: 1, dir: Dir::R, next_state: 1 });
	trans.insert((0, 1), Trans { write: 0, dir: Dir::R, next_state: 1 });
	// step 1: move L, state 2
	trans.insert((1, 0), Trans { write: 0, dir: Dir::L, next_state: 2 });
	trans.insert((1, 1), Trans { write: 1, dir: Dir::L, next_state: 2 });
	// step 2: flip back, move R, halt
	trans.insert((2, 0), Trans { write: 1, dir: Dir::R, next_state: 3 });
	trans.insert((2, 1), Trans { write: 0, dir: Dir::R, next_state: 3 });
	TM { trans, halt_state: 3, init_state: 0 }
}

/// Direction-reversed copy: wanders left first, then does the same copy.
/// Should be highly correlated with tm_copy despite different tape trajectory.
fn tm_copy_reversed() -> TM
{
	let mut trans = HashMap::new();
	trans.insert((0, 0), Trans { write: 0, dir: Dir::L, next_state: 1 });
	trans.insert((0, 1), Trans { write: 1, dir: Dir::L, next_state: 1 });
	trans.insert((1, 0), Trans { write: 0, dir: Dir::R, next_state: 2 });
	trans.insert((1, 1), Trans { write: 1, dir: Dir::R, next_state: 2 });
	trans.insert((2, 0), Trans { write: 0, dir: Dir::R, next_state: 3 });
	trans.insert((2, 1), Trans { write: 1, dir: Dir::R, next_state: 4 });
	trans.insert((3, 0), Trans { write: 0, dir: Dir::R, next_state: 5 });
	trans.insert((4, 0), Trans { write: 1, dir: Dir::R, next_state: 5 });
	TM { trans, halt_state: 5, init_state: 0 }
}

// ── main ─────────────────────────────────────────────────────────────────────

fn main()
{
	let init: HashMap<i64, u8> = [(0, 1)].into_iter().collect();
	let max   = 1000;
	let gamma = 0.9;

	let tm_id  = tm_identity();
	let tm_neg = tm_not();
	let tm_dn  = tm_double_not();
	let tm_cp  = tm_copy();
	let tm_cpr = tm_copy_reversed();

	let ex_id  = tm_id.run(&init, max).expect("id halted");
	let ex_neg = tm_neg.run(&init, max).expect("neg halted");
	let ex_dn  = tm_dn.run(&init, max).expect("double_not halted");
	let ex_cp  = tm_cp.run(&init, max).expect("copy halted");
	let ex_cpr = tm_cpr.run(&init, max).expect("copy_rev halted");

	println!("=== Naïve metric 合 (gamma={gamma}) ===");
	println!("  id vs id         (expect 0):         {:.4}", gou(&ex_id,  &ex_id,  gamma));
	println!("  id vs not        (expect 1):          {:.4}", gou(&ex_id,  &ex_neg, gamma));
	println!("  id vs double_not (expect 0 < x < 1): {:.4}", gou(&ex_id,  &ex_dn,  gamma));
	println!("  copy vs cpr      (expect small):      {:.4}", gou(&ex_cp,  &ex_cpr, gamma));
	println!("  id vs not (with length penalty):      {:.4}", gou_prime(&ex_id, &ex_neg, gamma));
	println!();

	let mode_exact  = ShapleyMode::Exact;
	let mode_approx = ShapleyMode::Approx { n_samples: 200 };

	println!("=== Less-naïve metric 挧 (exact Shapley, gamma={gamma}) ===");
	println!("  id vs id         (expect 0):    {:.4}", kuo(&tm_id, &tm_id, &ex_id, &ex_id,  0, 0, gamma, &mode_exact, max));
	println!("  id vs not        (expect 1):    {:.4}", kuo(&tm_id, &tm_neg, &ex_id, &ex_neg, 0, 0, gamma, &mode_exact, max));
	println!("  id vs double_not (same output, diff trace): {:.4}",
		kuo(&tm_id, &tm_dn, &ex_id, &ex_dn, 0, 0, gamma, &mode_exact, max));
	println!("  copy vs cpr: {:.4}", kuo(&tm_cp, &tm_cpr, &ex_cp, &ex_cpr, 1, 1, gamma, &mode_exact, max));
	println!();

	println!("=== Less-naïve metric 挧 (approx Shapley, 200 samples, gamma={gamma}) ===");
	println!("  id vs id:         {:.4}", kuo(&tm_id, &tm_id,  &ex_id, &ex_id,  0, 0, gamma, &mode_approx, max));
	println!("  id vs not:        {:.4}", kuo(&tm_id, &tm_neg, &ex_id, &ex_neg, 0, 0, gamma, &mode_approx, max));
	println!("  id vs double_not: {:.4}", kuo(&tm_id, &tm_dn,  &ex_id, &ex_dn,  0, 0, gamma, &mode_approx, max));
	println!("  copy vs cpr:      {:.4}", kuo(&tm_cp, &tm_cpr, &ex_cp, &ex_cpr, 1, 1, gamma, &mode_approx, max));

	bf_demo(gamma);
}

fn bf_demo(gamma: f64)
{
	let bsort = BFProg::new(BUBBLE_SORT);
	let isort = BFProg::new(INSERTION_SORT);
	let qsort = BFProg::new(QUICKSORT);
	let max   = 500_000;

	// A few inputs: reverse-sorted, random-ish, already sorted.
	let inputs: &[(&str, &[u8])] = &[
		("reverse [5,4,3,2,1]", &[5, 4, 3, 2, 1]),
		("random  [3,1,4,1,5]", &[3, 1, 4, 1, 5]),
		("sorted  [1,2,3,4,5]", &[1, 2, 3, 4, 5]),
		("tiny    [2,1]",        &[2, 1]),
	];

	println!("=== BF sorting: naïve metric 合 (gamma={gamma}) ===");
	println!("  (lower = more logically correlated)\n");

	let mode_approx = ShapleyMode::Approx { n_samples: 10 };
	let gammas = [0.9_f64, 0.99, 0.999];

	// First pass: discover where each program writes its output on one input.
	let probe = inputs[0].1;
	let (_, ob) = bsort.run_traced(probe, max).expect("bubble");
	let (_, oi) = isort.run_traced(probe, max).expect("insertion");
	let (_, oq) = qsort.run_traced(probe, max).expect("quick");
	println!("  output cell positions (first input {:?}):", probe);
	println!("    bubble    '.': {:?}", ob);
	println!("    insertion '.': {:?}", oi);
	println!("    quicksort '.': {:?}", oq);
	// Use the first output cell for each program as b_pos.
	let bp_b = *ob.first().expect("bubble produced no output");
	let bp_i = *oi.first().expect("insertion produced no output");
	let bp_q = *oq.first().expect("quick produced no output");
	println!("  → using b_pos: bubble={bp_b}  insertion={bp_i}  quick={bp_q}");
	println!();

	for (label, input) in inputs {
		let (eb, _) = bsort.run_traced(input, max)
			.unwrap_or_else(|| panic!("bubble sort timed out on {label}"));
		let (ei, _) = isort.run_traced(input, max)
			.unwrap_or_else(|| panic!("insertion sort timed out on {label}"));
		let (eq, _) = qsort.run_traced(input, max)
			.unwrap_or_else(|| panic!("quicksort timed out on {label}"));

		println!("  input: {label}");
		println!("    steps  — bubble:{:6}  insertion:{:6}  quick:{:6}",
			eb.steps(), ei.steps(), eq.steps());
		println!("    合  bubble vs insertion : {:.4}", gou(&eb, &ei, gamma));
		println!("    合  bubble vs quick     : {:.4}", gou(&eb, &eq, gamma));
		println!("    合  insertion vs quick  : {:.4}", gou(&ei, &eq, gamma));
		println!("    合  bubble vs bubble    : {:.4}", gou(&eb, &eb, gamma));

		for &g in &gammas {
			let steps_covered = (1e-3_f64.ln() / g.ln()).ceil() as usize;
			println!("    挧(γ={g})  steps≤{steps_covered}  10 samples:");
			println!("      bubble vs insertion : {:.4}",
				kuo_bf(&bsort, &isort, &eb, &ei, input, input, bp_b, bp_i, g, &mode_approx, max));
			println!("      bubble vs quick     : {:.4}",
				kuo_bf(&bsort, &qsort, &eb, &eq, input, input, bp_b, bp_q, g, &mode_approx, max));
			println!("      insertion vs quick  : {:.4}",
				kuo_bf(&isort, &qsort, &ei, &eq, input, input, bp_i, bp_q, g, &mode_approx, max));
			println!("      bubble vs bubble    : {:.4}",
				kuo_bf(&bsort, &bsort, &eb, &eb, input, input, bp_b, bp_b, g, &mode_approx, max));
		}
		println!();
	}
}
