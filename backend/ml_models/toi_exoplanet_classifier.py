import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

print("🔭 TOI EXOPLANET CLASSIFICATION - EXPLAINABLE PIPELINE")
print("=" * 70)


class TOIExoplanetClassifier:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.target_encoder = None
        self.feature_names = None
        self.df = None

    def load_and_preprocess(self, file_path, target_col='tfopwg_disp'):
        """Load the TOI CSV and preprocess it into X, y.

        - Automatically detects and drops very sparse columns
        - Fills missing values (median for numeric, mode for categorical)
        - Encodes low-cardinality categorical columns
        - Label-encodes the target column
        """
        print("📊 LOADING AND PREPROCESSING DATA...")

        # Read dataset (skip NASA-style comment lines that start with '#')
        df = pd.read_csv(file_path, comment='#')
        self.df = df.copy()

        if target_col not in df.columns:
            raise ValueError(f"Target column '{target_col}' not found in dataset. Available columns: {df.columns.tolist()}")

        # Separate target and features
        y = df[target_col].astype(str)
        X = df.drop(columns=[target_col])

        # Columns that are identifiers or clearly non-informative for ML
        possible_id_cols = [
            'rowid', 'toi', 'toipfx', 'tid', 'ctoi_alias', 'toi_name', 'pl_name',
            'rastr', 'decstr', 'rowupdate', 'toi_created'
        ]
        id_cols = [c for c in possible_id_cols if c in X.columns]
        if id_cols:
            X = X.drop(columns=id_cols)

        # Drop columns with too many missing values
        missing_threshold = 0.5
        missing_ratios = X.isnull().mean()
        cols_high_missing = missing_ratios[missing_ratios > missing_threshold].index.tolist()
        if cols_high_missing:
            print(f"   - Dropping {len(cols_high_missing)} columns with >{missing_threshold*100:.0f}% missing values")
            X = X.drop(columns=cols_high_missing)

        # Separate numeric and categorical
        numerical_cols = X.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()

        # Fill missing values
        for col in numerical_cols:
            if X[col].isnull().any():
                X[col] = X[col].fillna(X[col].median())
        for col in categorical_cols:
            if X[col].isnull().any():
                mode_val = X[col].mode()
                fill_val = mode_val[0] if len(mode_val) > 0 else 'Unknown'
                X[col] = X[col].fillna(fill_val)

        # Encode categorical columns with low cardinality
        for col in categorical_cols:
            try:
                if X[col].nunique() <= 10:
                    le = LabelEncoder()
                    X[col] = le.fit_transform(X[col].astype(str))
            except Exception:
                # fallback: drop problematic categorical column
                X = X.drop(columns=[col])

        # Final drop of any remaining non-numeric columns (for simplicity)
        non_numeric = X.select_dtypes(exclude=[np.number]).columns.tolist()
        if non_numeric:
            print(f"   - Dropping non-numeric columns that remain: {non_numeric}")
            X = X.drop(columns=non_numeric)

        # Encode target
        self.target_encoder = LabelEncoder()
        y_encoded = self.target_encoder.fit_transform(y)

        self.feature_names = X.columns.tolist()
        print(f"   - Final dataset: {X.shape[0]:,} rows, {X.shape[1]} features")
        print(f"   - Target classes: {self.target_encoder.classes_.tolist()}")

        return X, y_encoded

    def get_feature_explanations(self):
        """A helpful dictionary explaining common TOI/stellar/planet features.
        Add or edit entries to match the actual feature names in your CSV.
        """
        explanations = {
            'pl_pnum': "Number of planet candidates associated with the target star.",
            'pl_orbper': "Orbital period (days) — how long the candidate takes to orbit its star.",
            'pl_orbsmax': "Semi-major axis (AU) — average distance from the star.",
            'pl_rade': "Planet radius in Earth radii — estimated size of the candidate.",
            'pl_bmassj': "Planet mass in Jupiter masses (if available).",
            'st_teff': "Stellar effective temperature (K) — how hot the host star is.",
            'st_rad': "Stellar radius (Solar radii) — size of the host star.",
            'st_logg': "Stellar surface gravity — gives clues about star evolution.",
            'st_met': "Stellar metallicity — chemical composition; metal-rich stars often form more planets.",
            'toi_count': "Count of TOIs associated (system multiplicity).",
            'pl_trandep': "Transit depth (fraction) — how much starlight dims during transit.",
            'pl_trandur': "Transit duration (hours) — how long the dip lasts.",
            'pl_radj': "Planet radius in Jupiter radii (if present).",
            'ra': "Right Ascension of the target star (sky coordinate).",
            'dec': "Declination of the target star (sky coordinate).",
            'pl_tranmid': "Time of transit center — reference epoch for transit timing.",
            # Generic fallback: many TOI files reuse names similar to Kepler. Add more as needed
        }
        return explanations

    def train_model(self, X, y, test_size=0.2, random_state=42):
        """Train RandomForest and return accuracy."""
        print("\n🤖 TRAINING RANDOM FOREST MODEL...")

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )

        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        self.model = RandomForestClassifier(
            n_estimators=150,
            max_depth=12,
            random_state=random_state,
            class_weight='balanced'
        )

        self.model.fit(X_train_scaled, y_train)

        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"✅ Model Accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
        return accuracy

    def create_feature_importance_plot(self, top_n=15):
        """Plot feature importances and show textual explanations for the top features."""
        if self.model is None:
            print("Model not trained yet!")
            return None

        print(f"\n📊 CREATING FEATURE IMPORTANCE PLOT (top {top_n})")

        importance_scores = self.model.feature_importances_
        feature_importance = pd.DataFrame({
            'Feature': self.feature_names,
            'Importance': importance_scores
        }).sort_values('Importance', ascending=False)

        top_features = feature_importance.head(top_n)
        explanations = self.get_feature_explanations()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

        # Bar chart
        y_pos = np.arange(len(top_features))
        ax1.barh(y_pos, top_features['Importance'][::-1], edgecolor='black', alpha=0.8)
        ax1.set_yticks(y_pos)
        ax1.set_yticklabels(top_features['Feature'][::-1], fontsize=11)
        ax1.set_xlabel('Feature Importance', fontsize=12, fontweight='bold')
        ax1.set_title('Top Feature Importances', fontsize=14, fontweight='bold')
        ax1.invert_yaxis()
        ax1.grid(axis='x', linestyle='--', alpha=0.3)

        # Explanations panel
        ax2.axis('off')
        explanation_text = "🔍 FEATURE EXPLANATIONS:\n\n"
        for i, (_, row) in enumerate(top_features.iterrows(), 1):
            name = row['Feature']
            imp = row['Importance']
            expl = explanations.get(name, "No detailed explanation available for this feature.")
            explanation_text += f"{i}. {name} (Imp: {imp:.4f})\n   {expl}\n\n"

        ax2.text(0.01, 0.99, explanation_text, transform=ax2.transAxes, fontsize=10,
                 verticalalignment='top', family='monospace')

        plt.tight_layout()
        plt.show()

        return top_features

    def print_detailed_feature_table(self, top_n=15):
        if self.model is None:
            print("Model not trained yet!")
            return

        importance_scores = self.model.feature_importances_
        feature_importance = pd.DataFrame({
            'Feature': self.feature_names,
            'Importance': importance_scores
        }).sort_values('Importance', ascending=False)

        top_features = feature_importance.head(top_n)
        explanations = self.get_feature_explanations()

        print(f"\n📋 DETAILED FEATURE EXPLANATIONS")
        print("=" * 120)
        for i, (_, row) in enumerate(top_features.iterrows(), 1):
            name = row['Feature']
            imp = row['Importance']
            expl = explanations.get(name, "No detailed explanation available for this feature.")
            print(f"\n{i:2d}. 🎯 {name}")
            print(f"    📊 Importance: {imp:.4f}")
            print(f"    📖 Explanation: {expl}")
            print("    " + "-" * 80)

    def show_sample_predictions(self, X, y, num_samples=3):
        if self.model is None:
            print("Model not trained yet!")
            return

        print(f"\n🔮 SAMPLE PREDICTIONS (showing {num_samples} rows)")
        print("=" * 60)

        # Choose top 5 features for compact display
        importance_scores = self.model.feature_importances_
        top_features = pd.DataFrame({
            'Feature': self.feature_names,
            'Importance': importance_scores
        }).sort_values('Importance', ascending=False).head(5)['Feature'].tolist()

        # Make predictions for first num_samples rows
        for i in range(min(num_samples, len(X))):
            sample = X.iloc[[i]]
            true_label = self.target_encoder.inverse_transform([y[i]])[0]
            sample_scaled = self.scaler.transform(sample)
            proba = self.model.predict_proba(sample_scaled)[0]
            pred_idx = np.argmax(proba)
            pred_label = self.target_encoder.classes_[pred_idx]
            conf = proba[pred_idx]

            print(f"\n📝 SAMPLE {i+1}:")
            print(f"   • Actual: {true_label}")
            print(f"   • Predicted: {pred_label} (Confidence: {conf:.1%})")
            print("   • Key feature values:")
            for f in top_features:
                if f in sample.columns:
                    val = sample.iloc[0][f]
                    try:
                        print(f"     - {f}: {val:.4f}")
                    except Exception:
                        print(f"     - {f}: {val}")


def main():
    classifier = TOIExoplanetClassifier()
    file_path = 'TOI_2025.10.04_00.32.31.csv'

    try:
        X, y = classifier.load_and_preprocess(file_path, target_col='tfopwg_disp')
        accuracy = classifier.train_model(X, y)

        print("\n1) VISUALIZATION WITH EXPLANATIONS")
        top_feats = classifier.create_feature_importance_plot(top_n=15)

        print("\n2) DETAILED FEATURE TABLE")
        classifier.print_detailed_feature_table(top_n=15)

        print("\n3) SAMPLE PREDICTIONS")
        classifier.show_sample_predictions(X, y, num_samples=3)

        print("\n" + "=" * 70)
        print("🎉 ANALYSIS COMPLETE!")
        print("=" * 70)

        if top_feats is not None and len(top_feats) > 0:
            print(f"\n💡 KEY FINDINGS:")
            print(f"   • Model Accuracy: {accuracy*100:.1f}%")
            print(f"   • Most important feature: {top_feats.iloc[0]['Feature']}")
            top3_sum = top_feats.head(3)['Importance'].sum() if top_feats.shape[0] >= 3 else top_feats['Importance'].sum()
            print(f"   • Top 3 features account for {top3_sum*100:.1f}% of prediction power")

    except Exception as e:
        print(f"❌ Error during processing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
