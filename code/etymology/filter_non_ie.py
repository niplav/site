#!/usr/bin/env python3

import csv
import sys
from collections import defaultdict
from pathlib import Path

# Indo-European language families/branches and representative languages
IE_LANGUAGES = {
	# Germanic
	'English', 'German', 'Dutch', 'Swedish', 'Norwegian', 'Danish', 'Icelandic',
	'Gothic', 'Old English', 'Middle English', 'Old Norse', 'Old High German',
	'Middle High German', 'Old Saxon', 'Middle Dutch', 'Afrikaans', 'Yiddish',
	'Frisian', 'West Frisian', 'Old Frisian', 'German Low German', 'Low German',
	'Middle Low German', 'Anglo-Norman', 'Scots', 'Proto-Germanic', 'Proto-West Germanic',
	'Proto-Norse', 'Old Dutch', 'Norwegian Bokmål', 'Norwegian Nynorsk',
	'Saterland Frisian', 'North Frisian', 'Elfdalian', 'Frankish', 'Lombardic',
	'Old Low German', 'East Frisian', 'Flemish', 'Luxembourgish', 'Pennsylvania German',
	'Plautdietsch', 'Westphalian', 'Alemannic German', 'Bavarian', 'Swiss German',
	'Austrian German', 'Old Saxon', 'Dalecarlian', 'Faroese', 'Old Icelandic',
	'Norn', 'Gutnish', 'Crimean Gothic', 'Vandalic', 'Burgundian',
	'West Flemish', 'East Flemish', 'Limburgish', 'Lombard',
	'Old Swedish', 'Old Danish', 'Old Gutnish', 'Early Scots', 'Middle Scots',
	'American English', 'Anglian Old English', 'Northern Middle English',
	'Swabian', 'Swiss High German', 'Upper Saxon', 'Rhine Franconian',
	'Palatine German', 'Vilamovian', 'Mòcheno', 'Cimbrian', 'Hunsrik',
	'Jersey Dutch', 'Volga German', 'Unserdeutsch', 'Dutch Low Saxon',
	'Westrobothnian', 'Zealandic',

	# Romance
	'Latin', 'French', 'Spanish', 'Italian', 'Portuguese', 'Romanian',
	'Catalan', 'Occitan', 'Sardinian', 'Vulgar Latin', 'Old French',
	'Middle French', 'Old Spanish', 'Old Italian', 'Old Portuguese',
	'Medieval Latin', 'New Latin', 'Late Latin', 'Old Latin',
	'Proto-Romance', 'Galician', 'Corsican', 'Friulian', 'Venetian',
	'Neapolitan', 'Sicilian', 'Asturian', 'Aragonese', 'Ladino',
	'Provençal', 'Franco-Provençal', 'Walloon', 'Picard', 'Norman',
	'Gallo', 'Aromanian', 'Moldovan', 'Dalmatian', 'Mozarabic',
	'Judaeo-Spanish', 'Rhaeto-Romance', 'Ladin', 'Romansh', 'Istro-Romanian',
	'Megleno-Romanian', 'Louisiana Creole French', 'Cajun French', 'Haitian Creole',
	'Ecclesiastical Latin', 'Biblical Latin', 'Renaissance Latin',
	'Old Northern French', 'Old Catalan', 'Old Occitan', 'Old Provençal',
	'Canadian French', 'Brazilian Portuguese', 'Mexican Spanish', 'Rioplatense Spanish',
	'Puerto Rican Spanish', 'United States Spanish', 'Switzerland French',
	'Acadian French', 'Mirandese', 'Tarantino', 'Piedmontese', 'Romagnol',
	'Romansch', 'Bourguignon', 'Extremaduran', 'Valencian', 'Istriot',
	'Jersey Norman',

	# Slavic
	'Russian', 'Polish', 'Czech', 'Slovak', 'Ukrainian', 'Belarusian',
	'Bulgarian', 'Serbo-Croatian', 'Serbian', 'Croatian', 'Bosnian',
	'Slovene', 'Slovenian', 'Macedonian', 'Old Church Slavonic',
	'Church Slavonic', 'Old East Slavic', 'Proto-Slavic',
	'Old Polish', 'Old Czech', 'Kashubian', 'Sorbian', 'Polabian',
	'Montenegrin', 'Rusyn', 'Lower Sorbian', 'Upper Sorbian',
	'Old Novgorodian', 'Silesian',

	# Celtic
	'Irish', 'Scottish Gaelic', 'Welsh', 'Breton', 'Cornish', 'Manx',
	'Old Irish', 'Middle Irish', 'Middle Welsh', 'Old Welsh',
	'Gaulish', 'Proto-Celtic', 'Cumbric', 'Pictish', 'Lepontic',
	'Goidelic', 'Primitive Irish', 'Old Breton', 'Middle Breton',
	'Middle Cornish', 'Old Cornish', 'Celtiberian', 'Transalpine Gaulish',
	'Proto-Brythonic', 'Shelta',  # Irish-based cant

	# Greek
	'Greek', 'Ancient Greek', 'Koine Greek', 'Medieval Greek',
	'Byzantine Greek', 'Mycenaean Greek', 'Proto-Hellenic',
	'Attic Greek', 'Doric Greek', 'Ionic Greek', 'Aeolic Greek',
	'Epic Greek',

	# Indo-Iranian
	'Sanskrit', 'Hindi', 'Urdu', 'Persian', 'Farsi', 'Kurdish',
	'Pashto', 'Bengali', 'Punjabi', 'Marathi', 'Gujarati',
	'Nepali', 'Sindhi', 'Assamese', 'Oriya', 'Avestan',
	'Old Persian', 'Middle Persian', 'Pahlavi', 'Parthian',
	'Vedic Sanskrit', 'Prakrit', 'Pali', 'Proto-Indo-Iranian',
	'Proto-Iranian', 'Proto-Indo-Aryan', 'Sogdian', 'Bactrian',
	'Scythian', 'Sarmatian', 'Ossetian', 'Balochi', 'Dari',
	'Tajik', 'Hindustani', 'Sinhala', 'Maldivian', 'Dhivehi',
	'Romani', 'Kashmiri', 'Odia', 'Sinhalese', 'Old Marathi',
	'Proto-Ossetic', 'Proto-Scythian', 'Old Ossetic', 'Old Iranian',
	'Old Median', 'Alanic', 'Angloromani',  # English + Romani mixed language

	# Baltic
	'Lithuanian', 'Latvian', 'Old Prussian', 'Proto-Baltic',
	'Samogitian', 'Latgalian', 'Old Lithuanian',

	# Armenian
	'Armenian', 'Old Armenian', 'Classical Armenian', 'Eastern Armenian',
	'Western Armenian', 'Middle Armenian',

	# Albanian
	'Albanian', 'Gheg Albanian', 'Tosk Albanian', 'Proto-Albanian',

	# Anatolian (extinct)
	'Hittite', 'Luwian', 'Lydian', 'Lycian', 'Palaic', 'Carian',
	'Phrygian',

	# Tocharian (extinct)
	'Tocharian A', 'Tocharian B',

	# Italic (extinct)
	'Oscan', 'Umbrian', 'Venetic', 'Sabine',

	# Proto-languages
	'Proto-Indo-European', 'Proto-Germanic', 'Proto-Indo-Iranian',
	'Proto-Italic', 'Proto-Balto-Slavic',

	# Other/Misc
	'Translingual',  # not really IE but should be excluded

	# Language family codes (ISO 639-5 and others)
	'ine',  # Indo-European
	'gem',  # Germanic
	'gmw',  # West Germanic
	'gmq',  # North Germanic
	'gme',  # East Germanic
	'roa',  # Romance
	'sla',  # Slavic
	'cel',  # Celtic
	'grk',  # Greek
	'iir',  # Indo-Iranian
	'inc',  # Indo-Aryan
	'ira',  # Iranian
	'bat',  # Baltic
	'ca',   # Catalan
	'da',   # Danish
	'ru',   # Russian
	'en',   # English
	'zls',  # South Slavic
}

def classify_lang(lang):
	"""Return True if language is Indo-European"""
	if not lang:
		return None
	return lang in IE_LANGUAGES

# Build etymology graph
def build_etymology_graph():
	"""Build a graph of term_id -> list of parent (term_id, lang, term)"""
	graph = defaultdict(list)
	term_info = {}  # term_id -> (lang, term)

	with open('etymology.csv', 'r', encoding='utf-8') as f:
		reader = csv.DictReader(f)
		for row in reader:
			term_id = row['term_id']
			lang = row['lang']
			term = row['term']
			related_term_id = row['related_term_id']
			related_lang = row['related_lang']
			related_term = row['related_term']
			reltype = row['reltype']

			# Store term info
			term_info[term_id] = (lang, term)

			# Build edges for derivational relationships
			if reltype in ['borrowed_from', 'derived_from', 'inherited_from',
			               'learned_borrowing_from', 'orthographic_borrowing_from',
			               'semantic_loan_from', 'unadapted_borrowing_from',
			               'has_root']:
				if related_term_id and related_lang:
					graph[term_id].append((related_term_id, related_lang, related_term))

	return graph, term_info

def trace_ultimate_origins(term_id, graph, term_info, visited=None, depth=0, max_depth=20):
	"""Recursively trace to ultimate origin languages. Returns set of (lang, term) tuples."""
	if visited is None:
		visited = set()

	# Prevent infinite loops
	if term_id in visited or depth > max_depth:
		return set()

	visited.add(term_id)

	# Get parents
	parents = graph.get(term_id, [])

	# If no parents, this is an ultimate origin
	if not parents:
		if term_id in term_info:
			lang, term = term_info[term_id]
			return {(lang, term)}
		return set()

	# Recursively trace all parents
	ultimate_origins = set()
	for parent_id, parent_lang, parent_term in parents:
		child_origins = trace_ultimate_origins(parent_id, graph, term_info, visited.copy(), depth+1, max_depth)
		if child_origins:
			ultimate_origins.update(child_origins)
		else:
			# Parent has no further etymology, it's an ultimate origin
			ultimate_origins.add((parent_lang, parent_term))

	return ultimate_origins

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

def process_unknown_words(freq_rank):
	"""Process unknown_words.txt and output frequency-sorted list"""
	unknown_path = Path('unknown_words.txt')
	if not unknown_path.exists():
		print("No unknown_words.txt found, skipping", file=sys.stderr)
		return

	unknown_words = []
	with open(unknown_path, 'r', encoding='utf-8') as f:
		for line in f:
			word = line.strip()
			if word:  # Skip empty lines
				unknown_words.append(word)

	# Sort by frequency if available, otherwise alphabetically
	if freq_rank:
		unknown_words.sort(key=lambda x: (freq_rank.get(x, float('inf')), x))
	else:
		unknown_words.sort()

	# Write to output file
	with open('unknown_words_sorted.txt', 'w', encoding='utf-8') as f:
		for word in unknown_words:
			f.write(f"{word}\n")

	print(f"Wrote {len(unknown_words)} unknown words to unknown_words_sorted.txt", file=sys.stderr)

def main():
	print("Building etymology graph...", file=sys.stderr)
	graph, term_info = build_etymology_graph()

	print("Loading frequency list...", file=sys.stderr)
	freq_rank = load_frequency_list()
	if freq_rank:
		print(f"Loaded {len(freq_rank)} words from frequency list", file=sys.stderr)
	else:
		print("No frequency list found, sorting alphabetically", file=sys.stderr)

	print("Finding English words and tracing origins...", file=sys.stderr)

	# Find all English words
	english_words = {}
	with open('etymology.csv', 'r', encoding='utf-8') as f:
		reader = csv.DictReader(f)
		for row in reader:
			if row['lang'] == 'English':
				term_id = row['term_id']
				term = row['term']
				if term_id not in english_words:
					english_words[term_id] = term

	# Trace ultimate origins for each English word
	non_ie_words = []

	for term_id, term in english_words.items():
		ultimate_origins = trace_ultimate_origins(term_id, graph, term_info)

		# Check if any ultimate origin is non-IE
		non_ie_origins = []
		for lang, orig_term in ultimate_origins:
			if not classify_lang(lang):
				non_ie_origins.append(f"{lang}:{orig_term}")

		if non_ie_origins:
			non_ie_words.append((term, sorted(non_ie_origins)))

	# Sort by frequency if available, otherwise alphabetically
	if freq_rank:
		non_ie_words.sort(key=lambda x: (freq_rank.get(x[0], float('inf')), x[0]))
	else:
		non_ie_words.sort(key=lambda x: x[0])

	print(f"Found {len(non_ie_words)} English words with non-IE ultimate origins\n", file=sys.stderr)

	# Output as CSV
	print("word,ultimate_non_ie_origins")
	for term, origins in non_ie_words:
		origins_str = '; '.join(origins)
		term_escaped = term.replace('"', '""')
		print(f'"{term_escaped}","{origins_str}"')

	# Process unknown words
	print("", file=sys.stderr)  # Blank line
	process_unknown_words(freq_rank)

if __name__ == '__main__':
	main()
