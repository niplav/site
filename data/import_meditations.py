#!/usr/bin/env python3
"""
Import meditation data from ~/down/meditations.csv into the main data file,
avoiding duplicates.
"""

import csv
from datetime import datetime
from pathlib import Path

# File paths
HOME = Path.home()
SCRIPT_DIR = Path(__file__).parent  # data/ directory
DOWN_DIR = HOME / "down"

MED_FILE = SCRIPT_DIR / "meditations.csv"
MED_IMPORT = DOWN_DIR / "meditations.csv"


def read_existing_meditations():
    """Read existing meditation data and return set of meditation start times."""
    existing = set()
    with open(MED_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Use meditation_start as key for deduplication
            existing.add(row['meditation_start'])
    return existing


def import_meditation_data():
    """Import meditation data from ~/down/meditations.csv."""
    print("Importing meditation data...")

    existing_times = read_existing_meditations()
    imported = 0
    skipped_duplicate = 0

    # Find the highest existing ID
    with open(MED_FILE, 'r') as f:
        reader = csv.DictReader(f)
        max_id = max(int(row['_id']) for row in reader)

    # Read new entries to append
    new_rows = []
    with open(MED_IMPORT, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Transform from Medativo export format:
            # "ID","M_DATE","M_DURATION","M_TITLE","M_NOTE","M_RATING"
            # To existing format:
            # _id,meditation_start,meditation_end,meditation_duration,mindfulness_rating,concentration_rating,comment

            # Parse timestamp (milliseconds since epoch)
            timestamp_ms = int(row['M_DATE'])
            timestamp_s = timestamp_ms / 1000
            med_start = datetime.fromtimestamp(timestamp_s).astimezone()

            # Duration in seconds
            duration_ms = int(row['M_DURATION'])
            duration_s = duration_ms / 1000

            # Calculate end time
            med_end = datetime.fromtimestamp(timestamp_s + duration_s).astimezone()

            # Format timestamps
            start_str = med_start.strftime('%Y-%m-%dT%H:%M:%S%z')
            # Insert colon in timezone offset
            start_str = start_str[:-2] + ':' + start_str[-2:]

            # Check for duplicates
            if start_str in existing_times:
                skipped_duplicate += 1
                continue

            # Parse M_NOTE field: "mindfulness,concentration,comment"
            m_note = row['M_NOTE']
            mindfulness = ''
            concentration = ''
            comment = ''

            if m_note:
                parts = m_note.split(',', 2)  # Split on first 2 commas only
                if len(parts) >= 1:
                    mindfulness = parts[0].strip()
                if len(parts) >= 2:
                    concentration = parts[1].strip()
                if len(parts) >= 3:
                    comment = parts[2].strip()

            # Keep all entries, even without ratings

            end_str = med_end.strftime('%Y-%m-%dT%H:%M:%S%z')
            end_str = end_str[:-2] + ':' + end_str[-2:]

            max_id += 1
            new_row = {
                '_id': str(max_id),
                'meditation_start': start_str,
                'meditation_end': end_str,
                'meditation_duration': str(int(duration_s)),
                'mindfulness_rating': mindfulness,
                'concentration_rating': concentration,
                'comment': comment
            }

            new_rows.append(new_row)
            imported += 1

    # Sort new rows by start time before appending (chronological order)
    new_rows.sort(key=lambda x: x['meditation_start'])

    # Append only new rows to the file
    if new_rows:
        with open(MED_FILE, 'a', newline='\n') as f:
            fieldnames = ['_id', 'meditation_start', 'meditation_end', 'meditation_duration',
                         'mindfulness_rating', 'concentration_rating', 'comment']
            writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='\n')
            writer.writerows(new_rows)

    print(f"  Imported: {imported}")
    print(f"  Skipped (duplicate): {skipped_duplicate}")


if __name__ == '__main__':
    import_meditation_data()
    print("\nDone!")
