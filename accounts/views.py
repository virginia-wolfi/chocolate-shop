from decimal import Decimal, ROUND_HALF_UP

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin

from accounts.forms import PromoCodeForm
from accounts.models import PromoCode, UsedPromoCode
from common.views import TitleMixin
from products.filters import ProductFilter


class ProfileView(TitleMixin, LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'
    extra_context = {'product_name_filter': ProductFilter}

class PromoCodeApplyView(LoginRequiredMixin, FormMixin, View):
    success_url = reverse_lazy('basket')
    form_class = PromoCodeForm

    def post(self, request, *args, **kwargs):
        request.session.pop('promo_code', None)
        form = self.get_form()
        if form.is_valid():
            request.session['promo_code'] = form.cleaned_data['promo_code']
            messages.success(request, 'Promo code has been applied.')
            return self.form_valid(form)
        messages.error(request, form.errors.get('promo_code'))
        return redirect(self.success_url)

    def get_form_kwargs(self):
        """Adds user to kwargs for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class RemovePromoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        request.session.pop('promo_code', None)
        request.session.modified = True
        messages.success(request, "Promo code removed successfully.")
        return redirect('basket')


