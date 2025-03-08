from django import forms

from products.models import Review


class ReviewForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), required=True)

    class Meta:
        model = Review
        fields = ['text']