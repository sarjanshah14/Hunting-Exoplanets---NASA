# Exoplanet Detection Backend

Django REST API backend for exoplanet detection using NASA's machine learning models.

## Features

- **Multiple ML Models**: Support for Kepler, K2, and TOI (TESS) exoplanet classifiers
- **REST API**: RESTful endpoints for predictions, model information, and history
- **Real-time Predictions**: Fast predictions using trained Random Forest models
- **Feature Importance**: Detailed feature importance analysis
- **Prediction History**: Store and retrieve prediction history
- **CORS Enabled**: Ready for frontend integration

## Installation

1. **Create and activate virtual environment**:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Create superuser (optional)**:
```bash
python manage.py createsuperuser
```

## Running the Server

```bash
# Using the startup script
./start_server.sh

# Or manually
source venv/bin/activate
python manage.py runserver 0.0.0.0:8001
```

The server will be available at `http://localhost:8001`

## API Endpoints

### Models Information
- `GET /api/models/` - Get information about available models

### Predictions
- `POST /api/predict/` - Make exoplanet prediction
- `GET /api/history/` - Get prediction history
- `GET /api/features/?model={model}` - Get feature explanations

### Example Prediction Request
```json
POST /api/predict/
{
    "model": "kepler",
    "nasaConfidence": 0.85,
    "signalToNoise": 15.2,
    "transitDepth": 1200,
    "orbitalPeriod": 25.5,
    "transitDuration": 3.2,
    "planetRadius": 1.8,
    "planetTemperature": 450,
    "flagNotTransit": false,
    "flagStellarEclipse": false,
    "flagCentroidOffset": false,
    "flagEphemerisMatch": false
}
```

## Models

### Kepler Model
- **Dataset**: Kepler Mission Data Release 25
- **Features**: 40+ features including transit depth, orbital period, stellar parameters
- **Accuracy**: ~93.5%

### K2 Model
- **Dataset**: K2 Mission candidates
- **Features**: Light curve characteristics, transit parameters, stellar properties
- **Accuracy**: ~94.2%

### TOI (TESS) Model
- **Dataset**: TESS Object of Interest catalog
- **Features**: Full-frame image photometry, multi-sector observations
- **Accuracy**: ~96.8%

## Data Files

The following CSV files are required in the `data/` directory:
- `cleaned_kepler_train.csv` - Kepler training data
- `k2pandc_2025.10.04_00.32.39.csv` - K2 training data
- `TOI_2025.10.04_00.32.31.csv` - TOI training data

## Admin Interface

Access the Django admin interface at `http://localhost:8001/admin/` to:
- View prediction history
- Monitor model performance
- Manage user data

## Development

### Project Structure
```
backend/
├── exoplanet_backend/     # Django project settings
├── predictions/           # Main app with models, views, serializers
├── ml_models/            # Machine learning model classes
├── data/                 # Training data CSV files
├── requirements.txt      # Python dependencies
└── start_server.sh      # Server startup script
```

### Adding New Models

1. Create a new classifier class in `ml_models/`
2. Inherit from `BaseExoplanetClassifier`
3. Implement required methods
4. Add to model registry in `views.py`
5. Update API endpoints as needed

## Troubleshooting

### Common Issues

1. **Import Error**: Ensure virtual environment is activated
2. **Data File Not Found**: Check that CSV files are in `data/` directory
3. **Model Training Fails**: Verify CSV file format and target column names
4. **CORS Issues**: Check `CORS_ALLOW_ALL_ORIGINS` setting in `settings.py`

### Logs

Check Django logs for detailed error information:
```bash
python manage.py runserver --verbosity=2
```
