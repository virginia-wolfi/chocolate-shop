from django.urls import path

from orders import views

urlpatterns = [
    path("list/", views.OrderListView.as_view(), name="order-list"),
    path("checkout/", views.OrderCreateView.as_view(), name="checkout"),
]
