from django.urls import path

from orders.views import OrderCreateView, OrderListView

urlpatterns = [
    path("all/", OrderListView.as_view(), name="order-list"),
    path("checkout/", OrderCreateView.as_view(), name="checkout"),

    ]