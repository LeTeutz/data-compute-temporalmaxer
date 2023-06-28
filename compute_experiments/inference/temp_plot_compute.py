import pandas as pd
import matplotlib.pyplot as plt

# Load the data
memory_df = pd.read_csv('final_memory.csv')
time_df = pd.read_csv('final_time.csv')

# Plot memory
plt.figure(figsize=(10, 6))
plt.errorbar(memory_df['size'], memory_df['mean'], yerr=memory_df['std'], fmt='-o', label='Memory', capsize=5)
plt.xlabel('Size of the tensor')
plt.ylabel('Memory (MB)')
plt.title('Memory usage vs Size of tensor')
plt.legend()
plt.show()

# Plot time
plt.figure(figsize=(10, 6))
plt.errorbar(time_df['size'], time_df['mean'], yerr=time_df['std'], fmt='-o', label='Time', capsize=5)
plt.xlabel('Size of the tensor')
plt.ylabel('Time (seconds)')
plt.title('Inference time vs Size of tensor')
plt.legend()
plt.show()
