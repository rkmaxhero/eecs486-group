#!/usr/bin/env bash

# Directory containing the raw output.txt files
TEST_DIR="TEST"
# Where to put the cleaned predictions
OUT_DIR="parsed_articles_neutralized"

# Create the output directory if it doesn't exist
mkdir -p "$OUT_DIR"

# Loop over every .txt file in TEST_DIR
for infile in "$TEST_DIR"/*.txt; do
  # Invoke cleanoutput.py: args are input file and output directory
  python3 cleanoutput.py "$infile" "$OUT_DIR"
  if [ $? -ne 0 ]; then
    echo "Warning: failed to clean $infile" >&2
    # continue to next file instead of exiting
  fi
done

echo "All files cleaned and written to $OUT_DIR"