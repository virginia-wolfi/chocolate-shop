from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from common.views import TitleMixin
from orders.forms import OrderForm
from products.models import Basket


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'order/checkout.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders_list')
    title = 'Checkout'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.baskets.all():
            raise Http404("No products added to basket")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        form.instance.basket_history = Basket.objects.get_basket_json(self.request.user)
        form.instance.total_sum = self.request.user.basket_total_sum
        return super().form_valid(form)

class OrderListView(TitleMixin, ListView):
    template_name = 'order/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return self.request.user.orders.all()
