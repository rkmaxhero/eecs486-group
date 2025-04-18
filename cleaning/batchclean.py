import os
import time
from singleclean import process_single_file

def batch_process():
    in_dir = "in"
    files = [f for f in os.listdir(in_dir) if f.endswith(".out")]

    for filename in files:
        print(f"Processing: {filename}")
        try:
            process_single_file(filename)
        except Exception as e:
            print(f"Error processing {filename}: {e}")
        time.sleep(6)  # To avoid hitting the API too fast

if __name__ == "__main__":
    batch_process()
