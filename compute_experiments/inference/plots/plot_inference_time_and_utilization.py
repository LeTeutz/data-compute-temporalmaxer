import pandas as pd
import matplotlib.pyplot as plt

# Theoretical maximum GMACs for this GPU
max_gmacs = 8200

# Read data from files
time_data = pd.read_csv('tm_final_time.csv')
gmacs_data = pd.read_csv('macs.txt', header=None, names=['Length', 'GMACs'])

# Clean up data
gmacs_data['Length'] = gmacs_data['Length'].str.extract('(\d+)').astype(int)
gmacs_data['GMACs'] = gmacs_data['GMACs'].str.extract('(\d+\.\d+)').astype(float)

# Calculate GMACs per second (note: time is in ms, so multiply by 1000)
gmacs_data['GMACs_per_second'] = gmacs_data['GMACs'] / (time_data['mean'] / 1000)

# Calculate lower and upper bounds for utilization
gmacs_data['Utilization_lower'] = (gmacs_data['GMACs_per_second'] - gmacs_data['GMACs_per_second'] * 0.1) / max_gmacs * 100
gmacs_data['Utilization_upper'] = (gmacs_data['GMACs_per_second'] + gmacs_data['GMACs_per_second'] * 0.1) / max_gmacs * 100

# Create a new DataFrame for the csv file
csv_data = pd.DataFrame({
    'size of the feature': gmacs_data['Length'],
    'inference time': time_data['mean'],
    'utilization': gmacs_data['Utilization'],
    'utilization_lower': gmacs_data['Utilization_lower'],
    'utilization_upper': gmacs_data['Utilization_upper']
})

# Save the DataFrame to a csv file
csv_data.to_csv('inf_time_util.csv', index=False)

# Create the figure and the two subplots
fig, ax1 = plt.subplots()

# Plot the first data set with its own y-axis
color = 'tab:blue'
ax1.set_xlabel('Size')
ax1.set_ylabel('Time (ms)', color=color)
ax1.plot(time_data['size'], time_data['mean'], color=color)
ax1.fill_between(time_data['size'], time_data['mean'] - time_data['std'], time_data['mean'] + time_data['std'], alpha=0.1, color=color)
ax1.tick_params(axis='y', labelcolor=color)

# Create the second y-axis and plot the second data set
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Utilization (%)', color=color)
ax2.plot(gmacs_data['Length'], gmacs_data['Utilization'], color=color)
ax2.fill_between(gmacs_data['Length'], gmacs_data['Utilization_lower'], gmacs_data['Utilization_upper'], alpha=0.1, color=color)
ax2.tick_params(axis='y', labelcolor=color)

# Adjust plot
plt.tight_layout()

# Save the plot
plt.savefig('inference_time_utilization.png')

# Show the plot
plt.show()
