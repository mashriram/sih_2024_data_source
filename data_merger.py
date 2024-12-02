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
    def parse_date(val):
        try:
            return pd.to_datetime(val)
        except Exception:
            print("value: " + val)
    merged_df.columns = ['Unnamed: 0','district_name','market_name','commodity','vareity','grade','min_rs_quintal','max_rs_quintal','modal_rs_quintal','date']

    merged_df.drop(columns=['Unnamed: 0'],inplace=True)
    merged_df['year'] = merged_df['date'].str.split(" ").str[2]
    merged_df['month'] = merged_df['date'].str.split(" ").str[1]
    merged_df['day_of_month'] = merged_df['date'].str.split(" ").str[0]
    print(merged_df['date'])
    try:
       merged_df['datetime'] = pd.to_datetime(merged_df['date'])
    except Exception as e :
        merged_df['datetime'] = merged_df['date'].apply(parse_date)
    merged_df.to_csv(output_file, index=True)


# Replace 'your_directory_path' with the actual path to your directory
directory_paths = ["./responses/onion","./responses/Gram dal","./responses/Groundnut oil","./responses/gur","./responses/masur dal","./responses/moong dal","./responses/mustard oil","./responses/Potato","./responses/Rice","./responses/Sugar","./responses/tea","./responses/tomato","./responses/tur dal","./responses/urad dal","./responses/vanaspati","./responses/wheat"]
output_folders = ["./statewise_results/onion","./statewise_results/Gram dal","./statewise_results/Groundnut oil","./statewise_results/gur","./statewise_results/masur dal","./statewise_results/moong dal","./statewise_results/mustard oil","./statewise_results/Potato","./statewise_results/Rice","./statewise_results/Sugar","./statewise_results/tea","./statewise_results/tomato","./statewise_results/tur dal","./statewise_results/urad dal","./statewise_results/vanaspati","./statewise_results/wheat"]
# Create the output folder if it doesn't exist
def statewise_all_years(directory_paths:list[str],output_folders:list[str]):
    for directory_path,output_folder in zip(directory_paths,output_folders):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Iterate through   each folder in the directory
        for folder_name in os.listdir(directory_path):
            folder_path = os.path.join(directory_path, folder_name)
            # Check if   it's a directory
            if os.path.isdir(folder_path):
                output_file = os.path.join(output_folder, folder_name + "_all_years.csv")
                merge_csvs_in_directory(folder_path, output_file)

statewise_all_years(directory_paths=directory_paths,output_folders=output_folders)
