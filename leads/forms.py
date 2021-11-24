from django import forms
from .models import Leads as LeadsModel

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = LeadsModel
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
        )

class LeadForm(forms.Form):
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)
    age = forms.IntegerField(min_value=0)
