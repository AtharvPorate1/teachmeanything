from django import forms

class userform(forms.ModelForm):

    class Meta:
        model = 'users.user'
        fields = []