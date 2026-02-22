// Brainfuck interpreter with step-by-step tape tracing.
// Reuses Snap/Exec from tm.rs — tape cells are u8, head is i64,
// state field stores the instruction pointer, inp_pos tracks ',' reads.
//
// Input is passed as a &[u8] slice; EOF returns 0.
// The '.' command is executed but output is discarded (not needed for metrics).

use crate::tm::{Snap, Exec};
use crate::shapley::Continuation;
use std::collections::HashMap;

pub struct BFProg {
	pub code:         Vec<u8>,
	pub bracket_map:  HashMap<usize, usize>,
}

impl BFProg {
	pub fn new(source: &str) -> Self
	{
		let code: Vec<u8> = source.bytes()
			.filter(|b| b"+-<>[],.".contains(b))
			.collect();
		let bracket_map = compute_brackets(&code);
		BFProg { code, bracket_map }
	}

	/// Like `run`, but also returns (in order) the tape positions read by '.'.
	/// Use this to find which cells hold the sorted output.
	pub fn run_traced(&self, input: &[u8], max_steps: usize)
		-> Option<(Exec, Vec<i64>)>
	{
		let mut tape: HashMap<i64, u8> = HashMap::new();
		let mut head: i64   = 0;
		let mut ip:   usize = 0;
		let mut inp:  usize = 0;
		let mut output_cells: Vec<i64> = Vec::new();

		let mut snaps = vec![mk_snap(&tape, head, ip, inp)];

		while ip < self.code.len() {
			if snaps.len() > max_steps { return None; }
			let cell = *tape.get(&head).unwrap_or(&0);
			match self.code[ip] {
				b'+' => { tape.insert(head, cell.wrapping_add(1)); }
				b'-' => { tape.insert(head, cell.wrapping_sub(1)); }
				b'>' => { head += 1; }
				b'<' => { head -= 1; }
				b'[' => { if cell == 0 { ip = self.bracket_map[&ip]; } }
				b']' => { if cell != 0 { ip = self.bracket_map[&ip]; } }
				b',' => {
					let v = input.get(inp).copied().unwrap_or(0);
					tape.insert(head, v);
					inp += 1;
				}
				b'.' => { output_cells.push(head); }
				_    => {}
			}
			ip += 1;
			snaps.push(mk_snap(&tape, head, ip, inp));
		}

		Some((Exec { snaps }, output_cells))
	}

	/// Run the program, recording a Snap after every instruction.
	/// Returns None if max_steps is exceeded (non-halting / too slow).
	pub fn run(&self, input: &[u8], max_steps: usize) -> Option<Exec>
	{
		let mut tape: HashMap<i64, u8> = HashMap::new();
		let mut head: i64   = 0;
		let mut ip:   usize = 0;
		let mut inp:  usize = 0;

		let mut snaps = vec![mk_snap(&tape, head, ip, inp)];

		while ip < self.code.len() {
			if snaps.len() > max_steps { return None; }

			let cell = *tape.get(&head).unwrap_or(&0);

			match self.code[ip] {
				b'+' => { tape.insert(head, cell.wrapping_add(1)); }
				b'-' => { tape.insert(head, cell.wrapping_sub(1)); }
				b'>' => { head += 1; }
				b'<' => { head -= 1; }
				b'[' => { if cell == 0 { ip = self.bracket_map[&ip]; } }
				b']' => { if cell != 0 { ip = self.bracket_map[&ip]; } }
				b',' => {
					let v = input.get(inp).copied().unwrap_or(0);
					tape.insert(head, v);
					inp += 1;
				}
				b'.' => {}
				_    => {}
			}

			ip += 1;
			snaps.push(mk_snap(&tape, head, ip, inp));
		}

		Some(Exec { snaps })
	}
}

/// Build a continuation closure for a BF program resuming from `snap`.
/// The closure accepts a dense tape slice over [lo, hi], splices it into
/// the tape, then runs the BF program from snap.state (ip) and snap.inp_pos
/// until halt, returning the byte at `target_cell`.
pub fn make_bf_continuation(
	prog:        &BFProg,
	snap:        &Snap,
	lo:          i64,
	target_cell: i64,
	input:       &[u8],
	max_steps:   usize,
) -> Continuation
{
	let base_tape = snap.tape.clone();
	let head      = snap.head;
	let ip0       = snap.state;
	let inp0      = snap.inp_pos;
	let input_vec = input.to_vec();
	let code      = prog.code.clone();
	let bmap      = prog.bracket_map.clone();

	Box::new(move |slice: &[u8]| {
		let mut tape = base_tape.clone();
		for (i, &v) in slice.iter().enumerate() {
			tape.insert(lo + i as i64, v);
		}

		let mut h   = head;
		let mut ip  = ip0;
		let mut inp = inp0;

		for _ in 0..max_steps {
			if ip >= code.len() { break; }
			let cell = *tape.get(&h).unwrap_or(&0);
			match code[ip] {
				b'+' => { tape.insert(h, cell.wrapping_add(1)); }
				b'-' => { tape.insert(h, cell.wrapping_sub(1)); }
				b'>' => { h += 1; }
				b'<' => { h -= 1; }
				b'[' => { if cell == 0 { ip = bmap[&ip]; } }
				b']' => { if cell != 0 { ip = bmap[&ip]; } }
				b',' => {
					let v = input_vec.get(inp).copied().unwrap_or(0);
					tape.insert(h, v);
					inp += 1;
				}
				b'.' => {}
				_    => {}
			}
			ip += 1;
		}

		*tape.get(&target_cell).unwrap_or(&0)
	})
}

fn mk_snap(tape: &HashMap<i64, u8>, head: i64, ip: usize, inp: usize) -> Snap
{
	Snap { tape: tape.clone(), head, state: ip, inp_pos: inp }
}

fn compute_brackets(code: &[u8]) -> HashMap<usize, usize>
{
	let mut map   = HashMap::new();
	let mut stack = Vec::new();
	for (i, &c) in code.iter().enumerate() {
		match c {
			b'[' => stack.push(i),
			b']' => {
				let j = stack.pop().expect("unmatched ] in BF program");
				map.insert(j, i);
				map.insert(i, j);
			}
			_ => {}
		}
	}
	assert!(stack.is_empty(), "unmatched [ in BF program");
	map
}

// ── Cristofani sorting programs ───────────────────────────────────────────────
// Source: http://brainfuck.org/  (c) 2016 Daniel B. Cristofani
// Input: raw bytes via ',', terminated by EOF (returns 0).
// Output: sorted bytes via '.'.  All three share the same I/O convention.

pub const BUBBLE_SORT: &str = "
>>,[>>,]<<[
[<<]>>>>[
<<[>+<<+>-]
>>[>+<<<<[->]>[<]>>-]
<<<[[-]>>[>+<-]>>[<<<+>>>-]]
>>[[<+>-]>>]<
]<<[>>+<<-]<<
]>>>>[.>>]
";

pub const INSERTION_SORT: &str = "
>+[
    <[
        [>>+<<-]>[<<+<[->>+[<]]>>>[>]<<-]<<<
    ]>>[<<+>>-]<[>+<-]>[>>]<,
]<<<[<+<]>[>.>]
";

pub const QUICKSORT: &str = "
>>+>>>>>,[>+>>,]>+[--[+<<<-]<[<+>-]<[<[->[<<<+>>>>+<-]<<[>>+>[->]<<[<]
<-]>]>>>+<[[-]<[>+<-]<]>[[>>>]+<<<-<[<<[<<<]>>+>[>>>]<-]<<[<<<]>[>>[>>
>]<+<<[<<<]>-]]+<<<]+[->>>]>>]>>[.>>>]
";
