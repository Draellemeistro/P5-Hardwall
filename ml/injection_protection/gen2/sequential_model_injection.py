import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, classification_report
import joblib
from tf_keras.layers import LSTM, Dense
from tf_keras.models import Sequential
from tf_keras.optimizers import Adam




# Load and preprocess data
file_path = "combined_dataset.csv"
data = pd.read_csv(file_path)

# Prepare features and labels
X = data[['VK', 'HT', 'FT']].values
y = data['Injection'].values

# Extract VK separately and scale only HT and FT
X_vks = X[:, 0].reshape(-1, 1)  # VK values (no scaling needed)
X_continuous = X[:, 1:]  # HT and FT columns

# Standardize continuous features (HT and FT)
scaler = StandardScaler()
X_continuous_scaled = scaler.fit_transform(X_continuous)

# Combine VK with the scaled features
X_scaled = np.hstack((X_vks, X_continuous_scaled))

# Define buffer logic for grouping
def group_by_space_and_size(features, labels, max_chunk_size=10):
    chunks = []
    chunk_labels = []
    current_chunk = []
    current_labels = []

    for i, (feature, label) in enumerate(zip(features, labels)):
        current_chunk.append(feature)
        current_labels.append(label)

        # Check if we need to create a new chunk
        if len(current_chunk) == max_chunk_size:
            chunks.append(current_chunk)
            chunk_labels.append(1 if any(current_labels) else 0)  # Label is 1 if any 'Injection' in chunk, else 0
            current_chunk = []
            current_labels = []

    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(current_chunk)
        chunk_labels.append(1 if any(current_labels) else 0)

    return chunks, chunk_labels

# Group data into chunks
chunks, chunk_labels = group_by_space_and_size(X_scaled, y)

# Prepare data for sequential model
max_chunk_size = 10
X_prepared_seq = []
for chunk in chunks:
    padded_chunk = np.zeros((max_chunk_size, X_scaled.shape[1]))  # Zero-pad to max_chunk_size
    padded_chunk[:len(chunk), :] = chunk[:max_chunk_size]  # Truncate if chunk > max_chunk_size
    X_prepared_seq.append(padded_chunk)

X_prepared_seq = np.array(X_prepared_seq)  # Shape: (num_chunks, chunk_size, num_features)
y_prepared = np.array(chunk_labels)

print("\nPrepared sequential data (training):")
print(X_prepared_seq[:2])  # Print first 2 chunks (each chunk is padded to max_chunk_size)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_prepared_seq, y_prepared, test_size=0.2, random_state=42, stratify=y_prepared)

# Define sequential model
model = Sequential([
    LSTM(64, input_shape=(max_chunk_size, X_scaled.shape[1]), return_sequences=False),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Evaluate the model
eval_results = model.evaluate(X_test, y_test)
print(f"\nTest Loss: {eval_results[0]:.4f}, Test Accuracy: {eval_results[1]:.4f}")

# Save the model and scaler
model.save('sequential_model.keras')
joblib.dump(scaler, 'injection_scaler.pkl')

# Predictions
y_pred_prob = model.predict(X_test).flatten()
y_pred = (y_pred_prob > 0.5).astype(int)

print("\nPredictions and True Labels:")
print(f"Predictions: {y_pred[:10]}")
print(f"True Labels: {y_test[:10]}")

# ROC-AUC Score
roc_auc = roc_auc_score(y_test, y_pred_prob)
print(f"\nROC-AUC Score: {roc_auc:.4f}")

