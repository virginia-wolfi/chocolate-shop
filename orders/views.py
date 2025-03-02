

from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order
from products.models import Basket


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'order/checkout.html'
    form_class = OrderForm
    success_url = reverse_lazy('home')
    title = 'Checkout'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.baskets.all():
            raise Http404("No products added to basket")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        form.instance.basket_history = Basket.objects.get_basket_json(self.request.user)
        return super().form_valid(form)

class OrderListView(TitleMixin, ListView):
    template_name = 'order/list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(initiator=self.request.user)