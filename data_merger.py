import os

import pandas as pd
from datetime import datetime

def get_latest_file(directory):
    """
    Returns the path of the latest created file in the given directory.
    """
    files = [os.path.join(directory, f) for f in os.listdir(directory)]
    if not files:
        return None
    
    latest_file = max(files, key=os.path.getctime)
    return latest_file


def merge_csvs_with_statewise_results(directory_path,statewise_file_path):
    resp_file  = get_latest_file(directory_path) 
    if resp_file != None and resp_file.endswith(".csv"):
        statewise_df = pd.read_csv(statewise_file_path)
        resp_df = pd.read_csv(resp_file)
        resp_df.columns = ['Unnamed: 0','district_name','market_name','commodity','vareity','grade','min_rs_quintal','max_rs_quintal','modal_rs_quintal','date']
        resp_df.drop(columns=['Unnamed: 0'],inplace=True)
        resp_df['year'] = resp_df['date'].str.split(" ").str[2]
        resp_df['month'] = resp_df['date'].str.split(" ").str[1]
        resp_df['day_of_month'] = resp_df['date'].str.split(" ").str[0]
        try:
            resp_df['datetime'] = pd.to_datetime(resp_df['date'])
        except Exception as e :
            resp_df['datetime'] = resp_df['date'].apply(parse_date)
        statewise_df = pd.concat([statewise_df,resp_df],ignore_index=True)
        statewise_df.to_csv(statewise_file_path)
    else:
        print("error in parsing csv")


def parse_date(val):
        try:
            return pd.to_datetime(val)
        except Exception:
            print("value: " + val)

            
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
            if ( folder_name + "_all_years.csv") in os.listdir(output_folder):
                folder_path = os.path.join(directory_path, folder_name)
                if os.path.isdir(folder_path):
                    output_file = os.path.join(output_folder, folder_name + "_all_years.csv")
                    merge_csvs_with_statewise_results(folder_path,output_file)

            else:
                folder_path = os.path.join(directory_path, folder_name)
                # Check if   it's a directory
                if os.path.isdir(folder_path):
                    output_file = os.path.join(output_folder, folder_name + "_all_years.csv")
                    merge_csvs_in_directory(folder_path, output_file)

statewise_all_years(directory_paths=directory_paths,output_folders=output_folders)
