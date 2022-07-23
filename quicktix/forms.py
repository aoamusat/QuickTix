from django import forms

class RegistrationForm (forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False)
    password = forms.CharField(required=True, min_length=8)

    