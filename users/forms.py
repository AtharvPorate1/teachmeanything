from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
 
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','grasp_power')


class ChangeGraspPowerForm(forms.Form):
    email = forms.EmailField()
    grasp_power = forms.IntegerField(min_value=0, max_value=100)