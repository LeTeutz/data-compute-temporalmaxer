import os
import re
import csv
import statistics

# Define the list of percentages
percentages = [0.1, 0.2, 0.4, 0.6, 0.8, 1.0]

# Initialize a dictionary to store the mAP values for each percentage
results = {}

# Iterate over the percentages
for percentage in percentages:
    mAP_values = []
    # Iterate over the runs for each percentage
    for run in range(1, 6):
        # Define the filename pattern
        filename = f"final_accuracy_p{percentage}_run{run}.txt"
        # Read the file
        with open(filename, 'r') as file:
            content = file.read()
        # Extract the mAP value using regular expressions
        mAP = re.search(r"Average mAP: ([\d.]+)", content)
        if mAP:
            mAP_values.append(float(mAP.group(1)))
    
    # Store the mAP values for the current percentage
    results[percentage] = mAP_values

# Create a CSV file to store the results
with open('temporalmaxer.csv', 'w+', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["percentage", "mAP", "std"])
    
    # Iterate over the results and calculate the average and standard deviation
    for percentage, mAP_values in results.items():
        if (percentage*100).is_integer():
            percentage_str = f"{int(percentage*100)}%"
        else:
            percentage_str = f"{percentage*100}%"
        average_mAP = statistics.mean(mAP_values)
        std_mAP = statistics.stdev(mAP_values) if len(mAP_values) > 1 else 0
        writer.writerow([percentage_str, f"{average_mAP:.3f}", f"{std_mAP:.3f}"])
