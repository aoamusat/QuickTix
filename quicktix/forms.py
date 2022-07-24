from django import forms

class RegistrationForm (forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False)
    password = forms.CharField(required=True, min_length=8)

class TicketForm(forms.Form):
    origin = forms.CharField(required=False)
    destination = forms.CharField(required=False)
    ticket_class = forms.CharField(required=False)
    departure_date = forms.DateField(required=False)
    cost = forms.IntegerField(required=False)
    id_type = forms.CharField(required=False)
    id_number = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    next_of_kin = forms.CharField(required=False)
    next_of_kin_contact = forms.CharField(required=False)
    payment_reference = forms.CharField(required=False)
    payment_status = forms.CharField(required=False)
    