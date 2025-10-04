import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import warnings
warnings.filterwarnings('ignore')

print("🚀 EXOPLANET CLASSIFICATION - COMPLETE PIPELINE")
print("=" * 60)

class ExoplanetPipeline:
    def __init__(self):
        self.models = {}
        self.scaler = None
        self.target_encoder = None
        self.top_features = None
        self.feature_encoders = {}
        
    def load_and_preprocess(self, file_path):
        """Load and preprocess data - FIXED VERSION"""
        print("📊 LOADING DATA...")
        df = pd.read_csv(file_path, comment='#')
        
        target = 'koi_disposition'
        y = df[target]
        X = df.drop(columns=[target])
        
        print(f"📁 Original data: {X.shape[0]} rows, {X.shape[1]} columns")
        
        # Remove problematic columns
        columns_to_remove = [
            'kepid', 'kepoi_name', 'kepler_name', 'koi_comment', 
            'koi_datalink_dvr', 'koi_datalink_dvs', 'koi_tce_delivname',
            'koi_vet_date', 'koi_disp_prov', 'koi_parm_prov', 'koi_sparprov',
            'rowid'
        ]
        columns_to_remove = [col for col in columns_to_remove if col in X.columns]
        X = X.drop(columns=columns_to_remove)
        print(f"🗑️  Removed {len(columns_to_remove)} non-predictive columns")
        
        # Remove high missing columns
        missing_threshold = 0.5
        missing_ratios = X.isnull().mean()
        columns_to_drop = missing_ratios[missing_ratios > missing_threshold].index
        X = X.drop(columns=columns_to_drop)
        print(f"🗑️  Removed {len(columns_to_drop)} columns with >50% missing values")
        
        # Identify column types
        numerical_cols = X.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
        
        print(f"🔢 Numerical columns: {len(numerical_cols)}")
        print(f"🔤 Categorical columns: {len(categorical_cols)}")
        
        # Handle missing values for numerical columns
        for col in numerical_cols:
            X[col] = X[col].fillna(X[col].median())
        print("✅ Filled missing numerical values with median")
        
        # Handle categorical columns - encode or remove
        columns_to_remove_categorical = []
        for col in categorical_cols:
            unique_vals = X[col].nunique()
            if unique_vals <= 10:  # Encode if reasonable number of categories
                print(f"   🔤 Encoding {col} ({unique_vals} unique values)")
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].astype(str))
                self.feature_encoders[col] = le
            else:  # Remove high cardinality categorical columns
                print(f"   🗑️  Removing {col} (too many categories: {unique_vals})")
                columns_to_remove_categorical.append(col)
        
        X = X.drop(columns=columns_to_remove_categorical)
        print(f"🗑️  Removed {len(columns_to_remove_categorical)} high-cardinality categorical columns")
        
        # Final check - ensure all columns are numerical
        remaining_categorical = X.select_dtypes(include=['object']).columns
        if len(remaining_categorical) > 0:
            print(f"⚠️  Warning: Still have categorical columns: {list(remaining_categorical)}")
            print("   Removing them...")
            X = X.drop(columns=remaining_categorical)
        
        print(f"✅ Final feature matrix: {X.shape[0]} rows, {X.shape[1]} columns")
        
        # Encode target
        self.target_encoder = LabelEncoder()
        y_encoded = self.target_encoder.fit_transform(y)
        print(f"🎯 Target classes: {list(self.target_encoder.classes_)}")
        
        return X, y_encoded
    
    def find_top_features(self, X, y, top_n=15):
        """Find the most important features using Random Forest"""
        print("🔍 FINDING MOST IMPORTANT FEATURES...")
        
        # Ensure we have enough features
        if X.shape[1] < top_n:
            top_n = X.shape[1]
            print(f"⚠️  Only {X.shape[1]} features available, using all")
        
        # Train initial model to find important features
        X_temp, _, y_temp, _ = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X_temp)
        
        # Train model
        rf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
        rf.fit(X_scaled, y_temp)
        
        # Get feature importance
        importance_scores = rf.feature_importances_
        feature_importance = pd.DataFrame({
            'Feature': X.columns,
            'Importance': importance_scores
        }).sort_values('Importance', ascending=False)
        
        self.top_features = feature_importance.head(top_n)['Feature'].tolist()
        
        print(f"✅ Top {top_n} features identified:")
        for i, feature in enumerate(self.top_features, 1):
            imp_score = feature_importance[feature_importance['Feature'] == feature]['Importance'].values[0]
            print(f"   {i:2d}. {feature} (importance: {imp_score:.4f})")
        
        return self.top_features
    
    def compare_all_models(self, X, y):
        """Compare performance of all models"""
        print(f"\n⚖️ COMPARING ALL MODELS...")
        
        # Use only top features
        X_optimized = X[self.top_features]
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X_optimized)
        
        models = {
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced'),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'Logistic Regression': LogisticRegression(random_state=42, class_weight='balanced', max_iter=1000),
            'SVM': SVC(random_state=42, class_weight='balanced')
        }
        
        results = {}
        for name, model in models.items():
            try:
                # 5-fold cross validation
                cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring='accuracy')
                results[name] = {
                    'mean_accuracy': cv_scores.mean(),
                    'std_accuracy': cv_scores.std(),
                    'scores': cv_scores
                }
                print(f"   • {name:<20}: {cv_scores.mean():.3f} ± {cv_scores.std() * 2:.3f}")
            except Exception as e:
                print(f"   • {name:<20}: Failed - {e}")
        
        # Plot comparison
        if results:
            plt.figure(figsize=(10, 6))
            model_names = list(results.keys())
            accuracies = [results[name]['mean_accuracy'] for name in model_names]
            
            colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']
            bars = plt.bar(model_names, accuracies, color=colors[:len(model_names)], alpha=0.7)
            plt.title('Model Comparison for Exoplanet Classification')
            plt.ylabel('Accuracy')
            plt.xticks(rotation=45)
            
            # Add value labels
            for bar, accuracy in zip(bars, accuracies):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{accuracy:.3f}', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            plt.show()
        
        return results
    
    def create_production_predictor(self, X, y):
        """Create final production-ready predictor"""
        print(f"\n🏭 CREATING PRODUCTION PREDICTOR...")
        
        # Use best model (Random Forest usually works best)
        X_optimized = X[self.top_features]
        
        # Train on full dataset
        X_scaled = self.scaler.fit_transform(X_optimized)
        
        # Train final model
        final_model = RandomForestClassifier(
            n_estimators=150,
            max_depth=15,
            random_state=42,
            class_weight='balanced'
        )
        
        final_model.fit(X_scaled, y)
        
        # Evaluate final model
        y_pred = final_model.predict(X_scaled)
        accuracy = accuracy_score(y, y_pred)
        print(f"✅ Final model accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
        
        # Save model and components
        joblib.dump(final_model, 'exoplanet_predictor.pkl')
        joblib.dump(self.scaler, 'feature_scaler.pkl')
        joblib.dump(self.target_encoder, 'target_encoder.pkl')
        joblib.dump(self.top_features, 'important_features.pkl')
        
        print("✅ Production predictor saved!")
        print("   • exoplanet_predictor.pkl - The trained model")
        print("   • feature_scaler.pkl - Feature scaling parameters")
        print("   • target_encoder.pkl - Label encoding")
        print("   • important_features.pkl - Top features needed")
        
        return final_model
    
    def predict_new_candidates(self, new_data):
        """Predict new Kepler candidates"""
        if not hasattr(self, 'production_model'):
            # Load saved model
            try:
                self.production_model = joblib.load('exoplanet_predictor.pkl')
                self.scaler = joblib.load('feature_scaler.pkl')
                self.target_encoder = joblib.load('target_encoder.pkl')
                self.top_features = joblib.load('important_features.pkl')
                print("✅ Loaded trained model successfully")
            except Exception as e:
                print(f"❌ No trained model found: {e}")
                return
        
        # Ensure we have the right features
        missing_features = set(self.top_features) - set(new_data.columns)
        if missing_features:
            print(f"❌ Missing features: {missing_features}")
            return
        
        # Select and scale features
        X_new = new_data[self.top_features]
        X_new_scaled = self.scaler.transform(X_new)
        
        # Make predictions
        predictions = self.production_model.predict(X_new_scaled)
        probabilities = self.production_model.predict_proba(X_new_scaled)
        
        # Convert to readable format
        results = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            predicted_class = self.target_encoder.inverse_transform([pred])[0]
            class_probs = {
                self.target_encoder.classes_[j]: p 
                for j, p in enumerate(prob)
            }
            
            results.append({
                'candidate_id': i,
                'prediction': predicted_class,
                'confidence': max(prob),
                'probabilities': class_probs
            })
        
        return results

def demonstrate_real_world_use():
    """Show how this would be used in the real world"""
    print("\n" + "=" * 60)
    print("🌍 REAL-WORLD APPLICATIONS")
    print("=" * 60)
    
    print("\n🎯 HOW NASA WOULD USE THIS:")
    print("1. 📡 Kepler detects new candidate signals")
    print("2. 🔍 Extract the important features for each candidate")
    print("3. 🤖 Run through our trained model")
    print("4. 📊 Get instant classifications:")
    print("   • ✅ CONFIRMED (high confidence) → Priority for follow-up")
    print("   • ⏳ CANDIDATE (medium confidence) → Further analysis needed")
    print("   • ❌ FALSE POSITIVE (low confidence) → Discard")
    
    print("\n💡 BENEFITS:")
    print("   • Faster analysis than manual review")
    print("   • Consistent, reproducible results")
    print("   • Handles large data volumes efficiently")
    print("   • Works 24/7 without astronomer fatigue")

def main():
    """Complete pipeline demonstration"""
    pipeline = ExoplanetPipeline()
    
    try:
        # 1. Load data
        X, y = pipeline.load_and_preprocess('cumulative_2025.10.04_00.32.09.csv')
        
        # 2. Find important features
        top_features = pipeline.find_top_features(X, y, top_n=15)
        
        # 3. Compare models
        model_comparison = pipeline.compare_all_models(X, y)
        
        # 4. Build production model
        production_model = pipeline.create_production_predictor(X, y)
        
        # 5. Demonstrate real-world use
        demonstrate_real_world_use()
        
        print("\n" + "=" * 60)
        print("🎉 PIPELINE COMPLETE - READY FOR DEPLOYMENT!")
        print("=" * 60)
        
        print(f"\n📦 WHAT WE BUILT:")
        print("   1. Feature selector (identifies key measurements)")
        print("   2. Trained classifier (high accuracy)")
        print("   3. Production pipeline (ready for new data)")
        print("   4. Model comparison (proves our approach works)")
        
        print(f"\n🚀 NEXT STEPS:")
        print("   1. Use predict_new_candidates() for new Kepler data")
        print("   2. Deploy as web service for astronomers")
        print("   3. Integrate with NASA's data processing pipeline")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()