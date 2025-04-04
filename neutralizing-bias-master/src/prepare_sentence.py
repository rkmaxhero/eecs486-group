#!/usr/bin/env python3
import sys
import os
import spacy
import argparse
from pytorch_pretrained_bert.tokenization import BertTokenizer

def create_test_file(sentence, output_file="bias_data/WNC/rk.test", mode="w", id_num=""):
    # Load BERT tokenizer and spaCy model
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)
    
    # Align tokenizations
    b_tokens = []          # BERT tokens list
    pos_tags_aligned = []  # aligned POS tags
    dep_tags_aligned = []  # aligned dependency tags
    
    for token in doc:
        wordpieces = tokenizer.tokenize(token.text)
        b_tokens.extend(wordpieces)
        pos_tags_aligned.extend([token.pos_] * len(wordpieces))
        dep_tags_aligned.extend([token.dep_] * len(wordpieces))
    
    tokenized_text = " ".join(b_tokens)
    pos_tags_text = " ".join(pos_tags_aligned)
    dep_tags_text = " ".join(dep_tags_aligned)
    
    # Use the provided id_num
    tsv_line = f"{id_num}\t{tokenized_text}\t{tokenized_text}\t{sentence}\t{sentence}\t{pos_tags_text}\t{dep_tags_text}\n"
    
    # Ensure directory exists and write the file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, mode) as f:
        f.write(tsv_line)
    
    print(f"Sentence formatted and written to {output_file} with id {id_num}")
    return output_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare test file for bias neutralization.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--sentence", type=str, help="A single sentence to process")
    group.add_argument("--file", type=str, default="bias_data/WNC/input-multi.txt", help="A file containing one sentence per line")
    parser.add_argument("--output", type=str, default="bias_data/WNC/input-single.test", help="Output file path")
    args = parser.parse_args()
    
    if args.sentence:
        create_test_file(args.sentence, args.output, id_num="00000001")
    else:
        counter = 1
        with open(args.file, "r") as infile:
            for line in infile:
                sentence = line.strip()
                if not sentence:
                    continue
                # create an 8-digit id e.g., "00000001", "00000002", etc.
                id_num = f"{counter:08d}"
                mode = "w" if counter == 1 else "a"
                create_test_file(sentence, args.output, mode=mode, id_num=id_num)
                counter += 1
