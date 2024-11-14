import pandas as pd
import numpy as np

# Load the CSV file into a DataFrame
file_path = "small_dataset_combined_output.csv"  # Replace with the actual file path
data = pd.read_csv(file_path)

# Display the original data
#print("Original Data:")
#print(data)

# Preprocessing: Replace invalid Flight Time values
def preprocess_flight_time(ft):
    if ft > 1500 or ft == -1:
        return -1
    return ft

data['FT'] = data['FT'].apply(preprocess_flight_time)

# Extract valid values for normalization
valid_ht = data['HT']  # All HT values are valid in this example
valid_ft = data[data['FT'] >= 0]['FT']  # Exclude FT = -1 for normalization

# Compute normalization parameters
ht_min, ht_max = valid_ht.min(), valid_ht.max()
ft_min, ft_max = valid_ft.min(), valid_ft.max()

# Normalization function
def normalize(value, min_val, max_val):
    if value == -1:  # Preserve -1 as is
        return -1
    return (value - min_val) / (max_val - min_val)

# Apply normalization
data['HT_normalized'] = data['HT'].apply(lambda x: normalize(x, ht_min, ht_max))
data['FT_normalized'] = data['FT'].apply(lambda x: normalize(x, ft_min, ft_max))

# Ensure the first flight time in the dataset is -1
data.loc[0, 'FT_normalized'] = -1

# Display the processed data
print("\nProcessed Data:")
print(data)

# Save the normalized data to a new CSV file
output_file = "small_dataset_combined_output_normalized.csv"
data.to_csv(output_file, index=False)
print(f"\nNormalized data saved to {output_file}")
