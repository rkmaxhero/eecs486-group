import os
import sys
import csv
import subprocess
import argparse
from transformers import BertTokenizer

def tokenize_text(text, tokenizer):
    """Tokenize text using BERT tokenizer"""
    return " ".join(tokenizer.tokenize(text))

def create_tsv_file(input_file, output_file, has_pairs=False):
    """
    Create a properly formatted TSV file for bias neutralization
    
    Args:
        input_file: Path to input file
        output_file: Path to output TSV file
        has_pairs: If True, input file has tab-separated pairs of biased and neutral text
                   If False, input file has only biased text
    """
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter='\t')
        
        for i, line in enumerate(infile):
            line = line.strip()
            if not line:
                continue
                
            if has_pairs:
                # Input file has pairs of biased and neutral text
                parts = line.split('\t')
                if len(parts) != 2:
                    print(f"Warning: Line {i+1} does not have exactly two tab-separated fields. Skipping.")
                    continue
                    
                biased_text = parts[0].strip()
                neutral_text = parts[1].strip()
            else:
                # Input file has only biased text
                biased_text = line
                # For inference, we can use the same text as target (will be ignored)
                neutral_text = line
            
            # Create unique ID
            example_id = f"custom_{i+1}"
            
            # Tokenize texts
            tokenized_biased = tokenize_text(biased_text, tokenizer)
            tokenized_neutral = tokenize_text(neutral_text, tokenizer)
            
            # Write to TSV
            writer.writerow([
                example_id,
                tokenized_biased,
                tokenized_neutral,
                biased_text,
                neutral_text
            ])
    
    print(f"Created initial TSV file at {output_file}")
    return output_file

def add_pos_tags(tsv_file, output_file):
    """Add POS tags using add_tags.py script"""
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                               "neutralizing-bias-master", "harvest", "add_tags.py")
    
    if not os.path.exists(script_path):
        print(f"Error: add_tags.py script not found at {script_path}")
        sys.exit(1)
    
    try:
        command = f"python {script_path} {tsv_file} > {output_file}"
        subprocess.run(command, shell=True, check=True)
        print(f"Added POS tags and saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running add_tags.py: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Prepare data for bias neutralization")
    parser.add_argument("input_file", help="Path to input file with text to process")
    parser.add_argument("--output_dir", default="./data", help="Directory to save processed files")
    parser.add_argument("--has_pairs", action="store_true", 
                        help="If set, input file has tab-separated pairs of biased and neutral text")
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Path for intermediate and final files
    initial_tsv = os.path.join(args.output_dir, "initial_data.tsv")
    final_tsv = os.path.join(args.output_dir, "data_with_pos.tsv")
    
    # Create initial TSV file
    create_tsv_file(args.input_file, initial_tsv, args.has_pairs)
    
    # Add POS tags
    add_pos_tags(initial_tsv, final_tsv)
    
    print("\nData preparation complete!")
    print(f"Final data file: {final_tsv}")
    print("You can now use this file with the neutralizing bias model.")

if __name__ == "__main__":
    main()