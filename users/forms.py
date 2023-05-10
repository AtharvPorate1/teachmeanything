from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
 
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','grasp_power','comprehension','engagement','learning_speed','curiosity','confidence')
        


class ChangeGraspPowerForm(forms.Form):
    email = forms.EmailField()
    grasp_power = forms.IntegerField(min_value=0, max_value=100)
    # comprehension = forms.IntegerField(min_value=0, max_value=100)
    # engagement = forms.IntegerField(min_value=0, max_value=100)
    # learning_speed = forms.IntegerField(min_value=0, max_value=100)
    # curiosity = forms.IntegerField(min_value=0, max_value=100)
    # confidence = forms.IntegerField(min_value=0, max_value=100)