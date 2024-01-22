from django import forms
from main.models import User

class OperatorForm(forms.ModelForm):
    class Meta:
        model = User
        fields =['first_name','last_name','email','phone_number','role','viloyat']

    