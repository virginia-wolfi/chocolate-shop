from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin

from accounts.forms import PromoCodeForm
from common.views import TitleMixin
from products.filters import ProductFilter


class ProfileView(TitleMixin, LoginRequiredMixin, TemplateView):
    """
    View to display the user's profile page.

    The profile view displays the profile details and applies a product filter
    for the displayed products. The user must be logged in to access this page.
    """

    title = "Profile"
    template_name = "account/profile.html"
    extra_context = {"product_name_filter": ProductFilter}


class PromoCodeApplyView(LoginRequiredMixin, FormMixin, View):
    """
    View to apply a promo code to the user's basket.

    Users can submit a promo code via a form. If the code is valid, it will be
    saved in the session and the user will be notified. If the code is invalid,
    an error message will be displayed.
    """

    success_url = reverse_lazy("basket")  # Redirect after successful form submission
    form_class = PromoCodeForm

    def post(self, request, *args, **kwargs):
        """
        Handle the POST request to apply the promo code.

        Removes any previously applied promo code from the session,
        validates the form, and either applies the new promo code or displays an error.
        """
        request.session.pop("promo_code", None)
        form = self.get_form()
        if form.is_valid():
            request.session["promo_code"] = form.cleaned_data["promo_code"]
            messages.success(request, "Promo code has been applied.")
            return self.form_valid(form)

        # Display error message if the form is invalid
        messages.error(request, form.errors.get("promo_code"))
        return redirect(self.success_url)

    def get_form_kwargs(self):
        """
        Add the current user to the form's instantiation.
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class PromoCodeRemoveView(LoginRequiredMixin, View):
    """
    View to handle the removal of the promo code from the user's session.

    This view removes the promo code from the user's session and notifies the
    user with a success message. It is typically triggered when the user
    decides to cancel or remove a promo code applied to their basket.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles the POST request to remove a promo code from the session.

        It deletes the promo code stored in the session, sets the session as modified,
        and provides feedback to the user that the promo code has been successfully removed.
        """
        request.session.pop("promo_code", None)
        request.session.modified = True
        messages.success(request, "Promo code removed successfully.")
        return redirect("basket")
