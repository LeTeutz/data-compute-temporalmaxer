import os
import re
import csv
import statistics

# Define the list of percentages
percentages = [0.1, 0.2, 0.4, 0.6, 0.8, 1.0]

# Initialize a dictionary to store the average mAP values and standard deviations for each tIoU value
results = {0.3: [], 0.4: [], 0.5: [], 0.6: [], 0.7: []}

# Iterate over the percentages
for percentage in percentages:
    mAP_values_by_tIoU = {0.3: [], 0.4: [], 0.5: [], 0.6: [], 0.7: []}
    # Iterate over the runs for each percentage
    for run in range(1, 6):
        # Define the filename pattern
        filename = f"final_accuracy_p{percentage}_run{run}.txt"
        # Read the file
        with open(filename, 'r') as file:
            content = file.read()
        # Extract the mAP values for different tIoU values using regular expressions
        tIoU_values = re.findall(r"\|tIoU = (\d.\d+): mAP = ([\d.]+)", content)
        for tIoU, mAP in tIoU_values:
            mAP_values_by_tIoU[float(tIoU)].append(float(mAP))

    # Calculate the average and standard deviation for each tIoU value
    for tIoU, mAP_values in mAP_values_by_tIoU.items():
        average_mAP = statistics.mean(mAP_values)
        std_mAP = statistics.stdev(mAP_values) if len(mAP_values) > 1 else 0
        results[tIoU].append((percentage, average_mAP, std_mAP))

# Create a CSV file for each tIoU value to store the results
for tIoU, data in results.items():
    filename = f"mAP_results_tIoU_{tIoU}.csv"
    with open(filename, 'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Percentage", "Average mAP", "Standard Deviation"])
        # Write the results to the CSV file
        for item in data:
            writer.writerow([item[0], item[1], item[2]])

print("Results written to separate CSV files for each tIoU.")
