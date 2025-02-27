from django.urls import path

from orders.views import OrderCreateView, OrderListView

urlpatterns = [
    path("checkout/", OrderCreateView.as_view(), name="checkout"),
    path("all/", OrderListView.as_view(), name="orders_list"),
    ]