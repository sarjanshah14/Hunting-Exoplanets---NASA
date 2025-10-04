import joblib
import pandas as pd
import numpy as np

class ExoplanetPredictor:
    def __init__(self):
        try:
            # Load our trained components
            self.model = joblib.load('exoplanet_predictor.pkl')
            self.scaler = joblib.load('feature_scaler.pkl')
            self.target_encoder = joblib.load('target_encoder.pkl')
            self.top_features = joblib.load('important_features.pkl')

            # Load medians from training data (you can also pre-save a medians.pkl)
            df = pd.read_csv('cleaned_kepler_train.csv')
            self.medians = df.median(numeric_only=True).to_dict()

            print("✅ Model and dependencies loaded successfully!")

        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model = None
            self.medians = {}

    # -------------------------------------------------------------------------
    def prepare_features(self, input_features):
        """Ensure all required features exist and fill missing ones safely"""
        if self.model is None:
            return np.array([])

        required = self.model.feature_names_in_
        missing = set(required) - set(input_features.keys())

        # Fill missing numeric features with median of training set
        for col in missing:
            if col in self.medians:
                input_features[col] = self.medians[col]
            else:
                input_features[col] = 0  # safe default for unknowns

        # Reorder features to match model input
        ordered = [input_features[f] for f in required]
        return np.array(ordered).reshape(1, -1)

    # -------------------------------------------------------------------------
    def predict(self, input_data):
        if self.model is None:
            return self._dummy_prediction(input_data)

        try:
            # Convert to DataFrame for flexible handling
            input_df = pd.DataFrame([input_data])

            # Fill missing columns using medians
            for col in self.top_features:
                if col not in input_df.columns:
                    input_df[col] = self.medians.get(col, 0)

            # Select and scale features
            X_input = input_df[self.top_features]
            X_scaled = self.scaler.transform(X_input)

            # Predict
            prediction = self.model.predict(X_scaled)[0]
            probabilities = self.model.predict_proba(X_scaled)[0]

            # Decode target
            predicted_class = self.target_encoder.inverse_transform([prediction])[0]
            confidence = float(max(probabilities))

            class_probabilities = {
                self.target_encoder.classes_[i]: float(prob)
                for i, prob in enumerate(probabilities)
            }

            return {
                "prediction": predicted_class,
                "confidence": confidence,
                "probabilities": class_probabilities,
                "status": "success"
            }

        except Exception as e:
            return {"error": str(e), "status": "error"}

    # -------------------------------------------------------------------------
    def _dummy_prediction(self, input_data):
        """Fallback dummy mode"""
        koi_score = input_data.get('koi_score', 0.5)

        if koi_score > 0.8:
            return {
                "prediction": "CONFIRMED",
                "confidence": 0.967,
                "probabilities": {
                    "CONFIRMED": 0.967,
                    "CANDIDATE": 0.028,
                    "FALSE POSITIVE": 0.005
                },
                "status": "success",
                "note": "Using demo mode"
            }
        elif koi_score > 0.5:
            return {
                "prediction": "CANDIDATE",
                "confidence": 0.723,
                "probabilities": {
                    "CONFIRMED": 0.201,
                    "CANDIDATE": 0.723,
                    "FALSE POSITIVE": 0.076
                },
                "status": "success",
                "note": "Using demo mode"
            }
        else:
            return {
                "prediction": "FALSE POSITIVE",
                "confidence": 0.891,
                "probabilities": {
                    "CONFIRMED": 0.034,
                    "CANDIDATE": 0.075,
                    "FALSE POSITIVE": 0.891
                },
                "status": "success",
                "note": "Using demo mode"
            }


# -------------------------------------------------------------------------
# ✅ Local Test
if __name__ == "__main__":
    predictor = ExoplanetPredictor()

    test_input = {
        'koi_score': 0.98,
        'koi_fpflag_nt': 0,
        'koi_fpflag_ss': 0,
        'koi_depth': 1250,
        'koi_period': 365.25,
        'koi_model_snr': 18.5,
        'koi_fpflag_co': 0,
        'koi_duration': 8.2,
        'koi_teq': 288,
        'koi_fpflag_ec': 0,
        'koi_steff': 5780,
        'koi_impact': 0.15,
        'koi_ror': 0.0087,
        'koi_sma': 1.0,
        'koi_slogg': 4.44
    }

    result = predictor.predict(test_input)
    print("\n🔮 PREDICTION RESULT:")
    print(f"Planet Type: {result.get('prediction')}")
    print(f"Confidence: {result.get('confidence', 0):.1%}")
    print("Probabilities:")
    for planet_type, prob in result.get('probabilities', {}).items():
        print(f"  {planet_type}: {prob:.1%}")
