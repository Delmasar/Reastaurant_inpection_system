from django import forms
from .models import InspectionRequest, Inspection


class InspectionRequestForm(forms.ModelForm):
    requested_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = InspectionRequest
        fields = ['requested_date']


class InspectionForm(forms.ModelForm):
    inspection_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Inspection
        fields = ['inspection_date', 'general_hygiene', 'customer_service',
                  'food_preparation', 'cooking_outcome', 'comments']