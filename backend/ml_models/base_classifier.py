import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

class BaseExoplanetClassifier:
    """Base class for exoplanet classification models"""
    
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = None
        self.scaler = None
        self.target_encoder = None
        self.feature_names = None
        self.is_trained = False
        
    def load_data(self, file_path):
        """Load dataset from CSV file"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Data file not found: {file_path}")
        
        df = pd.read_csv(file_path, comment='#')
        return df
    
    def preprocess_data(self, df, target_column):
        """Preprocess the dataset"""
        # Drop rows where target is missing
        df = df.dropna(subset=[target_column])
        
        # Separate features and target
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        # Remove identifier columns
        id_cols = [col for col in X.columns if col.lower() in 
                  ['id', 'kepid', 'rowid', 'index', 'kepoi_name', 'kepler_name', 'toi', 'toi_name']]
        if id_cols:
            X = X.drop(columns=id_cols)
        
        # Handle missing values
        numerical_cols = X.select_dtypes(include=[np.number]).columns
        categorical_cols = X.select_dtypes(include=['object']).columns
        
        # Fill missing values
        X[numerical_cols] = X[numerical_cols].fillna(X[numerical_cols].median())
        X[categorical_cols] = X[categorical_cols].fillna('Unknown')
        
        # Encode categorical columns
        for col in categorical_cols:
            if X[col].nunique() <= 10:
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].astype(str))
        
        # Encode target
        self.target_encoder = LabelEncoder()
        y_encoded = self.target_encoder.fit_transform(y)
        
        self.feature_names = X.columns.tolist()
        return X, y_encoded
    
    def train_model(self, X, y):
        """Train the Random Forest model"""
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
        
        self.is_trained = True
        return accuracy
    
    def predict(self, input_data):
        """Make prediction on input data"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Convert input to DataFrame
        if isinstance(input_data, dict):
            input_df = pd.DataFrame([input_data])
        else:
            input_df = input_data
        
        # Ensure all required features are present
        missing_features = set(self.feature_names) - set(input_df.columns)
        if missing_features:
            raise ValueError(f"Missing features: {missing_features}")
        
        # Select only the features used in training
        input_df = input_df[self.feature_names]
        
        # Scale the input
        input_scaled = self.scaler.transform(input_df)
        
        # Make prediction
        prediction_proba = self.model.predict_proba(input_scaled)[0]
        predicted_class_idx = np.argmax(prediction_proba)
        predicted_class = self.target_encoder.classes_[predicted_class_idx]
        confidence = prediction_proba[predicted_class_idx]
        
        return {
            'predicted_class': predicted_class,
            'confidence': float(confidence),
            'probabilities': {
                class_name: float(prob) 
                for class_name, prob in zip(self.target_encoder.classes_, prediction_proba)
            }
        }
    
    def get_feature_importance(self, top_n=10):
        """Get feature importance scores"""
        if not self.is_trained:
            raise ValueError("Model must be trained before getting feature importance")
        
        importance_scores = self.model.feature_importances_
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': importance_scores
        }).sort_values('importance', ascending=False)
        
        return feature_importance.head(top_n).to_dict('records')
