from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from common.views import PromoCodeMixin, TitleMixin
from .forms import OrderForm
from .models import Order
from products.filters import ProductFilter
from products.models import Basket


class OrderCreateView(PromoCodeMixin, TitleMixin, LoginRequiredMixin, CreateView):
    """
    View for creating an order during the checkout process.

    This view handles the order creation, including the assignment of the
    current user, applying promo codes if available, calculating the total sum,
    and saving the order along with the basket history.
    """

    template_name = "order/checkout.html"
    form_class = OrderForm
    success_url = reverse_lazy("order-list")
    title = "Checkout"
    extra_context = {"product_name_filter": ProductFilter}

    def dispatch(self, request, *args, **kwargs):
        """
        Handles the request to ensure the user has added products to the basket.

        If no products are added to the basket, a 404 error is raised.
        """
        if not request.user.baskets.all():
            raise Http404("No products added to basket")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Handles the form submission when the form is valid.

        Assigns the current user to the order, calculates the total sum after
        applying the promo code (if any), and saves the basket history.
        """
        form.instance.initiator = self.request.user
        if self.promo_code is not None:
            form.instance.basket_history = Basket.objects.json(
                self.request.user, self.promo_code
            )
            form.instance.promo_code = self.promo_code
            form.instance.total_sum = self.total_after_promo
            del self.request.session["promo_code"]
        else:
            form.instance.total_sum = self.basket_total_sum
            form.instance.basket_history = Basket.objects.json(self.request.user)

        return super().form_valid(form)


class OrderListView(TitleMixin, LoginRequiredMixin, ListView):
    """
    View to display the list of orders placed by the current user.

    This view fetches all orders associated with the current user and displays
    them in a list. Each order includes the order details like the full name,
    phone number, address, and status.
    """

    template_name = "order/list.html"
    context_object_name = "orders"
    extra_context = {"product_name_filter": ProductFilter}

    def get_queryset(self):
        """
        Returns the queryset of orders associated with the current user.

        Only orders where the `initiator` is the current logged-in user are
        returned.
        """
        return Order.objects.filter(initiator=self.request.user).all()
