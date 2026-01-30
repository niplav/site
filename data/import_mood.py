#!/usr/bin/env python3
"""
Import mood data from ~/down/mood.csv into the main data file,
avoiding duplicates and skipping entries with no actual mood data.
"""

import csv
from pathlib import Path

# File paths
HOME = Path.home()
SCRIPT_DIR = Path(__file__).parent  # data/ directory
DOWN_DIR = HOME / "down"

MOOD_FILE = SCRIPT_DIR / "mood.csv"
MOOD_IMPORT = DOWN_DIR / "mood.csv"


def read_existing_mood():
    """Read existing mood data and return set of dates for deduplication."""
    existing = set()
    with open(MOOD_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Use date as key for deduplication
            existing.add(row['date'])
    return existing


def import_mood_data():
    """Import mood data from ~/down/mood.csv."""
    print("Importing mood data...")

    existing_dates = read_existing_mood()
    imported = 0
    skipped_duplicate = 0
    skipped_no_data = 0

    # Read new entries to append
    new_rows = []
    with open(MOOD_IMPORT, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # The import file has different column names
            # "alarm","date","sad – happy","discontent – content","stressed – relaxed","bored – interested"
            # We need to transform to: "alarm","date","activity","happy","content","relaxed","horny"

            # Normalize date format (replace space with T)
            date = row['date'].replace(' ', 'T')

            # Check for duplicates
            if date in existing_dates:
                skipped_duplicate += 1
                continue

            # Map the mood values
            happy = row.get('sad – happy', '')
            content = row.get('discontent – content', '')
            relaxed = row.get('stressed – relaxed', '')
            horny = row.get('bored – interested', '')

            # Check if there's actual mood data (at least one of the main three)
            if not happy and not content and not relaxed:
                skipped_no_data += 1
                continue

            # Normalize alarm format too
            alarm = row['alarm'].replace(' ', 'T')

            new_row = {
                'alarm': alarm,
                'date': date,
                'activity': '',  # Import file doesn't have activity
                'happy': happy,
                'content': content,
                'relaxed': relaxed,
                'horny': horny
            }

            new_rows.append(new_row)
            imported += 1

    # Sort new rows by date before appending (chronological order)
    new_rows.sort(key=lambda x: x['date'])

    # Append only new rows to the file
    if new_rows:
        with open(MOOD_FILE, 'a', newline='\n') as f:
            fieldnames = ['alarm', 'date', 'activity', 'happy', 'content', 'relaxed', 'horny']
            writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='\n')
            writer.writerows(new_rows)

    print(f"  Imported: {imported}")
    print(f"  Skipped (duplicate): {skipped_duplicate}")
    print(f"  Skipped (no data): {skipped_no_data}")


if __name__ == '__main__':
    import_mood_data()
    print("\nDone!")
