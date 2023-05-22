from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
from django.forms import ModelForm, TextInput, EmailInput

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','name','background')
        # email = forms.EmailInput(widget=forms.EmailInput(attrs={'class': 'form-control'}))
        # name = forms.CharInput(widget=forms.TextInput(attrs={'class': 'form-control'}))
        # background = forms.CharInput(widget=forms.TextInput(attrs={'class': 'form-control'}))

        widgets = {
            'email': EmailInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Email'
                }),
            'name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Name'
                }),
            
        }    
        


class ChangeGraspPowerForm(forms.Form):
    email = forms.EmailField()
    grasp_power = forms.IntegerField(min_value=0, max_value=100)
    # comprehension = forms.IntegerField(min_value=0, max_value=100)
    # engagement = forms.IntegerField(min_value=0, max_value=100)
    # learning_speed = forms.IntegerField(min_value=0, max_value=100)
    # curiosity = forms.IntegerField(min_value=0, max_value=100)
    # confidence = forms.IntegerField(min_value=0, max_value=100)