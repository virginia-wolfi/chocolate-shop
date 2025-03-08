from django import forms
from accounts.models import PromoCode


class PromoCodeForm(forms.Form):
    """
    Form for handling the promo code input.

    This form is used to validate a promo code entered by the user, checking its validity
    and ensuring that it has not already been used by the user.
    """

    promo_code = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"placeholder": "Promo Code"})
    )

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes the form and passes the user object for validation.
        """
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_promo_code(self) -> str:
        """
        Validates the promo code entered by the user.

        Checks if the promo code exists, and whether it is valid for the user.
        Raises a validation error if the promo code is invalid or has already been used.
        """
        code = self.cleaned_data.get("promo_code")

        try:
            promo = PromoCode.objects.get(code=code)
            if not promo.is_valid_for_user(user=self.user):
                raise forms.ValidationError("You have already used this promo code.")
        except PromoCode.DoesNotExist:
            raise forms.ValidationError("Invalid promo code.")

        return code
