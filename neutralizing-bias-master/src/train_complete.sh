#!/bin/bash
#SHEBANG

ARTICLES_DIR=$1
PREP_OUTPUT_DIR=${2:-bias_data/articles}
FINAL_OUTPUT_DIR=${3:-TEST}
MAX_JOBS=3  #change at ur own risk....

if [ -z "$ARTICLES_DIR" ]; then
  echo "Usage: $0 <articlesDirectory> [prepOutputDir=default:bias_data/articles] [finalOutputDir=default:TEST]"
  exit 1
fi

# Check if the articles directory exists
[ -f "$FINAL_OUTPUT_DIR/test_data.pkl" ] && rm "$FINAL_OUTPUT_DIR/test_data.pkl"
mkdir -p "$PREP_OUTPUT_DIR"
mkdir -p "$FINAL_OUTPUT_DIR"

# process each file in the articles directory
process_file() {
  article_file="$1"
  filename=$(basename "$article_file" .txt)
  test_file="$PREP_OUTPUT_DIR/${filename}.test"
  output_file="$FINAL_OUTPUT_DIR/${filename}.txt"

  echo "Preparing file: $filename"
  python3 prepare_sentence.py --file "$article_file" --output "$test_file" > /dev/null 2>&1

  echo "Running inference on: $filename"
  python joint/inference.py \
    --extra_features_top --pre_enrich --activation_hidden \
    --test_batch_size 1 --bert_full_embeddings --debias_weight 2 --token_softmax \
    --pointer_generator --coverage \
    --working_dir "$FINAL_OUTPUT_DIR" \
    --test "$test_file" \
    --checkpoint model.ckpt \
    --inference_output "$output_file" > /dev/null 2>&1

  echo "Finished processing: $filename"
}

job_count=0

for article_file in "$ARTICLES_DIR"/*.txt; do
  process_file "$article_file" &

  ((job_count++))
  if ((job_count % MAX_JOBS == 0)); then
    wait  # wait for all background jobs to finish before spawning more
  fi
done

wait  # pause for any remaining background jobs to finish
echo "✅ All files processed."
