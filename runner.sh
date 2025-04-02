# Process a file with biased text (one sentence per line)
python prepare_bias_data.py my_biased_text.txt --output_dir ./my_data

# For paired data (biased text and neutral text pairs separated by tabs)
python prepare_bias_data.py my_paired_data.txt --output_dir ./my_data --has_pairs

# Neutralize a single sentence
python neutralize_sentence.py --sentence "This terrible article shows the president's dishonest approach to climate policy."

# Process multiple sentences from a file
python neutralize_sentence.py --file my_sentences.txt

# Specify a custom model checkpoint
python neutralize_sentence.py --sentence "..." --model_checkpoint /path/to/model_checkpoint.ckpt

# Get detailed output
python neutralize_sentence.py --sentence "..." --verbose