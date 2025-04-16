from rouge_score import rouge_scorer


# The first element in each tuple is the original file and the second is the modified file.
FILE_PAIRS = [
#   ("original_filename.txt", "modified_filename.txt"),
    ("test1.txt", "test1out.txt"),
    ("test2.txt", "test2out.txt"),
]
"""
Some notes from RK
We mostly  just care about the F1 scores being above a certain threshold. 
Most ppl use 0.5 for summaries but we might want to use 0.8 since it's tonal shifts.

rouge1 measures how many raw terms are the same
rougeL measures how much of the flow / structure of the text is the same.
"""

def read_file_content(filename):
    """
    Reads the content of a file.
    
    Args:
        filename (str): The path to the file.
        
    Returns:
        str: The content of the file. Returns an empty string if the file is not found.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return ""

def compute_rouge_scores(original_text, modified_text):
    """
    Computes ROUGE scores between two text strings.
    
    Args:
        original_text (str): Text from the original file.
        modified_text (str): Text from the modified file.
        
    Returns:
        dict: A dictionary with ROUGE score objects for each metric.
    """
    # Create a ROUGE scorer that will compute ROUGE-1 and ROUGE-L.
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    scores = scorer.score(original_text, modified_text)
    return scores

def main():
    # Process each file pair in the global FILE_PAIRS list.
    for original_file, modified_file in FILE_PAIRS:
        print(f"Processing pair: '{original_file}' vs '{modified_file}'")
        
        # Read contents from both files
        original_text = read_file_content(original_file)
        modified_text = read_file_content(modified_file)
        
        # Skip processing if either file could not be read.
        if not original_text or not modified_text:
            print("Skipping this pair due to missing file(s).\n")
            continue

        # Calculate the ROUGE scores for the text pair.
        rouge_scores = compute_rouge_scores(original_text, modified_text)
        
        # Print the ROUGE scores.
        print("ROUGE Scores:")
        for metric, score in rouge_scores.items():
            print(f"  {metric}: Precision = {score.precision:.4f}, Recall = {score.recall:.4f}, F1 = {score.fmeasure:.4f}")
        print("-" * 50)

if __name__ == "__main__":
    main()
