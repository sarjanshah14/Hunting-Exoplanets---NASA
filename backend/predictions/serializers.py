from rest_framework import serializers
from .models import Prediction

class PredictionInputSerializer(serializers.Serializer):
    """Serializer for prediction input data"""
    
    # Common parameters that map across all models
    nasa_confidence = serializers.FloatField(required=False, min_value=0, max_value=1)
    signal_to_noise = serializers.FloatField(required=False, min_value=0)
    transit_depth = serializers.FloatField(required=False, min_value=0)
    orbital_period = serializers.FloatField(required=False, min_value=0)
    transit_duration = serializers.FloatField(required=False, min_value=0)
    planet_radius = serializers.FloatField(required=False, min_value=0)
    planet_temperature = serializers.FloatField(required=False, min_value=0)
    star_temperature = serializers.FloatField(required=False, min_value=0)
    star_radius = serializers.FloatField(required=False, min_value=0)
    star_mass = serializers.FloatField(required=False, min_value=0)
    distance = serializers.FloatField(required=False, min_value=0)
    
    # Flags
    flag_not_transit = serializers.BooleanField(required=False, default=False)
    flag_stellar_eclipse = serializers.BooleanField(required=False, default=False)
    flag_centroid_offset = serializers.BooleanField(required=False, default=False)
    flag_ephemeris_match = serializers.BooleanField(required=False, default=False)
    
    # Additional parameters for specific models
    impact_parameter = serializers.FloatField(required=False, min_value=0, max_value=1)
    eccentricity = serializers.FloatField(required=False, min_value=0, max_value=1)
    inclination = serializers.FloatField(required=False, min_value=0, max_value=180)
    metallicity = serializers.FloatField(required=False)
    surface_gravity = serializers.FloatField(required=False)
    age = serializers.FloatField(required=False, min_value=0)
    
    def validate(self, data):
        """Validate the input data"""
        # Check that at least some key parameters are provided
        required_fields = ['nasa_confidence', 'signal_to_noise', 'transit_depth', 'orbital_period']
        provided_fields = [field for field in required_fields if field in data and data[field] is not None]
        
        if len(provided_fields) < 2:
            raise serializers.ValidationError(
                "At least 2 of the following parameters must be provided: "
                "nasa_confidence, signal_to_noise, transit_depth, orbital_period"
            )
        
        return data

class PredictionResultSerializer(serializers.Serializer):
    """Serializer for prediction results"""
    status = serializers.CharField(max_length=20)
    confidence = serializers.FloatField()
    explanation = serializers.CharField()
    probabilities = serializers.DictField()
    feature_importance = serializers.ListField(required=False)

class PredictionSerializer(serializers.ModelSerializer):
    """Serializer for saved predictions"""
    
    class Meta:
        model = Prediction
        fields = ['id', 'timestamp', 'model_name', 'input_data', 
                 'predicted_status', 'confidence', 'probabilities']
        read_only_fields = ['id', 'timestamp']
