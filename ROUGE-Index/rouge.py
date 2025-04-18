import csv
from rouge_score import rouge_scorer

# The first element in each tuple is the original file and the second is the modified file.
FILE_PAIRS = [
    # ("original_filename.txt", "modified_filename.txt"),
    ("test1.txt", "test1out.txt"),
    ("test2.txt", "test2out.txt"),
]

"""
Some notes from RK
We mostly just care about the F1 scores being above a certain threshold.
Most people use 0.5 for summaries, but we might want to use 0.8 since it's tonal shifts.

rouge1 measures how many raw terms are the same.
rougeL measures how much of the flow/structure of the text is the same.
"""

def read_file_content(filename):

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return ""

def compute_rouge_scores(original_text, modified_text):

    # Create a ROUGE scorer that will compute ROUGE-1 and ROUGE-L.
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    scores = scorer.score(original_text, modified_text)
    return scores

def main():
    # Open both the CSV and the TXT file for output.
    with open("rouge-out.csv", "w", newline="", encoding="utf-8") as csvfile, \
         open("rouge-out.txt", "w", encoding="utf-8") as txtfile:
        csv_writer = csv.writer(csvfile)
        # Write header row for CSV.
        csv_writer.writerow(["Original File", "Modified File", "Metric", "Precision", "Recall", "F1"])

        # Process each file pair in the FILE_PAIRS list.
        for original_file, modified_file in FILE_PAIRS:
            txtfile.write(f"Processing pair: '{original_file}' vs '{modified_file}'\n")
            
            # Read contents from both files.
            original_text = read_file_content(original_file)
            modified_text = read_file_content(modified_file)
            
            # Skip processing if either file could not be read.
            if not original_text or not modified_text:
                txtfile.write("Skipping this pair due to missing file(s).\n")
                csv_writer.writerow([original_file, modified_file, "SKIPPED", "", "", ""])
                txtfile.write("-" * 50 + "\n")
                continue

            # Calculate the ROUGE scores for the text pair.
            rouge_scores = compute_rouge_scores(original_text, modified_text)
            txtfile.write("ROUGE Scores:\n")
            
            # Write scores for each metric.
            for metric, score in rouge_scores.items():
                score_line = (f"  {metric}: Precision = {score.precision:.4f}, "
                              f"Recall = {score.recall:.4f}, F1 = {score.fmeasure:.4f}\n")
                txtfile.write(score_line)
                csv_writer.writerow([
                    original_file,
                    modified_file,
                    metric,
                    f"{score.precision:.4f}",
                    f"{score.recall:.4f}",
                    f"{score.fmeasure:.4f}"
                ])
            txtfile.write("-" * 50 + "\n")

if __name__ == "__main__":
    main()
