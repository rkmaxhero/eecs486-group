#!/bin/bash
# Remove old test_data.pkl so inference always re‑runs
[ -f "TEST/test_data.pkl" ] && rm "TEST/test_data.pkl"

# Loop over every .test file in bias_data/WNC
for test_file in bias_data/articles/*.test; do
  # strip directory and extension to get the base name
  filename=$(basename "$test_file")       # e.g. input-single.test
  base="${filename%.test}"               # e.g. input-single

  # build output path
  output="TEST/${base}-debias.txt"

  # run inference
  python joint/inference.py \
    --extra_features_top \
    --pre_enrich \
    --activation_hidden \
    --test_batch_size 1 \
    --bert_full_embeddings \
    --debias_weight 1.4 \
    --token_softmax \
    --pointer_generator \
    --coverage \
    --working_dir TEST \
    --test "$test_file" \
    --checkpoint model.ckpt \
    --inference_output "$output"
done
