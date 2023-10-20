from django import forms
from phonenumber_field.modelfields import PhoneNumberField

class ClientForm(forms.Form):
    firstname = forms.CharField(max_length=45)
    surname = forms.CharField(max_length=45)
    timeframe = forms.DateField()
