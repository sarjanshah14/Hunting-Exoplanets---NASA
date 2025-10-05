import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

print("🔭 EXOPLANET CLASSIFICATION - CLEAR FEATURE EXPLANATIONS")
print("=" * 60)

class ExoplanetClassifier:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.target_encoder = None
        self.feature_names = None
        
    def load_and_preprocess(self, file_path):
        """Load and preprocess the data"""
        print("📊 LOADING AND PREPROCESSING DATA...")
        
        # Load the dataset
        self.df = pd.read_csv(file_path, comment='#')
        
        # Define target variable
        target = 'koi_disposition'
        y = self.df[target]
        X = self.df.drop(columns=[target])
        
        # Remove problematic columns
        columns_to_remove = [
            'kepid', 'kepoi_name', 'kepler_name', 'koi_comment',
            'koi_datalink_dvr', 'koi_datalink_dvs', 'koi_tce_delivname',
            'koi_vet_date', 'koi_disp_prov', 'koi_parm_prov', 'koi_sparprov',
            'rowid'
        ]
        columns_to_remove = [col for col in columns_to_remove if col in X.columns]
        X = X.drop(columns=columns_to_remove)
        
        # Remove high missing columns
        missing_threshold = 0.5
        missing_ratios = X.isnull().mean()
        columns_to_drop = missing_ratios[missing_ratios > missing_threshold].index
        X = X.drop(columns=columns_to_drop)
        
        # Fill missing values
        numerical_cols = X.select_dtypes(include=[np.number]).columns
        categorical_cols = X.select_dtypes(include=['object']).columns
        
        for col in numerical_cols:
            X[col] = X[col].fillna(X[col].median())
        for col in categorical_cols:
            X[col] = X[col].fillna(X[col].mode()[0] if len(X[col].mode()) > 0 else 'Unknown')
        
        # Encode categorical variables
        for col in categorical_cols:
            if X[col].nunique() <= 10:
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].astype(str))
        
        # Encode target
        self.target_encoder = LabelEncoder()
        y_encoded = self.target_encoder.fit_transform(y)
        
        self.feature_names = X.columns.tolist()
        
        return X, y_encoded
    
    def get_feature_explanations(self):
        """Return detailed explanations for features"""
        explanations = {
            'koi_score': "NASA's Confidence Score (0-1): How confident NASA is that this is a real planet. Higher = more reliable.",
            'koi_fpflag_nt': "Not Transit Flag (0/1): 1 means it doesn't look like a planet transit (probably false positive).",
            'koi_fpflag_ss': "Stellar Eclipse Flag (0/1): 1 means it's likely binary stars eclipsing, not a planet.",
            'koi_depth': "Transit Depth (ppm): How much the star dims when object passes. Deeper = larger object.",
            'koi_period': "Orbital Period (days): How long it takes to orbit the star. Shorter = closer to star.",
            'koi_model_snr': "Signal-to-Noise Ratio: How clear the detection is. Higher = more reliable signal.",
            'koi_fpflag_co': "Centroid Offset Flag (0/1): 1 means signal comes from different star, not the target.",
            'koi_duration': "Transit Duration (hours): How long the dimming lasts. Affected by orbit geometry.",
            'koi_teq': "Planet Temperature (K): Estimated temperature. Hotter = closer to star.",
            'koi_fpflag_ec': "Ephemeris Match Flag (0/1): 1 matches known instrument errors (false positive).",
            'koi_steff': "Star Temperature (K): Temperature of the host star.",
            'koi_impact': "Impact Parameter: How centrally it transits (0=center, 1=edge).",
            'koi_ror': "Planet/Star Size Ratio: Relative sizes. Larger = bigger planet or smaller star.",
            'koi_sma': "Orbit Distance (AU): Distance from star. 1 AU = Earth-Sun distance.",
            'koi_slogg': "Star Surface Gravity: Indicates star's evolutionary stage.",
            'koi_prad': "Planet Radius (Earth radii): Estimated size of the candidate planet.",
            'koi_insol': "Stellar Flux: Amount of energy received from star.",
            'koi_srad': "Star Radius (Solar radii): Size of the host star.",
            'koi_smet': "Star Metallicity: Chemical composition. Metal-rich stars may form more planets.",
            'koi_incl': "Orbital Inclination: Orbit angle relative to our view. 90° = perfect for detection.",
            'koi_num_transits': "Number of Transits: How many times observed. More = more reliable.",
            'koi_count': "Planets in System: Number of candidate planets in this star system.",
            'koi_max_sngle_ev': "Single Event Significance: Strength of strongest individual transit.",
            'koi_max_mult_ev': "Multiple Event Significance: Combined strength of all transits.",
            'koi_bin_oedp_sig': "Odd-Even Test: Checks if alternate transits differ (binary star indicator)."
        }
        return explanations
    
    def train_model(self, X, y):
        """Train the Random Forest model"""
        print("🤖 TRAINING MODEL...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"✅ Model Accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
        
        return accuracy
    
    def create_feature_importance_plot(self, top_n=15):
        """Create feature importance plot with explanations"""
        if self.model is None:
            print("Model not trained yet!")
            return
        
        print(f"\n📊 CREATING FEATURE IMPORTANCE PLOT")
        print("=" * 60)
        
        # Get feature importance
        importance_scores = self.model.feature_importances_
        feature_importance = pd.DataFrame({
            'Feature': self.feature_names,
            'Importance': importance_scores
        }).sort_values('Importance', ascending=False)
        
        # Get top features
        top_features = feature_importance.head(top_n)
        explanations = self.get_feature_explanations()
        
        # Create the plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
        
        # Plot 1: Feature importance bars
        y_pos = np.arange(len(top_features))
        colors = plt.cm.plasma(np.linspace(0, 1, len(top_features)))
        
        bars = ax1.barh(y_pos, top_features['Importance'], color=colors, alpha=0.7)
        
        ax1.set_yticks(y_pos)
        ax1.set_yticklabels(top_features['Feature'], fontsize=11)
        ax1.set_xlabel('Feature Importance Score', fontsize=12, fontweight='bold')
        ax1.set_title(f'Top {top_n} Most Important Features\nfor Exoplanet Classification', 
                     fontsize=14, fontweight='bold')
        ax1.grid(axis='x', alpha=0.3, linestyle='--')
        ax1.invert_yaxis()
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax1.text(width + 0.001, bar.get_y() + bar.get_height()/2, 
                    f'{width:.3f}', ha='left', va='center', fontsize=9,
                    fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        # Plot 2: Feature explanations
        ax2.axis('off')
        
        # Create explanation text
        explanation_text = "🔍 FEATURE EXPLANATIONS:\n\n"
        
        for i, (_, row) in enumerate(top_features.iterrows(), 1):
            feature_name = row['Feature']
            importance = row['Importance']
            explanation = explanations.get(feature_name, "No detailed explanation available")
            
            explanation_text += f"{i}. {feature_name} (Imp: {importance:.4f})\n"
            explanation_text += f"   📖 {explanation}\n\n"
        
        ax2.text(0.02, 0.98, explanation_text, transform=ax2.transAxes, fontsize=10,
                verticalalignment='top', linespacing=1.5, fontfamily='monospace')
        
        ax2.set_title('What These Features Mean', fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.show()
        
        return top_features
    
    def print_detailed_feature_table(self, top_n=15):
        """Print a detailed table of top features"""
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
            feature_name = row['Feature']
            importance = row['Importance']
            explanation = explanations.get(feature_name, "No detailed explanation available")
            
            print(f"\n{i:2d}. 🎯 {feature_name}")
            print(f"    📊 Importance: {importance:.4f}")
            print(f"    📖 Explanation: {explanation}")
            print(f"    {'-' * 80}")
    
    def show_sample_predictions(self, X, y, num_samples=3):
        """Show sample predictions with feature values"""
        if self.model is None:
            print("Model not trained yet!")
            return
        
        print(f"\n🔮 SAMPLE PREDICTIONS WITH FEATURE VALUES")
        print("=" * 60)
        
        # Get top 5 features for display
        importance_scores = self.model.feature_importances_
        top_features = pd.DataFrame({
            'Feature': self.feature_names,
            'Importance': importance_scores
        }).sort_values('Importance', ascending=False).head(5)['Feature'].tolist()
        
        for i in range(min(num_samples, len(X))):
            sample_data = X.iloc[[i]].copy()
            actual_class = self.target_encoder.inverse_transform([y[i]])[0]
            
            # Scale and predict
            sample_scaled = self.scaler.transform(sample_data)
            prediction_proba = self.model.predict_proba(sample_scaled)[0]
            predicted_class_idx = np.argmax(prediction_proba)
            predicted_class = self.target_encoder.classes_[predicted_class_idx]
            confidence = prediction_proba[predicted_class_idx]
            
            print(f"\n📝 SAMPLE {i+1}:")
            print(f"   • Actual: {actual_class}")
            print(f"   • Predicted: {predicted_class} (Confidence: {confidence:.1%})")
            
            print(f"   • Key Feature Values:")
            for feature in top_features:
                if feature in sample_data.columns:
                    value = sample_data[feature].values[0]
                    print(f"     - {feature}: {value:.3f}")

def main():
    """Main function"""
    
    # Initialize classifier
    classifier = ExoplanetClassifier()
    
    try:
        # Load and preprocess data
        X, y = classifier.load_and_preprocess('cumulative_2025.10.04_00.32.09.csv')
        
        print(f"✅ Data ready: {X.shape[0]:,} objects, {X.shape[1]} features")
        print(f"🎯 Target classes: {classifier.target_encoder.classes_.tolist()}")
        
        # Train model
        accuracy = classifier.train_model(X, y)
        
        # Create visualization with explanations
        print(f"\n1. 📊 VISUALIZATION WITH EXPLANATIONS")
        top_features = classifier.create_feature_importance_plot(top_n=15)
        
        # Print detailed table
        print(f"\n2. 📋 DETAILED FEATURE EXPLANATIONS")
        classifier.print_detailed_feature_table(top_n=15)
        
        # Show sample predictions
        print(f"\n3. 🔮 SAMPLE PREDICTIONS")
        classifier.show_sample_predictions(X, y, num_samples=2)
        
        print("\n" + "=" * 60)
        print("🎉 ANALYSIS COMPLETE!")
        print("=" * 60)
        print(f"\n💡 KEY FINDINGS:")
        print(f"   • Model Accuracy: {accuracy*100:.1f}%")
        print(f"   • Most important feature: {top_features.iloc[0]['Feature']}")
        print(f"   • Top 3 features account for {top_features.head(3)['Importance'].sum()*100:.1f}% of prediction power")
        print(f"\n🔭 What this means:")
        print(f"   • NASA's confidence scores are the best predictors")
        print(f"   • False positive flags are crucial for filtering")
        print(f"   • The model learned to trust NASA's expertise")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()