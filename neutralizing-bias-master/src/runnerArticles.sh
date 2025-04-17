#!/bin/bash
# the old.pkl file just re-runs previous tests. Delete to run current tests
[ -f "TEST/test_data.pkl" ] && rm "TEST/test_data.pkl"
python joint/inference.py \
       --extra_features_top --pre_enrich --activation_hidden \
       --test_batch_size 1 --bert_full_embeddings --debias_weight 2 --token_softmax \
       --pointer_generator --coverage \
       --working_dir TEST \
       --test bias_data/articles/fox12.test \
       --checkpoint model.ckpt \
       --inference_output TEST/fox12.txt