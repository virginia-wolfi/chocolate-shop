from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """
    Form for creating and updating an order.

    This form allows users to input the required details for an order such as
    their full name, phone number, and address. The form uses model fields
    and provides placeholder attributes for each input field.
    """

    class Meta:
        model = Order
        fields = ["full_name", "phone_number", "address"]

        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Full Name"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "Phone Number"}),
            "address": forms.TextInput(attrs={"placeholder": "Address"}),
        }
