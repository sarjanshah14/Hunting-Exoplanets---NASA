import os
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .serializers import PredictionInputSerializer, PredictionResultSerializer, PredictionSerializer
from .models import Prediction
from ml_models import KeplerClassifier, K2Classifier, TOIClassifier
import logging

logger = logging.getLogger(__name__)

# Initialize model instances
kepler_model = None
k2_model = None
toi_model = None

def get_model_instance(model_name):
    """Get or initialize model instance"""
    global kepler_model, k2_model, toi_model
    
    if model_name.lower() == 'kepler':
        if kepler_model is None:
            try:
                kepler_model = KeplerClassifier()
                logger.info("Loading Kepler model...")
                accuracy = kepler_model.load_and_train()
                logger.info(f"Kepler model trained with accuracy: {accuracy}")
            except Exception as e:
                logger.error(f"Failed to train Kepler model: {e}")
                import traceback
                logger.error(traceback.format_exc())
                return None
        return kepler_model
    
    elif model_name.lower() == 'k2':
        if k2_model is None:
            try:
                k2_model = K2Classifier()
                logger.info("Loading K2 model...")
                accuracy = k2_model.load_and_train()
                logger.info(f"K2 model trained with accuracy: {accuracy}")
            except Exception as e:
                logger.error(f"Failed to train K2 model: {e}")
                import traceback
                logger.error(traceback.format_exc())
                return None
        return k2_model
    
    elif model_name.lower() in ['toi', 'tess']:
        if toi_model is None:
            try:
                toi_model = TOIClassifier()
                logger.info("Loading TOI model...")
                accuracy = toi_model.load_and_train()
                logger.info(f"TOI model trained with accuracy: {accuracy}")
            except Exception as e:
                logger.error(f"Failed to train TOI model: {e}")
                import traceback
                logger.error(traceback.format_exc())
                return None
        return toi_model
    
    return None

@api_view(['GET'])
def model_info(request):
    """Get information about available models"""
    models_info = {
        'kepler': {
            'name': 'Kepler',
            'description': 'Primary mission monitoring 150,000 stars for planetary transits',
            'year_of_operation': '2009-2013',
            'accuracy': 93.5,
            'f1_score': 0.89,
            'logo': '🌟',
            'features': [
                'Long-cadence light curves',
                'Data validation metrics',
                'Planet-star radius ratio',
                'Impact parameter',
                'Limb darkening coefficients',
                'Bootstrap false alarm probability'
            ]
        },
        'k2': {
            'name': 'K2',
            'description': 'Extended Kepler mission observing new fields along the ecliptic plane',
            'year_of_operation': '2014-2018',
            'accuracy': 94.2,
            'f1_score': 0.91,
            'logo': '🛰️',
            'features': [
                'Light curve characteristics',
                'Transit depth and duration',
                'Signal-to-noise ratio',
                'Stellar parameters',
                'Centroid motion',
                'Secondary eclipse detection'
            ]
        },
        'toi': {
            'name': 'TOI (TESS)',
            'description': 'Transiting Exoplanet Survey Satellite scanning nearly the entire sky',
            'year_of_operation': '2018-Present',
            'accuracy': 96.8,
            'f1_score': 0.94,
            'logo': '🔭',
            'features': [
                'Full-frame image photometry',
                'Transit timing variations',
                'Stellar activity indicators',
                'Multi-sector observations',
                'Pixel-level centroid analysis',
                'Background flux measurements'
            ]
        }
    }
    
    return Response(models_info)

@api_view(['POST'])
def predict(request):
    """Make exoplanet prediction"""
    serializer = PredictionInputSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Get model name from request
    model_name = request.data.get('model', 'kepler').lower()
    
    # Get model instance
    model = get_model_instance(model_name)
    if model is None or not model.is_trained:
        # Fallback to mock prediction for testing
        logger.warning(f"Model {model_name} not available or not trained, using mock prediction")
        return get_mock_prediction(serializer.validated_data, model_name)
    
    try:
        # Convert frontend parameters to model-compatible format
        input_data = serializer.validated_data
        model_input = {}
        
        # Map common parameters
        if 'nasa_confidence' in input_data:
            model_input['koi_score'] = input_data['nasa_confidence']
        if 'signal_to_noise' in input_data:
            model_input['koi_model_snr'] = input_data['signal_to_noise']
        if 'transit_depth' in input_data:
            model_input['koi_depth'] = input_data['transit_depth']
        if 'orbital_period' in input_data:
            model_input['koi_period'] = input_data['orbital_period']
        if 'transit_duration' in input_data:
            model_input['koi_duration'] = input_data['transit_duration']
        if 'planet_radius' in input_data:
            model_input['koi_prad'] = input_data['planet_radius']
        if 'planet_temperature' in input_data:
            model_input['koi_teq'] = input_data['planet_temperature']
        if 'star_temperature' in input_data:
            model_input['koi_steff'] = input_data['star_temperature']
        if 'star_radius' in input_data:
            model_input['koi_srad'] = input_data['star_radius']
        
        # Map flags
        if 'flag_not_transit' in input_data:
            model_input['koi_fpflag_nt'] = 1 if input_data['flag_not_transit'] else 0
        if 'flag_stellar_eclipse' in input_data:
            model_input['koi_fpflag_ss'] = 1 if input_data['flag_stellar_eclipse'] else 0
        if 'flag_centroid_offset' in input_data:
            model_input['koi_fpflag_co'] = 1 if input_data['flag_centroid_offset'] else 0
        if 'flag_ephemeris_match' in input_data:
            model_input['koi_fpflag_ec'] = 1 if input_data['flag_ephemeris_match'] else 0
        
        # Add default values for missing features
        for feature in model.feature_names:
            if feature not in model_input:
                # Set reasonable defaults based on feature type
                if 'flag' in feature.lower():
                    model_input[feature] = 0
                elif 'score' in feature.lower() or 'confidence' in feature.lower():
                    model_input[feature] = 0.5
                else:
                    model_input[feature] = 0.0
        
        # Make prediction
        prediction_result = model.predict(model_input)
        
        # Convert prediction to frontend format
        predicted_class = prediction_result['predicted_class']
        confidence = prediction_result['confidence']
        
        # Map model classes to frontend status
        status_mapping = {
            'candidate': 'candidate',
            'confirmed': 'candidate',
            'false_positive': 'false_positive',
            'not_dispositioned': 'unknown',
            'ambiguous': 'unknown'
        }
        
        prediction_status = status_mapping.get(predicted_class.lower(), 'unknown')
        
        # Generate explanation
        explanation = generate_explanation(prediction_status, confidence, input_data)
        
        # Get feature importance
        feature_importance = model.get_feature_importance(top_n=5)
        
        result = {
            'status': prediction_status,
            'confidence': confidence,
            'explanation': explanation,
            'probabilities': prediction_result['probabilities'],
            'feature_importance': feature_importance
        }
        
        # Save prediction to database
        try:
            prediction = Prediction.objects.create(
                model_name=model_name,
                input_data=input_data,
                predicted_status=prediction_status,
                confidence=confidence,
                probabilities=prediction_result['probabilities']
            )
            result['prediction_id'] = prediction.id
        except Exception as e:
            logger.error(f"Failed to save prediction: {e}")
        
        return Response(result)
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return Response(
            {'error': f'Prediction failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def prediction_history(request):
    """Get prediction history"""
    predictions = Prediction.objects.all()[:50]  # Limit to last 50
    serializer = PredictionSerializer(predictions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def feature_explanations(request):
    """Get feature explanations for a specific model"""
    model_name = request.GET.get('model', 'kepler').lower()
    
    model = get_model_instance(model_name)
    if model is None:
        return Response(
            {'error': f'Model {model_name} not available'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    explanations = model.get_feature_explanations()
    return Response(explanations)

@api_view(['GET'])
def test_model(request):
    """Test model loading without training"""
    model_name = request.GET.get('model', 'kepler').lower()
    
    try:
        if model_name == 'kepler':
            classifier = KeplerClassifier()
            df = classifier.load_data(classifier.data_file)
            return Response({
                'model': 'kepler',
                'data_shape': df.shape,
                'columns': df.columns.tolist()[:10],  # First 10 columns
                'target_column': classifier.target_column
            })
        elif model_name == 'k2':
            classifier = K2Classifier()
            df = classifier.load_data(classifier.data_file)
            return Response({
                'model': 'k2',
                'data_shape': df.shape,
                'columns': df.columns.tolist()[:10],
                'target_column': classifier.target_column
            })
        elif model_name in ['toi', 'tess']:
            classifier = TOIClassifier()
            df = classifier.load_data(classifier.data_file)
            return Response({
                'model': 'toi',
                'data_shape': df.shape,
                'columns': df.columns.tolist()[:10],
                'target_column': classifier.target_column
            })
        else:
            return Response({'error': 'Unknown model'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_mock_prediction(input_data, model_name):
    """Generate mock prediction for testing when ML models are not available"""
    
    # Calculate a mock confidence score based on input parameters
    confidence = 0.5  # Base confidence
    
    # Adjust confidence based on input parameters
    if 'nasa_confidence' in input_data:
        confidence += input_data['nasa_confidence'] * 0.3
    
    if 'signal_to_noise' in input_data:
        snr = input_data['signal_to_noise']
        confidence += min(snr / 100, 0.2)
    
    if 'transit_depth' in input_data:
        depth = input_data['transit_depth']
        confidence += min(depth / 5000, 0.1)
    
    # Check for flags that would reduce confidence
    flag_penalty = 0
    if input_data.get('flag_not_transit', False):
        flag_penalty += 0.3
    if input_data.get('flag_stellar_eclipse', False):
        flag_penalty += 0.25
    if input_data.get('flag_centroid_offset', False):
        flag_penalty += 0.2
    
    confidence -= flag_penalty
    confidence = max(0.1, min(0.95, confidence))  # Clamp between 0.1 and 0.95
    
    # Determine status based on confidence
    if confidence >= 0.7:
        prediction_status = 'candidate'
    elif confidence >= 0.4:
        prediction_status = 'unknown'
    else:
        prediction_status = 'false_positive'
    
    # Generate explanation
    explanation = generate_explanation(prediction_status, confidence, input_data)
    
    # Create mock probabilities
    probabilities = {
        'candidate': confidence if prediction_status == 'candidate' else (1 - confidence) / 2,
        'false_positive': confidence if prediction_status == 'false_positive' else (1 - confidence) / 2,
        'unknown': confidence if prediction_status == 'unknown' else (1 - confidence) / 2
    }
    
    # Normalize probabilities to sum to 1
    total = sum(probabilities.values())
    probabilities = {k: v / total for k, v in probabilities.items()}
    
    result = {
        'status': prediction_status,
        'confidence': round(confidence, 3),
        'explanation': explanation,
        'probabilities': probabilities,
        'feature_importance': [
            {'feature': 'nasa_confidence', 'importance': 0.25},
            {'feature': 'signal_to_noise', 'importance': 0.20},
            {'feature': 'transit_depth', 'importance': 0.15},
            {'feature': 'orbital_period', 'importance': 0.10},
            {'feature': 'flags', 'importance': 0.30}
        ],
        'mock_prediction': True  # Flag to indicate this is a mock prediction
    }
    
    # Save mock prediction to database
    try:
        prediction = Prediction.objects.create(
            model_name=model_name,
            input_data=input_data,
            predicted_status=prediction_status,
            confidence=confidence,
            probabilities=probabilities
        )
        result['prediction_id'] = prediction.id
    except Exception as e:
        logger.error(f"Failed to save mock prediction: {e}")
    
    return Response(result)

def generate_explanation(status, confidence, input_data):
    """Generate human-readable explanation for the prediction"""
    
    explanations = {
        'candidate': 'Strong signals indicate this is likely a planetary candidate. High confidence score, favorable orbital parameters, and minimal false positive flags suggest a genuine exoplanet transit.',
        'false_positive': 'Low confidence signals suggest this is likely a false positive. Detected anomalies may be caused by stellar activity, instrumental artifacts, or other non-planetary phenomena.',
        'unknown': 'Moderate confidence. The signal shows characteristics of a potential planet, but requires additional observation and analysis to confirm. Some parameters fall outside optimal ranges.'
    }
    
    base_explanation = explanations.get(status, explanations['unknown'])
    
    # Add specific details based on input parameters
    details = []
    
    if 'nasa_confidence' in input_data:
        conf = input_data['nasa_confidence']
        if conf > 0.8:
            details.append("NASA's high confidence score strongly supports the detection.")
        elif conf < 0.3:
            details.append("NASA's low confidence score raises concerns about the detection quality.")
    
    if 'signal_to_noise' in input_data:
        snr = input_data['signal_to_noise']
        if snr > 10:
            details.append("High signal-to-noise ratio indicates a clear, reliable detection.")
        elif snr < 5:
            details.append("Low signal-to-noise ratio suggests the signal may be weak or noisy.")
    
    if details:
        base_explanation += " " + " ".join(details)
    
    return base_explanation