from django import forms

from products.models import Review


class ReviewForm(forms.ModelForm):
    """
    A form for submitting a review for a product.
    This form includes a text field where users can write their review content.

    The form is linked to the `Review` model and allows users to submit a review for a product.
    The `text` field is required and displayed as a textarea widget with a set number of rows and columns.
    """

    text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "cols": 40}), required=True
    )

    class Meta:
        model = Review
        fields = ["text"]
