from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from common.views import TitleMixin
from products.filters import ProductFilter


class ProfileView(TitleMixin, LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'
    extra_context = {'product_name_filter': ProductFilter}


