#!/usr/bin/env python3

from pathlib import Path

def load_frequency_list():
	"""Load word frequency rankings from en_full.txt"""
	freq_path = Path('en_full.txt')
	if not freq_path.exists() or freq_path.stat().st_size == 0:
		return {}

	freq_rank = {}
	with open(freq_path, 'r', encoding='utf-8') as f:
		for rank, line in enumerate(f, start=1):
			parts = line.strip().split()
			if parts:
				word = parts[0]  # First column is the word
				freq_rank[word] = rank
	return freq_rank

def main():
	print("Loading frequency list...")
	freq_rank = load_frequency_list()
	if freq_rank:
		print(f"Loaded {len(freq_rank)} words from frequency list")
	else:
		print("No frequency list found, sorting alphabetically")

	unknown_path = Path('unknown_words.txt')
	if not unknown_path.exists():
		print("Error: unknown_words.txt not found")
		return

	unknown_words = []
	with open(unknown_path, 'r', encoding='utf-8') as f:
		for line in f:
			word = line.strip()
			if word:  # Skip empty lines
				unknown_words.append(word)

	print(f"Loaded {len(unknown_words)} unknown words")

	# Sort by frequency if available, otherwise alphabetically
	if freq_rank:
		unknown_words.sort(key=lambda x: (freq_rank.get(x, float('inf')), x))
	else:
		unknown_words.sort()

	# Write to output file
	with open('unknown_words_sorted.txt', 'w', encoding='utf-8') as f:
		for word in unknown_words:
			f.write(f"{word}\n")

	print(f"Wrote {len(unknown_words)} unknown words to unknown_words_sorted.txt")

if __name__ == '__main__':
	main()
