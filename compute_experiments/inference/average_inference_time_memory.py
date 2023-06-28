import os
import pandas as pd
import numpy as np

# set directory where the .txt files are located
directory = 'inference_time'

# define function to calculate mean and std deviation and save to csv
def compute_and_save_to_csv(file_prefix, csv_name):
    # create a list to collect all dataframes
    data_list = []

    # iterate over the .txt files in the directory
    for filename in os.listdir(directory):
        if filename.startswith(file_prefix) and filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            # load the data from the .txt file
            data = pd.read_csv(file_path, header=None, names=['size', file_prefix])
            # append dataframe to the list
            data_list.append(data)

    # concat all dataframes into one
    all_data = pd.concat(data_list, ignore_index=True)

    # group the data by 'size' and calculate the mean and std deviation
    final_data = all_data.groupby('size')[file_prefix].agg(['mean', 'std'])

    # save the final_data dataframe to a csv file
    final_data.to_csv(csv_name)

# call function for time data
compute_and_save_to_csv("time_", "final_time.csv")

# call function for memory data
compute_and_save_to_csv("memory_", "final_memory.csv")
