# forms.py
from django import forms
from .models import Itineraries

class CreateItineraryForm(forms.ModelForm):
    class Meta:
        model = Itineraries
        fields = ['title', 'days', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'start_date', 'readonly': 'readonly'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'end_date', 'readonly': 'readonly'}),
        }
