from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model
from .models import Leads, Agent

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Leads
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
            'organization'
        )



class LeadForm(forms.Form):
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)
    age = forms.IntegerField(min_value=0)

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)
        field_classes={'username':UsernameField}
