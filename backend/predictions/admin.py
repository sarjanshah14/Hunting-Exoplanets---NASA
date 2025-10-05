from django.contrib import admin
from .models import Prediction

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['id', 'timestamp', 'model_name', 'predicted_status', 'confidence', 'input_summary']
    list_filter = ['model_name', 'predicted_status', 'timestamp']
    search_fields = ['input_data']
    readonly_fields = ['timestamp']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('timestamp', 'model_name')
        }),
        ('Prediction Results', {
            'fields': ('predicted_status', 'confidence', 'probabilities')
        }),
        ('Input Data', {
            'fields': ('input_data',),
            'classes': ('collapse',)
        }),
    )