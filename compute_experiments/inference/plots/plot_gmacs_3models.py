import pandas as pd
import matplotlib.pyplot as plt

# Read data from files
tm_macs_data = pd.read_csv('tm_macs.txt', header=None, names=['Length', 'TM_GMACs'])
td_macs_data = pd.read_csv('td_macs.txt', names=['Length', 'TD_GMACs'])
af_macs_data = pd.read_csv('af_macs.csv', names=['Length', 'AF_GMACs'])

# Clean up data
tm_macs_data['Length'] = tm_macs_data['Length'].str.extract('(\d+)').astype(int)
tm_macs_data['TM_GMACs'] = tm_macs_data['TM_GMACs'].str.extract('(\d+\.\d+)').astype(float)

# Create the figure
fig, ax = plt.subplots()

# Plot the data for each model
ax.plot(tm_macs_data['Length'], tm_macs_data['TM_GMACs'], label='TemporalMaxer')
ax.plot(td_macs_data['Length'], td_macs_data['TD_GMACs'], label='TriDet')
ax.plot(af_macs_data['Length'], af_macs_data['AF_GMACs'], label='ActionFormer')

# Set labels and title
ax.set_xlabel('Size')
ax.set_ylabel('GMACs')
ax.set_title('GMACs of TemporalMaxer, TriDet, and ActionFormer')

# Add a legend
ax.legend()

# Save the plot
plt.savefig('gmacs_models.png')

# Show the plot
plt.show()
