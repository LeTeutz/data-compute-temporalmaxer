import pandas as pd
import matplotlib.pyplot as plt

# Read the csv files into pandas DataFrames
af_data = pd.read_csv('af_final_time.csv')
td_data = pd.read_csv('td_final_time.csv')
tm_data = pd.read_csv('tm_final_time.csv')

# Create a new figure
plt.figure(figsize=(10, 6))

# Plot the data from each DataFrame with standard deviation as filled region
# The markersize parameter has been added to make the markers smaller
plt.plot(af_data['size'], af_data['mean'], marker='o', markersize=3, label='ActionFormer')
plt.fill_between(af_data['size'], af_data['mean'] - af_data['std'], af_data['mean'] + af_data['std'], alpha=0.1)

plt.plot(td_data['size'], td_data['mean'], marker='o', markersize=3, label='TriDet')
plt.fill_between(td_data['size'], td_data['mean'] - td_data['std'], td_data['mean'] + td_data['std'], alpha=0.1)

plt.plot(tm_data['size'], tm_data['mean'], marker='o', markersize=3, label='TemporalMaxer')
plt.fill_between(tm_data['size'], tm_data['mean'] - tm_data['std'], tm_data['mean'] + tm_data['std'], alpha=0.1)

# Add a legend
plt.legend()

# Add labels for the x and y axes
plt.xlabel('Size')
plt.ylabel('Mean Inference Time')

# Add a title
plt.title('Mean Inference Time for Different Models with Standard Deviation')
plt.savefig('inference_time_3lines.png')

# Display the plot
plt.show()
