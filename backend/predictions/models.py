from django.db import models
import json

class Prediction(models.Model):
    """Model to store prediction history"""
    
    MODEL_CHOICES = [
        ('kepler', 'Kepler'),
        ('k2', 'K2'),
        ('toi', 'TOI (TESS)'),
    ]
    
    STATUS_CHOICES = [
        ('candidate', 'Planetary Candidate'),
        ('false_positive', 'False Positive'),
        ('confirmed', 'Confirmed Planet'),
        ('unknown', 'Unknown'),
    ]
    
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    model_name = models.CharField(max_length=20, choices=MODEL_CHOICES)
    input_data = models.JSONField()
    predicted_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    confidence = models.FloatField()
    probabilities = models.JSONField()
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.model_name} - {self.predicted_status} ({self.confidence:.2f})"
    
    @property
    def input_summary(self):
        """Return a summary of input parameters"""
        data = self.input_data
        summary = []
        for key, value in data.items():
            if isinstance(value, float):
                summary.append(f"{key}: {value:.3f}")
            else:
                summary.append(f"{key}: {value}")
        return ", ".join(summary[:3]) + "..." if len(summary) > 3 else ", ".join(summary)