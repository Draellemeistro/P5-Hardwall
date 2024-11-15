import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV, RepeatedStratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, precision_recall_curve
from sklearn.utils import class_weight
import joblib
import matplotlib.pyplot as plt

# Load and sample the dataset
file_path = "small_dataset_combined_output_normalized.csv"
data = pd.read_csv(file_path)
sample_frac = 1  # Use 100% of data, adjust as needed
data_sampled = data.sample(frac=sample_frac, random_state=42)

# Preprocess features and labels
X = data_sampled[['HT_normalized', 'FT_normalized']]
y = data_sampled['Injection']

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Stratified split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

# Calculate class weights
class_weights = class_weight.compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
class_weight_dict = dict(enumerate(class_weights))

# Random Forest Classifier
clf = RandomForestClassifier(
    random_state=42,
    class_weight=class_weight_dict
)

# Hyperparameter tuning with RandomizedSearchCV
param_grid = {
    'n_estimators': [50, 100, 200, 500],          # Number of trees
    'max_depth': [None, 10, 20, 50],              # Tree depth
    'min_samples_split': [2, 5, 10],              # Minimum samples to split a node
    'min_samples_leaf': [1, 2, 4],                # Minimum samples per leaf
    'max_features': ['sqrt', 'log2', None],       # Features considered at split
    'bootstrap': [True, False]                   # Bootstrapping
}

# Cross-validation with repeated stratified k-fold
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=42)

# Hyperparameter tuning with RandomizedSearchCV
random_search = RandomizedSearchCV(
    clf, param_distributions=param_grid, n_iter=50, cv=cv, scoring='f1', n_jobs=-1, random_state=42
)

# Perform RandomizedSearchCV
random_search.fit(X_train, y_train)

# Best model
best_clf = random_search.best_estimator_

# Train and evaluate the best model
best_clf.fit(X_train, y_train)
y_pred = best_clf.predict(X_test)

# Classification Report and Confusion Matrix
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ROC-AUC Score
roc_auc = roc_auc_score(y_test, best_clf.predict_proba(X_test)[:, 1])
print(f"\nROC-AUC Score: {roc_auc:.2f}")

# Precision-Recall curve
precision, recall, _ = precision_recall_curve(y_test, best_clf.predict_proba(X_test)[:, 1])
plt.plot(recall, precision, marker='.', label='Precision-Recall curve')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend()
plt.show()

# Feature Importances
feature_importances = best_clf.feature_importances_
print(f"\nFeature Importances: {feature_importances}")

# Save the model and scaler
joblib.dump(best_clf, 'random_forest_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
