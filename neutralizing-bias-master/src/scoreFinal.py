import os

def parse_file(filepath, normalize=False):
    data = {}
    with open(filepath, 'r') as file:
        header = file.readline().strip().split('\t')
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) != len(header):
                continue
            entry = dict(zip(header, parts))
            # Convert scores to float
            for key in ['pscore', 'nscore', 'neuscore']:
                entry[key] = float(entry[key])
            filename = entry['filename']
            if normalize:
                filename = os.path.splitext(filename)[0]  # strip .txt, .out, etc.
            data[filename] = entry
    return data

def process_bias_differences(directory):
    files = os.listdir(directory)
    initial_files = [f for f in files if f.endswith("_bias_analysis_initial.txt")]

    for initial_file in initial_files:
        source = initial_file.replace("_bias_analysis_initial.txt", "")
        final_file = f"{source}_bias_analysis_final.txt"
        output_file = f"{source}_final_bias.txt"

        initial_path = os.path.join(directory, initial_file)
        final_path = os.path.join(directory, final_file)
        output_path = os.path.join(directory, output_file)

        if not os.path.exists(final_path):
            print(f"Skipping {source}: Final file not found.")
            continue

        initial_data = parse_file(initial_path, normalize=True)
        final_data = parse_file(final_path, normalize=True)

        print(f"Comparing scores for {source}...")
        if not initial_data or not final_data:
            print(f"Skipping {source}: No data found in initial or final files.")
            continue

        with open(output_path, 'w') as out:
            out.write("filename\tpscore_diff\tnscore_diff\tneuscore_diff\n")
            for filename in initial_data:
                if filename not in final_data:
                    continue
                initial = initial_data[filename]
                final = final_data[filename]
                p_diff = final['pscore'] - initial['pscore']
                n_diff = final['nscore'] - initial['nscore']
                neu_diff = final['neuscore'] - initial['neuscore']
                out.write(f"{filename}\t{p_diff:.3f}\t{n_diff:.3f}\t{neu_diff:.3f}\n")

        print(f"Saved score differences to {output_file}")

if __name__ == "__main__":
    process_bias_differences("training_output")
