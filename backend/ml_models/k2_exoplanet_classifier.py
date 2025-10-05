import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt

# -------------------------------------------------------------
#  K2 EXOPLANET CLASSIFIER (Clean and Explanatory Version)
# -------------------------------------------------------------

def load_and_inspect_data(file_path):
    print("\n🔍 Step 1: Loading Dataset ...")
    df = pd.read_csv(file_path, comment='#')
    print(f"✅ Loaded successfully! Shape: {df.shape}")
    print("\nFirst 5 rows:")
    print(df.head())
    return df


def preprocess_data(df, target_column):
    print("\n⚙️ Step 2: Preprocessing Data ...")

    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataset!")

    # Drop rows where target is missing
    df = df.dropna(subset=[target_column])

    # Separate features and target
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # Drop identifier columns if present
    id_like_cols = [col for col in X.columns if col.lower() in ["id", "kepid", "rowid", "index"]]
    if id_like_cols:
        print(f"🧹 Removing identifier columns: {id_like_cols}")
        X = X.drop(columns=id_like_cols)

    # Handle categorical and numeric columns
    cat_cols = X.select_dtypes(include=['object']).columns
    num_cols = X.select_dtypes(exclude=['object']).columns

    print(f"📊 Numeric columns: {len(num_cols)} | Categorical columns: {len(cat_cols)}")

    # Fill missing values
    X[num_cols] = X[num_cols].fillna(X[num_cols].median())
    X[cat_cols] = X[cat_cols].fillna('Unknown')

    # Encode categorical columns
    label_encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le

    # Encode target
    y_encoder = LabelEncoder()
    y = y_encoder.fit_transform(y)

    print(f"✅ Preprocessing complete! Final shape: {X.shape}")
    return X, y, y_encoder


def train_random_forest(X, y):
    print("\n🌲 Step 3: Training Random Forest Model ...")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Model trained successfully! Accuracy: {acc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    return model, X_test, y_test


def plot_feature_importance(model, X):
    print("\n📈 Step 4: Plotting Feature Importances ...")

    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]

    plt.figure(figsize=(10, 6))
    plt.title("Feature Importance (K2 Exoplanet Classifier)")
    plt.bar(range(len(importances)), importances[indices], align='center')
    plt.xticks(range(len(importances)), X.columns[indices], rotation=90)
    plt.tight_layout()
    plt.show()


def explain_sample_predictions(model, X_test, y_test, y_encoder, num_samples=5):
    print("\n🔎 Step 5: Sample Predictions ...")

    preds = model.predict(X_test[:num_samples])
    decoded_preds = y_encoder.inverse_transform(preds)
    decoded_actual = y_encoder.inverse_transform(y_test[:num_samples])

    for i in range(num_samples):
        print(f"Sample {i+1} → Predicted: {decoded_preds[i]} | Actual: {decoded_actual[i]}")


def main():
    file_path = "k2pandc_2025.10.04_00.32.39.csv"
    target_column = "disposition"

    df = load_and_inspect_data(file_path)
    X, y, y_encoder = preprocess_data(df, target_column)
    model, X_test, y_test = train_random_forest(X, y)
    plot_feature_importance(model, X)
    explain_sample_predictions(model, X_test, y_test, y_encoder)


if __name__ == "__main__":
    main()
