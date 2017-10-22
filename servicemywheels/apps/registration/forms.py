from django import forms
from core.models import Customers


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Customers
        fields = ('customer_name', 'email', 'password')