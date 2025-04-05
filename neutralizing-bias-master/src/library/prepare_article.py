# Returns a TSV line with the following format:
# id_num    tokenized_text    tokenized_text    sentence    sentence    pos_tags_text    dep_tags_text

import spacy
from pytorch_pretrained_bert.tokenization import BertTokenizer
import logging
logging.getLogger().setLevel(logging.ERROR)


def convertToTsv(sentence: str, id_num: str = "00000001") -> str:
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)
    
    b_tokens = []          
    pos_tags_aligned = []  
    dep_tags_aligned = []  
    
    for token in doc:
        wordpieces = tokenizer.tokenize(token.text)
        b_tokens.extend(wordpieces)
        pos_tags_aligned.extend([token.pos_] * len(wordpieces))
        dep_tags_aligned.extend([token.dep_] * len(wordpieces))
    
    tokenized_text = " ".join(b_tokens)
    pos_tags_text = " ".join(pos_tags_aligned)
    dep_tags_text = " ".join(dep_tags_aligned)
    
    tsv_line = f"{id_num}\t{tokenized_text}\t{tokenized_text}\t{sentence}\t{sentence}\t{pos_tags_text}\t{dep_tags_text}\n"
    
    return tsv_line
