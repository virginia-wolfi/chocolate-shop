from django.urls import path

from orders.views import OrderCreateView

urlpatterns = [
    path("checkout/", OrderCreateView.as_view(), name="checkout"),
    ]