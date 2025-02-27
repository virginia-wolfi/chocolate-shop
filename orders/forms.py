from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone_number', 'address']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full name'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone number'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address'}),
        }

