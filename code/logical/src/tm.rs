// Binary-tape Turing machine matching the formalization in logical.md
// Tape cells are 0 or 1; tape is infinite (modeled as a HashMap).

use std::collections::HashMap;

pub type Symbol = u8; // 0 or 1
pub type State  = usize;

#[derive(Clone, Copy, Debug, PartialEq)]
pub enum Dir { L, R }

#[derive(Clone, Debug)]
pub struct Trans {
	pub write:      Symbol,
	pub dir:        Dir,
	pub next_state: State,
}

pub struct TM {
	// transitions[(state, read)] = Trans
	pub trans:        HashMap<(State, Symbol), Trans>,
	pub halt_state:   State,
	pub init_state:   State,
}

/// One snapshot of the TM/BF configuration.
#[derive(Clone, Debug)]
pub struct Snap {
	/// Sparse tape: missing cells are implicitly 0.
	pub tape:    HashMap<i64, Symbol>,
	pub head:    i64,
	pub state:   State,
	/// Input buffer position (always 0 for TMs; tracks ',' reads in BF).
	pub inp_pos: usize,
}

impl Snap {
	pub fn read(&self, pos: i64) -> Symbol
	{
		*self.tape.get(&pos).unwrap_or(&0)
	}

	/// Left- and rightmost visited cell.
	pub fn frontier(&self) -> (i64, i64)
	{
		if self.tape.is_empty() {
			return (self.head, self.head);
		}
		let l = *self.tape.keys().min().unwrap();
		let r = *self.tape.keys().max().unwrap();
		(l.min(self.head), r.max(self.head))
	}

	/// Dense slice over [lo, hi] (inclusive), missing = 0.
	pub fn slice(&self, lo: i64, hi: i64) -> Vec<Symbol>
	{
		(lo..=hi).map(|i| self.read(i)).collect()
	}
}

/// Full execution trace: trace[0] is the initial config, trace.last() is halt.
pub struct Exec {
	pub snaps: Vec<Snap>,
}

impl Exec {
	pub fn output(&self) -> &Snap
	{
		self.snaps.last().unwrap()
	}

	pub fn steps(&self) -> usize
	{
		self.snaps.len() - 1
	}

	/// Union frontier across all snapshots.
	pub fn global_frontier(&self) -> (i64, i64)
	{
		let mut lo = i64::MAX;
		let mut hi = i64::MIN;
		for s in &self.snaps {
			let (l, r) = s.frontier();
			lo = lo.min(l);
			hi = hi.max(r);
		}
		(lo, hi)
	}
}

impl TM {
	pub fn run(&self, init_tape: &HashMap<i64, Symbol>, max_steps: usize)
		-> Option<Exec>
	{
		let mut snap = Snap {
			tape:    init_tape.clone(),
			head:    0,
			state:   self.init_state,
			inp_pos: 0,
		};
		let mut snaps = vec![snap.clone()];

		for _ in 0..max_steps {
			if snap.state == self.halt_state {
				return Some(Exec { snaps });
			}
			let sym = snap.read(snap.head);
			let tr  = self.trans.get(&(snap.state, sym))?;
			snap.tape.insert(snap.head, tr.write);
			snap.head  = match tr.dir { Dir::L => snap.head - 1, Dir::R => snap.head + 1 };
			snap.state = tr.next_state;
			snaps.push(snap.clone());
		}

		// Timed out without halting.
		None
	}
}
