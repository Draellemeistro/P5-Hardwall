import numpy as np
import pandas as pd
import joblib
from tf_keras.models import load_model


model = load_model('sequential_model.keras')
scaler = joblib.load('injection_scaler.pkl')


def preprocess_data(file_path, scaler, max_chunk_size=10):
    data = pd.read_csv(file_path)

    X = data[['VK', 'HT', 'FT']].values

    # Extract VK separately and scale HT and FT
    X_vks = X[:, 0].reshape(-1, 1)  # VK values
    X_continuous = X[:, 1:]  # HT and FT columns
    X_continuous_scaled = scaler.transform(X_continuous)
    X_scaled = np.hstack((X_vks, X_continuous_scaled))

    # Group data into chunks
    def group_features(features, max_chunk_size):
        chunks = []
        current_chunk = []
        for feature in features:
            current_chunk.append(feature)
            if len(current_chunk) == max_chunk_size:
                chunks.append(current_chunk)
                current_chunk = []
        # Add the last chunk if it exists
        if current_chunk:
            padded_chunk = np.zeros((max_chunk_size, X_scaled.shape[1]))
            padded_chunk[:len(current_chunk), :] = current_chunk
            chunks.append(padded_chunk)
        return np.array(chunks)

    chunks = group_features(X_scaled, max_chunk_size)
    return chunks


# Preprocess the new CSV file
new_data_path = "keystroke_data.csv"  # Replace with the actual file path
X_new_chunks = preprocess_data(new_data_path, scaler)

# Make predictions
predictions = model.predict(X_new_chunks).flatten()
predicted_labels = (predictions > 0.5).astype(int)


# Display predictions
print("\nPredictions for the new data:")
print(predicted_labels)

# Save predictions to a CSV file
output_file = "predictions_output.csv"  # Define the output file path
predictions_df = pd.DataFrame({
    "Prediction": predicted_labels
})

predictions_df.to_csv(output_file, index=True)
print(f"Predictions saved to {output_file}")

