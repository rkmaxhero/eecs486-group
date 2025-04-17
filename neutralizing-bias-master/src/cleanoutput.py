#!/usr/bin/env python3
import re
import sys
import os

def extract_pred_seqs(path):
    """
    Reads the file at `path`, splits on lines of ####…,
    and for each block finds the 'PRED SEQ:' line,
    strips off the leading marker and trailing quote,
    and yields the raw prediction string.
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()

    # Split on any line consisting solely of '#' characters
    blocks = re.split(r'(?m)^[#]+\s*$', data)

    for blk in blocks:
        for line in blk.splitlines():
            if line.startswith("PRED SEQ:"):
                m = re.match(r"PRED SEQ:\s*b'(.*)'", line)
                if m:
                    yield m.group(1)
                else:
                    part = line.split("b'", 1)
                    if len(part) > 1:
                        yield part[1].rstrip("'")
                break

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_file> <output_dir>", file=sys.stderr)
        sys.exit(1)

    input_path  = sys.argv[1]
    output_dir  = sys.argv[2]

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Derive the output filename: same basename, but with .out extension
    base        = os.path.splitext(os.path.basename(input_path))[0]
    output_name = f"{base}.out"
    output_path = os.path.join(output_dir, output_name)

    # Extract and write predictions
    count = 0
    with open(output_path, 'w', encoding='utf-8') as out:
        for pred in extract_pred_seqs(input_path):
            out.write(pred + "\n")
            count += 1

    print(f"Wrote {count} predictions to {output_path}")

if __name__ == "__main__":
    main()
