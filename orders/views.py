from decimal import Decimal, ROUND_HALF_UP

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from common.views import TitleMixin, PromoCodeMixin
from orders.forms import OrderForm
from orders.models import Order
from products.filters import ProductFilter
from products.models import Basket


class OrderCreateView(PromoCodeMixin, TitleMixin, LoginRequiredMixin, CreateView):
    template_name = 'order/checkout.html'
    form_class = OrderForm
    success_url = reverse_lazy('order-list')
    title = 'Checkout'
    extra_context = {'product_name_filter': ProductFilter}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.baskets.all():
            raise Http404("No products added to basket")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        if self.promo_code is not None:
            form.instance.basket_history = Basket.objects.json(self.request.user, self.promo_code)
            form.instance.promo_code = self.promo_code
            form.instance.total_sum = self.total_after_promo
            del self.request.session["promo_code"]
        else:
            form.instance.total_sum = self.basket_total_sum
            form.instance.basket_history = Basket.objects.json(self.request.user)

        return super().form_valid(form)

class OrderListView(TitleMixin, LoginRequiredMixin, ListView):
    template_name = 'order/list.html'
    context_object_name = 'orders'
    extra_context = {'product_name_filter': ProductFilter}

    def get_queryset(self):
        return Order.objects.filter(initiator=self.request.user)