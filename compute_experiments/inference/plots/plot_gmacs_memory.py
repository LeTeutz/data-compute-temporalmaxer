import pandas as pd
import matplotlib.pyplot as plt

# Read data from files
gmacs_data = pd.read_csv('macs.txt', header=None, names=['Length', 'GMACs'])
memory_data = pd.read_csv('tm_final_memory.csv')

# Clean up data
gmacs_data['Length'] = gmacs_data['Length'].str.extract('(\d+)').astype(int)
gmacs_data['GMACs'] = gmacs_data['GMACs'].str.extract('(\d+\.\d+)').astype(float)

# Create the figure and the two subplots
fig, ax1 = plt.subplots()

# Plot the GMACs data set with its own y-axis
color = 'tab:blue'
ax1.set_xlabel('Size')
ax1.set_ylabel('GMACs', color=color)
ax1.plot(gmacs_data['Length'], gmacs_data['GMACs'], color=color)
ax1.tick_params(axis='y', labelcolor=color)

# Create the second y-axis and plot the memory data set
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Memory Used (MB)', color=color)
ax2.plot(memory_data['size'], memory_data['mean'], color=color)
ax2.tick_params(axis='y', labelcolor=color)

# Adjust plot
plt.tight_layout()

# Save the plot
plt.savefig('gmacs_memory_usage.png')

# Show the plot
plt.show()
