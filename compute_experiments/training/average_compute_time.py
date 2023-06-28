import os
import csv
import re
import numpy as np

folder_path = 'compute_results'

num_seeds = 5
num_models = 5

seed_results = {}
overall_results = {}
time_range_results = {}  # A new dictionary to store the lowest and highest training time for each seed

for filename in os.listdir(folder_path):
    if filename.startswith('ntrain_'):
        matches = re.match(r'ntrain_(\d)_(\d+).txt', filename)
        seed = int(matches.group(1))
        run = int(matches.group(2))

        with open(os.path.join(folder_path, filename), 'r') as file:
            content = file.read()

        time_match = re.search(r'TOTAL TIME FOR TRAINING:  (\d+\.?\d*)', content)
        training_time = float(time_match.group(1)) if time_match else None

        seed_match = re.search(r'\'init_rand_seed\': (\d+)', content)
        seed_number = int(seed_match.group(1)) if seed_match else None

        if seed not in seed_results:
            seed_results[seed] = []

        seed_results[seed].append({'Run': run, 'Time': training_time, 'Seed Number': seed_number})

        # Update the time_range_results dictionary
        if seed not in time_range_results:
            time_range_results[seed] = {'Lowest Time': training_time, 'Highest Time': training_time}
        else:
            if training_time < time_range_results[seed]['Lowest Time']:
                time_range_results[seed]['Lowest Time'] = training_time
            if training_time > time_range_results[seed]['Highest Time']:
                time_range_results[seed]['Highest Time'] = training_time

    elif filename.startswith('nresults_'):
        matches = re.match(r'nresults_(\d)_(\d+).txt', filename)
        seed = int(matches.group(1))
        run = int(matches.group(2))

        with open(os.path.join(folder_path, filename), 'r') as file:
            content = file.read()

        accuracy_match = re.search(r'Average mAP: (\d+\.\d*)', content)
        accuracy = float(accuracy_match.group(1)) if accuracy_match else None
        overall_results[(seed, run)] = {'Accuracy': accuracy}

seed_output_file = 'seed_results.csv'
overall_output_file = 'overall_results.csv'
time_range_output_file = 'time_range_results.csv'  # Output filename for time ranges


# Compute average and standard deviation for each seed
seed_average = {}
seed_std_dev = {}
for seed, results in seed_results.items():
    times = [result['Time'] for result in results if result['Time'] is not None and not np.isnan(result['Time'])]
    accuracies = [overall_results[(seed, run)]['Accuracy'] for result in results
                  if result['Time'] is not None and not np.isnan(result['Time']) and (seed, run) in overall_results]
    
    seed_average[seed] = {
        'Time (Average)': np.mean(times) if len(times) > 0 else None,
        'Accuracy (Average)': np.mean(accuracies) if len(accuracies) > 0 else None,
        'Time (Standard Deviation)': np.std(times) if len(times) > 0 else None,
        'Accuracy (Standard Deviation)': np.std(accuracies) if len(accuracies) > 0 else None
    }
    
    print(f"Seed: {seed}")
    print("Times:", times)
    print("Accuracies:", accuracies)
    print()

# Compute overall average and standard deviation
all_times = [result['Time'] for results in seed_results.values() for result in results if result['Time'] is not None and not np.isnan(result['Time'])]
all_accuracies = [result['Accuracy'] for result in overall_results.values() if result['Accuracy'] is not None and not np.isnan(result['Accuracy'])]

overall_average = {
    'Time (Average)': np.mean(all_times) if len(all_times) > 0 else None,
    'Accuracy (Average)': np.mean(all_accuracies) if len(all_accuracies) > 0 else None,
    'Time (Standard Deviation)': np.std(all_times) if len(all_times) > 0 else None,
    'Accuracy (Standard Deviation)': np.std(all_accuracies) if len(all_accuracies) > 0 else None
}

print(f"All Times: {all_times}")
print(f"All Accuracies: {all_accuracies}")
print()

# Write results to CSV files
with open(seed_output_file, 'w', newline='') as csvfile:
    fieldnames = ['Seed', 'Seed Number', 'Time (Average)', 'Accuracy (Average)', 'Time (Standard Deviation)', 'Accuracy (Standard Deviation)']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for seed, data in seed_average.items():
        data = {k: round(v, 3) for k, v in data.items()}
        writer.writerow({'Seed': seed, 'Seed Number': seed_results[seed][0]['Seed Number'], **data})

with open(overall_output_file, 'w', newline='') as csvfile:
    fieldnames = ['Time (Average)', 'Accuracy (Average)', 'Time (Standard Deviation)', 'Accuracy (Standard Deviation)']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    overall_average = {k: round(v, 3) for k, v in overall_average.items()}
    writer.writerow(overall_average)

print("Results have been saved to", seed_output_file, "and", overall_output_file)

with open(time_range_output_file, 'w', newline='') as csvfile:
    fieldnames = ['Seed', 'Seed Number', 'Lowest Time', 'Highest Time']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for seed, data in time_range_results.items():
        writer.writerow({'Seed': seed, 'Seed Number': seed_results[seed][0]['Seed Number'], 'Lowest Time': data['Lowest Time'], 'Highest Time': data['Highest Time']})

print("Results have been saved to", seed_output_file, ",", overall_output_file, "and", time_range_output_file)