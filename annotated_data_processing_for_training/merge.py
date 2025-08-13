"""
ChatGPT made this function
"""
import os

# Define your directories
original_dir = 'SRL_data/train/train_5'
curated_dir = 'SRL_data_with_curated_entities/curated_entities/train_5'
output_dir = 'SRL_data_curated_entities_and_all_events/train/train_5'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Loop through all files in the original directory
for filename in os.listdir(original_dir):
    original_path = os.path.join(original_dir, filename)
    curated_path = os.path.join(curated_dir, filename)
    output_path = os.path.join(output_dir, filename)

    # Skip if matching curated file doesn't exist
    if not os.path.isfile(curated_path):
        print(f"Warning: No curated file for {filename}, skipping.")
        continue

    with open(original_path, 'r', encoding='utf-8') as f1, \
         open(curated_path, 'r', encoding='utf-8') as f2, \
         open(output_path, 'w', encoding='utf-8') as out:

        for line1, line2 in zip(f1, f2):
            line1 = line1.rstrip('\n')
            line2 = line2.rstrip('\n')

            # Skip empty lines (e.g., sentence breaks)
            if not line1.strip():
                out.write('\n')
                continue

            last_col = line2.split('\t')[-1]
            merged_line = f"{line1}\t{last_col}\n"
            out.write(merged_line)

    print(f"Merged: {filename}")