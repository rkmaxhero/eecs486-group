import os
import subprocess
import logging
logging.getLogger().setLevel(logging.ERROR)  # Suppress warnings
from library.prepare_article import convertToTsv
from library.run_interface import runInterface
from library.calculate_bias import computeBias

def main(directory="parsed_articles"):
    os.makedirs("temp", exist_ok=True)  # Ensure temp directory exists
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    for filename in files:
        print(f"Processing file: {filename}")
        filepath = os.path.join(directory, filename)
        with open(filepath, "r") as f:
            content = f.read().strip()
            if not content:
                print(f"Skipping empty file: {filename}")
                continue

        # Step 2: Get TSV string from content
        print("Converting to TSV...")
        tsv_data = convertToTsv(content, id_num=filename)

        # Write TSV to temp file for inference
        print("Writing TSV to temp file...")
        tsv_temp_path = "temp/temp.test"
        with open(tsv_temp_path, "w") as test_file:
            test_file.write(tsv_data)

        # Step 3: Run inference
        print("Running inference...")
        result = runInterface(filename, tsv_temp_path)
        
        # Step 4: Print output
        print("Computing bias...")
        computeBias(result)


if __name__ == "__main__":
    main()