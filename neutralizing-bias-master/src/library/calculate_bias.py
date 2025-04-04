import numpy as np
from scipy.special import softmax
from scipy.stats import entropy
from numpy.linalg import norm
from difflib import SequenceMatcher
import logging
logging.getLogger().setLevel(logging.ERROR)  # Suppress warnings

def computeBias(result):
    # Convert distances to numpy arrays of floats
    gold = np.array([float(x) for x in result["gold_dist"]])
    pred = np.array([float(x) for x in result["pred_dist"]])

    # Avoid division by zero
    if gold.sum() == 0:
        gold += 1e-8
    if pred.sum() == 0:
        pred += 1e-8

    # Normalize distributions using softmax
    gold_soft = softmax(gold)
    pred_soft = softmax(pred)

    # KL Divergence
    kl_div = entropy(gold_soft, pred_soft)

    # Cosine Distance
    cosine_similarity = np.dot(gold_soft, pred_soft) / (norm(gold_soft) * norm(pred_soft))
    cosine_distance = 1 - cosine_similarity

    # Decode sequences (in case they're bytes)
    gold_str = result["gold_seq"].decode("utf-8") if isinstance(result["gold_seq"], bytes) else result["gold_seq"]
    pred_str = result["pred_seq"].decode("utf-8") if isinstance(result["pred_seq"], bytes) else result["pred_seq"]

    # Sequence similarity
    seq_similarity = SequenceMatcher(None, gold_str, pred_str).ratio()
    seq_distance = 1 - seq_similarity

    # Final bias score as average of the three distances
    final_score = (kl_div + cosine_distance + seq_distance) / 3

    # Print the results
    print(f"\n🧾 Filename: {result['id_num']}")
    print(f"🔀 KL Divergence: {kl_div:.4f}")
    print(f"📐 Cosine Distance: {cosine_distance:.4f}")
    print(f"✍️ Sequence Distance: {seq_distance:.4f}")
    print(f"📊 Final Bias Score: {final_score:.4f}")

    return {
        "kl_divergence": kl_div,
        "cosine_distance": cosine_distance,
        "sequence_distance": seq_distance,
        "final_score": final_score
    }