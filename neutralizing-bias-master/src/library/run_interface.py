# Returns dict with original and predicted sequences, and their distributions

import os
import subprocess
import ast
import logging
logging.getLogger().setLevel(logging.ERROR)


def runInterface(filename: str, tsv_temp_path: str) -> dict:
    print(f"\nRunning inference for {filename}...")
    output_path = f"training_output/{filename}"
    cmd = [
        "python", "joint/inference.py",
        "--extra_features_top", "--pre_enrich", "--activation_hidden",
        "--test_batch_size", "1", "--bert_full_embeddings", "--debias_weight", "1.3", "--token_softmax",
        "--pointer_generator", "--coverage",
        "--working_dir", "temp",
        "--test", tsv_temp_path,
        "--checkpoint", "model.ckpt",
        "--inference_output", output_path
    ]
    # subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(cmd, check=True)

    result = {
        "id_num": filename,
        "in_seq": None,
        "gold_seq": None,
        "pred_seq": None,
        "gold_dist": [],
        "pred_dist": [],
        "gold_tok": [],
        "pred_tok": []
    }

    with open(output_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("IN SEQ:"):
                result["in_seq"] = line.split("IN SEQ:")[1].strip().lstrip("b'").rstrip("'")
            elif line.startswith("GOLD SEQ:"):
                result["gold_seq"] = line.split("GOLD SEQ:")[1].strip().lstrip("b'").rstrip("'")
            elif line.startswith("PRED SEQ:"):
                result["pred_seq"] = line.split("PRED SEQ:")[1].strip().lstrip("b'").rstrip("'")
            elif line.startswith("GOLD DIST:"):
                array_str = line.split("GOLD DIST:")[1].strip()
                result["gold_dist"] = ast.literal_eval(array_str.replace("np.float32", ""))
            elif line.startswith("PRED DIST:"):
                array_str = line.split("PRED DIST:")[1].strip()
                result["pred_dist"] = ast.literal_eval(array_str.replace("np.float32", ""))
            elif line.startswith("GOLD TOK:"):
                result["gold_tok"] = ast.literal_eval(line.split("GOLD TOK:")[1].strip())
            elif line.startswith("PRED TOK:"):
                result["pred_tok"] = ast.literal_eval(line.split("PRED TOK:")[1].strip())
    return result
        