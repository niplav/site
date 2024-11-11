use std::collections::VecDeque;

#[derive(Debug, Clone, PartialEq)]
pub enum Instruction {
    IncrPointer,    // >
    DecrPointer,    // <
    IncrByte,       // +
    DecrByte,       // -
    Output,         // .
    Input,          // ,
    JumpForward,    // [
    JumpBackward,   // ]
}

#[derive(Debug)]
pub struct Program {
    instructions: Vec<Instruction>,
    instruction_pointer: usize,
    data_pointer: usize,
    tape: VecDeque<u8>,
    bracket_map: Vec<usize>,  // Maps opening brackets to closing brackets
}

impl Program {
    pub fn new(code: &str) -> Result<Self, String> {
        let mut instructions = Vec::new();
        let mut bracket_stack = Vec::new();
        let mut bracket_map = Vec::new();

        // Parse instructions
        for c in code.chars() {
            let instruction = match c {
                '>' => Some(Instruction::IncrPointer),
                '<' => Some(Instruction::DecrPointer),
                '+' => Some(Instruction::IncrByte),
                '-' => Some(Instruction::DecrByte),
                '.' => Some(Instruction::Output),
                ',' => Some(Instruction::Input),
                '[' => {
                    bracket_stack.push(instructions.len());
                    Some(Instruction::JumpForward)
                },
                ']' => {
                    if let Some(open_pos) = bracket_stack.pop() {
                        while bracket_map.len() <= instructions.len() {
                            bracket_map.push(0);
                        }
                        bracket_map[open_pos] = instructions.len();
                        Some(Instruction::JumpBackward)
                    } else {
                        return Err("Unmatched closing bracket".to_string());
                    }
                },
                _ => None,
            };

            if let Some(inst) = instruction {
                instructions.push(inst);
            }
        }

        if !bracket_stack.is_empty() {
            return Err("Unmatched opening bracket".to_string());
        }

        Ok(Program {
            instructions,
            instruction_pointer: 0,
            data_pointer: 0,
            tape: VecDeque::from(vec![0; 30000]),  // Standard tape size
            bracket_map,
        })
    }

    pub fn step(&mut self) -> Option<(Vec<u8>, Option<char>)> {
        if self.instruction_pointer >= self.instructions.len() {
            return None;
        }

        let mut output = None;

        match self.instructions[self.instruction_pointer] {
            Instruction::IncrPointer => {
                self.data_pointer += 1;
                if self.data_pointer >= self.tape.len() {
                    self.tape.push_back(0);
                }
            },
            Instruction::DecrPointer => {
                if self.data_pointer > 0 {
                    self.data_pointer -= 1;
                }
            },
            Instruction::IncrByte => {
                self.tape[self.data_pointer] = self.tape[self.data_pointer].wrapping_add(1);
            },
            Instruction::DecrByte => {
                self.tape[self.data_pointer] = self.tape[self.data_pointer].wrapping_sub(1);
            },
            Instruction::Output => {
                output = Some(self.tape[self.data_pointer] as char);
            },
            Instruction::Input => {
                // For now, just input 0
                self.tape[self.data_pointer] = 0;
            },
            Instruction::JumpForward => {
                if self.tape[self.data_pointer] == 0 {
                    self.instruction_pointer = self.bracket_map[self.instruction_pointer];
                }
            },
            Instruction::JumpBackward => {
                if self.tape[self.data_pointer] != 0 {
                    // Find matching opening bracket
                    for (i, bracket_end) in self.bracket_map.iter().enumerate() {
                        if *bracket_end == self.instruction_pointer {
                            self.instruction_pointer = i;
                            break;
                        }
                    }
                }
            },
        }

        self.instruction_pointer += 1;

        // Return current tape state and any output
        Some((self.tape.iter().cloned().collect(), output))
    }

    pub fn run_to_completion(&mut self) -> Vec<(Vec<u8>, Option<char>)> {
        let mut states = Vec::new();
        while let Some(state) = self.step() {
            states.push(state);
        }
        states
    }

    // Helper function to get current tape state
    pub fn get_tape_state(&self) -> Vec<u8> {
        self.tape.iter().cloned().collect()
    }
}

// Previous Instruction and Program implementations remain the same...
// [Previous code from brainfuck-interpreter up until the end of the Program impl]

/// Compute string distance between two tape states
fn tape_distance(tape1: &[u8], tape2: &[u8]) -> f64 {
    // Using Hamming distance normalized by the longer tape length
    let max_len = tape1.len().max(tape2.len());
    let mut diff = 0;

    for i in 0..max_len {
        let byte1 = tape1.get(i).unwrap_or(&0);
        let byte2 = tape2.get(i).unwrap_or(&0);
        if byte1 != byte2 {
            diff += 1;
        }
    }

    diff as f64
}

/// Compute logical correlation between two Brainfuck programs
pub fn logical_correlation(prog1: &str, prog2: &str, gamma: f64) -> Result<f64, String> {
    let mut p1 = Program::new(prog1)?;
    let mut p2 = Program::new(prog2)?;

    // Run both programs to completion and collect all tape states
    let states1 = p1.run_to_completion();
    let states2 = p2.run_to_completion();

    // Extract final outputs (last tape states)
    let output1 = states1.last()
        .map(|(tape, _)| tape.clone())
        .ok_or("Program 1 produced no states")?;
    let output2 = states2.last()
        .map(|(tape, _)| tape.clone())
        .ok_or("Program 2 produced no states")?;

    // Calculate d(o₁, o₂)
    let output_distance = tape_distance(&output1, &output2);

    // Calculate the sum of discounted trace differences
    let min_steps = states1.len().min(states2.len());
    let mut trace_diff_sum = 0.0;

    for k in 1..=min_steps {
        let state1_idx = states1.len() - k;
        let state2_idx = states2.len() - k;

        let distance = tape_distance(
            &states1[state1_idx].0,
            &states2[state2_idx].0
        );

        trace_diff_sum += gamma.powi(k as i32) * distance;
    }

    // Apply the formula: 合(p₁, p₂, γ) = d(o₁, o₂) + 0.5 - 1/(2 + Σ γᵏ·d(t₁(l₁-k), t₂(l₂-k)))
    let correlation = output_distance + 0.5 - 1.0 / (2.0 + trace_diff_sum);

    Ok(correlation)
}

// Example usage and tests
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_identical_programs() -> Result<(), String> {
        // Program that outputs 'A'
        let prog = "++++++++++ ++++++++++ ++++++++++ ++++++++++ ++++++++++ +++++ .";
        let correlation = logical_correlation(prog, prog, 0.9)?;
        assert!((correlation - 0.0).abs() < 1e-10);
        Ok(())
    }

    #[test]
    fn test_similar_programs() -> Result<(), String> {
        // Two programs that output 'A', but second one uses a loop
        let prog1 = "++++++++++ ++++++++++ ++++++++++ ++++++++++ ++++++++++ +++++ .";
        let prog2 = "++++++[>++++++++<-]>+++++.";
        let correlation = logical_correlation(prog1, prog2, 0.9)?;
        // These programs should have some correlation but not be identical
        assert!(correlation > 0.0);
        assert!(correlation < 1.0);
        Ok(())
    }

    #[test]
    fn test_different_programs() -> Result<(), String> {
        // First program outputs 'A', second outputs 'B'
        let prog1 = "++++++++++ ++++++++++ ++++++++++ ++++++++++ ++++++++++ +++++ .";
        let prog2 = "++++++++++ ++++++++++ ++++++++++ ++++++++++ ++++++++++ ++++++ .";
        let correlation = logical_correlation(prog1, prog2, 0.9)?;
        // These programs should have low correlation
        assert!(correlation > 0.5);
        Ok(())
    }
}

// ... [Previous code for Program and logical_correlation remains the same] ...

fn main() {
    // Three different ways to output 'A' (ASCII 65):

    let prog1 = "++++++++++ ++++++++++ ++++++++++ ++++++++++ ++++++++++ +++++ .";

    // Method 2: Multiplication using a loop
    let prog2 = "++++++[>++++++++<-]>+++++.";

    // Method 3: Decrement from 0 (wraps to 255) until we reach 65
    let prog3 = "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------.";

    println!("Comparing three different programs that output 'A':");

    // Compare all pairs with different discount factors to see the effect
    let gammas = [0.5, 0.7, 0.9];

    for &gamma in &gammas {
        println!("\nWith discount factor γ = {}", gamma);

        match logical_correlation(prog1, prog2, gamma) {
            Ok(corr) => println!("Correlation between direct addition and loop method: {:.6}", corr),
            Err(e) => println!("Error comparing prog1 and prog2: {}", e),
        }

        match logical_correlation(prog1, prog3, gamma) {
            Ok(corr) => println!("Correlation between direct addition and decrement method: {:.6}", corr),
            Err(e) => println!("Error comparing prog1 and prog3: {}", e),
        }

        match logical_correlation(prog2, prog3, gamma) {
            Ok(corr) => println!("Correlation between loop method and decrement method: {:.6}", corr),
            Err(e) => println!("Error comparing prog2 and prog3: {}", e),
        }

        // Also test self-correlation for verification
        match logical_correlation(prog1, prog1, gamma) {
            Ok(corr) => println!("Self-correlation of direct addition method: {:.6}", corr),
            Err(e) => println!("Error in self-correlation: {}", e),
        }
    }

    // Print out the execution traces for comparison
    println!("\nExecution traces:");

    let mut programs = vec![
        ("Direct addition", Program::new(prog1).unwrap()),
        ("Loop method", Program::new(prog2).unwrap()),
        ("Decrement wrap", Program::new(prog3).unwrap()),
    ];
}
