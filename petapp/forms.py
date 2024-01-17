from django import forms
from .models import pet,user

class petform(forms.ModelForm):
    model=pet
    fields=['Name','Species','Breed','Age','Gender','Description','Price']

class Userform(forms.ModelForm): 
    model=user
    fields='__all__'   