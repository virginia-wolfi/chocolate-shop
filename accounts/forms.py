from django import forms

from accounts.models import PromoCode, UsedPromoCode


class PromoCodeForm(forms.Form):
    promo_code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Promo Code'})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_promo_code(self):
        code = self.cleaned_data.get("promo_code")

        try:
            promo = PromoCode.objects.get(code=code)
            if not promo.is_valid_for_user(user=self.user):
                raise forms.ValidationError("You have already used this promo code.")
        except PromoCode.DoesNotExist:
            raise forms.ValidationError("Invalid promo code.")

        return code

