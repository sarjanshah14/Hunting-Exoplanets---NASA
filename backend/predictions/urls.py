from django.urls import path
from . import views

urlpatterns = [
    path('models/', views.model_info, name='model_info'),
    path('predict/', views.predict, name='predict'),
    path('history/', views.prediction_history, name='prediction_history'),
    path('features/', views.feature_explanations, name='feature_explanations'),
    path('test-model/', views.test_model, name='test_model'),
]
