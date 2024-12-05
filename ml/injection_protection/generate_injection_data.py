import pandas as pd
import random


# Function to generate synthetic keystroke injection attack data
def generate_injection_attack_dataset(num_rows):
    data = []
    for _ in range(num_rows):
        vk = random.randint(13, 90)
        ht = random.randint(5, 20)
        ft = random.choice([-1, random.randint(10, 30)])

        label = 1  # Assign label 1 to indicate keystroke injection attack

        data.append((vk, ht, ft, label))

    return pd.DataFrame(data, columns=["VK", "HT", "FT", "Injection"])


num_rows = 600
large_injection_attack_dataset = generate_injection_attack_dataset(num_rows)

# Save to CSV
file_path = "DATASET/large_injection_attack_data.csv"
large_injection_attack_dataset.to_csv(file_path, index=False)
print(f"Dataset saved to {file_path}")
