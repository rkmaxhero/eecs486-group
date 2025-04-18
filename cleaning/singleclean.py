import os
import time
import language_tool_python


def fix_grammar_in_chunks(text: str, chunk_size=2000) -> str:
    tool = language_tool_python.LanguageToolPublicAPI('en-US')
    corrected = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        try:
            fixed_chunk = tool.correct(chunk)
        except Exception as e:
            print(f"Chunk failed: {e}")
            fixed_chunk = chunk  # fallback to original
        corrected.append(fixed_chunk)
        time.sleep(6)  # To avoid rate limiting
    return ''.join(corrected)

def process_single_file(input_file: str):
    if not input_file.endswith(".out"):
        print("Error: Please select a file with the .out extension.")
        return

    input_path = os.path.join("in", input_file)
    base_name = os.path.splitext(input_file)[0]
    output_filename = f"{base_name}clean.out"
    output_path = os.path.join("out", output_filename)
    os.makedirs("out", exist_ok=True)

    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' does not exist.")
        return

    print(f"Processing file: {input_file}")
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            original_text = f.read()

        corrected_text = fix_grammar_in_chunks(original_text)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(corrected_text)

        print(f"Correction complete. Saved to: {output_path}")
    except Exception as e:
        print(f"Failed to process {input_file}: {e}")

if __name__ == "__main__":
    filename = input("Enter the filename of the target document in the 'in' directory (e.g. cnn12.out): ").strip()
    process_single_file(filename)

