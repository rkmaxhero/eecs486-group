import re
import argparse
import codecs
from rouge_score import rouge_scorer

def parse_output(file_path):
    golds, preds = [], []
    with open(file_path, encoding='utf-8') as f:
        lines = f.read().splitlines()
    for i, line in enumerate(lines):
        if line.startswith("GOLD SEQ"):
            m = re.search(r"b'(.*)'", line)
            if not m: 
                continue
            gold_raw = m.group(1)
            golds.append(codecs.decode(gold_raw, 'unicode_escape'))
            # find the next PRED SEQ
            for j in range(i+1, len(lines)):
                if lines[j].startswith("PRED SEQ"):
                    m2 = re.search(r"b'(.*)'", lines[j])
                    if m2:
                        pred_raw = m2.group(1)
                        preds.append(codecs.decode(pred_raw, 'unicode_escape'))
                    break
    return golds, preds

def main():
    parser = argparse.ArgumentParser(
        description="Compute ROUGE between GOLD and PRED sequences in output.txt"
    )
    parser.add_argument(
        "-i","--input", default="TEST/output.txt",
        help="Path to output.txt"
    )
    parser.add_argument(
        "-m","--metrics", nargs="+",
        default=["rouge1","rougeL"], help="ROUGE metrics"
    )
    args = parser.parse_args()

    golds, preds = parse_output(args.input)
    scorer = rouge_scorer.RougeScorer(args.metrics, use_stemmer=True)

    # accumulate and average
    agg = {m: {'p':0,'r':0,'f':0} for m in args.metrics}
    n = len(golds)
    for g, p in zip(golds, preds):
        scores = scorer.score(g, p)
        for m, s in scores.items():
            agg[m]['p'] += s.precision
            agg[m]['r'] += s.recall
            agg[m]['f'] += s.fmeasure

    print(f"Computed ROUGE over {n} sentence pairs")
    for m in args.metrics:
        print(f"{m}: P={agg[m]['p']/n:.4f}  R={agg[m]['r']/n:.4f}  F1={agg[m]['f']/n:.4f}")

if __name__ == "__main__":
    main()