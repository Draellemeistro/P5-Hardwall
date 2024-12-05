from pynput import keyboard
import time
import numpy as np
import joblib
import pandas as pd

# Load your trained model and scaler
model = joblib.load("RF_injection_classifier_model.pkl")
scaler = joblib.load("injection_scaler.pkl")

# Variables to track timing
key_press_time = {}
keystroke_data = []
last_release_time = None


def preprocess_features(ht, ft):
    # Convert values >1500 ms to -1
    ft = -1 if ft > 1500 else ft

    # Create feature DataFrame with correct column names
    features = pd.DataFrame([[ht, ft]], columns=['HT', 'FT'])

    # Scale the features using the fitted scaler
    features_scaled = scaler.transform(features)

    # print(f"Raw Features: HT={ht}, FT={ft}")
    # print(f"Scaled Features: {features_scaled}")
    return features_scaled


def on_press(key):
    try:
        key_press_time[key] = time.time()
    except Exception as e:
        print(f"Error on_press: {e}")


def on_release(key):
    global last_release_time
    try:
        press_time = key_press_time.pop(key, None)
        if press_time is not None:
            release_time = time.time()
            hold_time = (release_time - press_time) * 1000  # Convert to milliseconds

            # Calculate flight time
            flight_time = (press_time - last_release_time) * 1000 if last_release_time else 0
            last_release_time = release_time

            # Preprocess features
            features_scaled = preprocess_features(hold_time, flight_time)

            # Predict with the model
            prediction = model.predict(features_scaled)
            print(f"Prediction: {'Injection Attack' if prediction[0] == 1 else 'Human'}")

    except Exception as e:
        print(f"Error on_release: {e}")


# Start listening to keyboard events
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
