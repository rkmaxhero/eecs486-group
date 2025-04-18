#!/usr/bin/env python3

import os
import sys
import re
import argparse

SEP = "#" * 80

def extract_pred_seqs(path):
    """Yield each predicted sequence (without the b'…' wrapper) from the given file."""
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    blocks = re.split(r'(?m)^[#]+\s*$', data)
    for blk in blocks:
        for line in blk.splitlines():
            if line.startswith("PRED SEQ:"):
                # try full capture
                m = re.match(r"PRED SEQ:\s*b'(.*)'", line)
                if m:
                    yield m.group(1)
                else:
                    # fallback split
                    parts = line.split("b'", 1)
                    if len(parts) == 2:
                        yield parts[1].rstrip("'")
                break

def main():
    parser = argparse.ArgumentParser(
        description="Batch-clean all TEST/*.txt into parsed_articles_neutralized/"
    )
    parser.add_argument(
        "-i","--input-dir",
        default=os.path.join(os.path.dirname(__file__), "TEST"),
        help="Directory containing .txt output files"
    )
    parser.add_argument(
        "-o","--output-dir",
        default=os.path.join(os.path.dirname(__file__), "parsed_articles_neutralized"),
        help="Where to write cleaned prediction files"
    )
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    for fname in sorted(os.listdir(args.input_dir)):
        if not fname.lower().endswith(".txt"):
            continue
        inp = os.path.join(args.input_dir, fname)
        base, _ = os.path.splitext(fname)
        out = os.path.join(args.output_dir, f"{base}.out")

        count = 0
        with open(out, 'w', encoding='utf-8') as outf:
            for pred in extract_pred_seqs(inp):
                outf.write(pred + "\n")
                count += 1

        print(f"[{count:2d}] → {fname}  cleaned → {os.path.basename(out)}")

if __name__ == "__main__":
    main()