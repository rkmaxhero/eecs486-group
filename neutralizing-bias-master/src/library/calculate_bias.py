# Compares the predicted and gold distributions and sequences to compute bias scores.

import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging
logging.getLogger().setLevel(logging.ERROR)  # Suppress warnings


def computeBias(result: dict) -> dict:
    sentence1 = result["gold_seq"]
    sentence2 = result["pred_seq"]
    
    vectorizer = CountVectorizer(stop_words=stopwords.words('english'))
    vectors = vectorizer.fit_transform([sentence1, sentence2])
    cosine_sim = cosine_similarity(vectors[0:1], vectors[1:2])
    bias_score = cosine_sim[0][0]
   
    print(f"\nFilename: {result['id_num']}")
    print(f"Bias score: {bias_score:.4f}")

    return {
        "bias_score": bias_score,
    }