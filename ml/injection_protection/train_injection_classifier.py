import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier, IsolationForest
from sklearn.metrics import roc_auc_score, classification_report
import joblib
import lightgbm as lgb

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
import xgboost as xgb
from catboost import CatBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import PassiveAggressiveClassifier


file_path = "small_dataset_combined_output_normalized.csv"
data = pd.read_csv(file_path)


# Prepare features and labels
X = data[['HT', 'FT']]
y = data['Injection']

# Standardize features (removed)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Print the processed data
print("\nProcessed Data:")
print(X_scaled)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)


# Define models
models = {
    "RandomForest": RandomForestClassifier(random_state=42),

    #"LightGBM": lgb.LGBMClassifier(random_state=42),
    #"GradientBoosting": GradientBoostingClassifier(random_state=42),
    #"ExtraTrees": ExtraTreesClassifier(random_state=42),
    #"IsolationForest": IsolationForest(random_state=42),
    #"LogisticRegression": LogisticRegression(random_state=42),
    #"SVM": SVC(random_state=42),
    #"KNN": KNeighborsClassifier(),
    #"AdaBoost": AdaBoostClassifier(random_state=42),
    #"XGBoost": xgb.XGBClassifier(random_state=42),
    #"CatBoost": CatBoostClassifier(random_state=42, silent=True),
    #"NeuralNetwork": MLPClassifier(random_state=42),
    #"DecisionTree": DecisionTreeClassifier(random_state=42),
    #"PassiveAggressive": PassiveAggressiveClassifier(random_state=42)
}


best_model = None
best_score = -np.inf
best_name = None

# Train and evaluate models
for name, model in models.items():
    if name == "IsolationForest":
        # Isolation Forest (unsupervised)
        model.fit(X_train)
        y_pred = model.predict(X_test)
        y_pred = np.where(y_pred == -1, 1, 0)  # Convert anomaly (-1) to "Injection" (1)
        score = roc_auc_score(y_test, y_pred)
    else:
        # Supervised models
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
        score = roc_auc_score(y_test, y_prob) if y_prob is not None else roc_auc_score(y_test, y_pred)

    print(f"\n{name} - ROC-AUC Score: {score:.4f}")

    if score > best_score:
        best_score = score
        best_model = model
        best_name = name

# Save the best model and scaler
print(f"\nBest Model: {best_name} with ROC-AUC Score: {best_score:.4f}")
joblib.dump(best_model, f'{best_name}_model.pkl')

joblib.dump(scaler, 'injection_scaler.pkl')
