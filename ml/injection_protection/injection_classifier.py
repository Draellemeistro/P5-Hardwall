from joblib import load
import pandas as pd

scaler = load('injection_scaler.pkl')
random_forest_model = load('RF_injection_classifier_model.pkl')


input_csv_path = 'dataset/GUN-A1BFO1ZAS64NUZ-1-HUMAN_with_injection_normalized.csv'
input_data = pd.read_csv(input_csv_path)

# Apply scaler to input data
input_data[['HT', 'FT']] = scaler.transform(input_data[['HT', 'FT']])

# Prepare features
scaled_data = input_data[['HT', 'FT']]

# Make predictions
predicted_labels = random_forest_model.predict(scaled_data)

# Add predictions to the input data
input_data['Prediction'] = predicted_labels
input_data['Prediction'] = input_data['Prediction'].map({1: 'Injection', 0: 'Human'})


print(input_data[['HT', 'FT', 'Prediction']])

output_csv_path = 'predictions_output.csv'
input_data.to_csv(output_csv_path, index=False)
print(f"Predictions saved to {output_csv_path}")
