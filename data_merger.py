import os

import pandas as pd


def merge_csvs_in_directory(directory_path, output_file):
    """Merges all CSV files in a directory into a single CSV file.

    Args:
    directory_path: The path to the directory containing the CSV files.
    output_file: The path to the output CSV file.
    """

    # Get a list of all CSV files in the directory
    csv_files = [
        os.path.join(directory_path, file)
        for file in os.listdir(directory_path)
        if file.endswith(".csv")
    ]

    # Create an empty DataFrame to store the merged data
    merged_df = pd.DataFrame()

    # Iterate through each CSV file and append it to the merged DataFrame
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        merged_df = pd.concat([merged_df, df], ignore_index=True)

    # Save the merged DataFrame to
    # a CSV file
    merged_df.to_csv(output_file, index=False)


# Replace 'your_directory_path' with the actual path to your directory
directory_path = "./fetch_data/responses/Onion"
output_folder = "./fetch_data/statewise_results/Onion"
# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Iterate through   each folder in the directory
for folder_name in os.listdir(directory_path):
    folder_path = os.path.join(directory_path, folder_name)

    # Check if   it's a directory
    if os.path.isdir(folder_path):
        output_file = os.path.join(output_folder, folder_name + "_all_years.csv")
        merge_csvs_in_directory(folder_path, output_file)
