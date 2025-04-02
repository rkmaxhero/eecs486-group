import os
import sys
import tempfile
import subprocess
import argparse
from transformers import BertTokenizer

def prepare_sentence(sentence, temp_dir):
    """Prepare a single sentence for bias neutralization"""
    # Create a temporary file with the sentence
    input_file = os.path.join(temp_dir, "input.txt")
    with open(input_file, "w", encoding="utf-8") as f:
        f.write(sentence)
    
    # Prepare the data
    prepare_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prepare_bias_data.py")
    initial_tsv = os.path.join(temp_dir, "temp_data.tsv")
    tagged_tsv = os.path.join(temp_dir, "temp_data_tagged.tsv")
    
    # Create initial TSV file
    subprocess.run([
        "python", prepare_script, 
        input_file, 
        "--output_dir", temp_dir
    ], check=True)
    
    return os.path.join(temp_dir, "data_with_pos.tsv")

def neutralize_sentence(sentence, model_checkpoint=None, verbose=False):
    """
    Neutralize bias in a given sentence
    
    Args:
        sentence: The potentially biased input sentence
        model_checkpoint: Path to model checkpoint (optional)
        verbose: Whether to print detailed output
    
    Returns:
        Neutralized sentence
    """
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Prepare the sentence in the correct format
        data_file = prepare_sentence(sentence, temp_dir)
        
        # Set up paths
        project_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.join(project_dir, "neutralizing-bias-master", "src")
        
        # Default checkpoint path if not provided
        if not model_checkpoint:
            model_checkpoint = os.path.join(project_dir, "neutralizing-bias-master", "src", "model.ckpt")
        
        # Path for output
        output_file = os.path.join(temp_dir, "neutralized_output.txt")
        
        # Run inference
        cmd = [
            "python", os.path.join(src_dir, "joint", "inference.py"),
            "--test", data_file,
            "--bert_full_embeddings", "--debias_weight", "1.3",
            "--token_softmax", "--pointer_generator", "--coverage",
            "--working_dir", temp_dir,
            "--inference_output", output_file,
            "--checkpoint", model_checkpoint
        ]
        
        if verbose:
            print(f"Running command: {' '.join(cmd)}")
            process = subprocess.run(cmd, cwd=src_dir)
        else:
            process = subprocess.run(cmd, cwd=src_dir, 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE)
        
        # Parse results
        if os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                if lines:
                    # Format varies, but typically model output is in the last part of each line
                    # or after a separator like "|||"
                    result_line = lines[0].strip()
                    if "|||" in result_line:
                        return result_line.split("|||")[-1].strip()
                    return result_line
        
        # If we couldn't find the output
        if verbose:
            print("Warning: Could not find neutralized output")
        return "Error: Could not neutralize text"

def main():
    parser = argparse.ArgumentParser(description="Neutralize bias in text")
    parser.add_argument("--sentence", help="Sentence to neutralize")
    parser.add_argument("--file", help="File containing sentences to neutralize")
    parser.add_argument("--model_checkpoint", 
                       help="Path to model checkpoint (default: ./neutralizing-bias-master/src/model.ckpt)")
    parser.add_argument("--verbose", action="store_true", help="Print detailed output")
    
    args = parser.parse_args()
    
    if not args.sentence and not args.file:
        print("Please provide either a sentence or a file containing sentences to neutralize")
        sys.exit(1)
    
    if args.sentence:
        # Process a single sentence
        neutralized = neutralize_sentence(args.sentence, args.model_checkpoint, args.verbose)
        print("\nOriginal:   ", args.sentence)
        print("Neutralized:", neutralized)
    
    elif args.file:
        # Process multiple sentences from a file
        if not os.path.exists(args.file):
            print(f"Error: File {args.file} does not exist")
            sys.exit(1)
        
        with open(args.file, "r", encoding="utf-8") as f:
            sentences = [line.strip() for line in f if line.strip()]
        
        print(f"Processing {len(sentences)} sentences...")
        
        for i, sentence in enumerate(sentences):
            neutralized = neutralize_sentence(sentence, args.model_checkpoint, args.verbose)
            print(f"\n[{i+1}/{len(sentences)}]")
            print("Original:   ", sentence)
            print("Neutralized:", neutralized)

if __name__ == "__main__":
    main()