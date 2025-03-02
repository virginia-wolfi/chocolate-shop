from django.urls import path

from products.filters import ProductFilter
from products.views import CategoryProductsView, ProductDetailView, BasketAddView, BasketListView, BasketDeleteView, \
    ProductListView

urlpatterns = [
    path(
        "category/<slug:slug>/",
        CategoryProductsView.as_view(),
        name="category_products",
    ),
    path("product/", ProductListView.as_view(), name="product_list"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
    path("add-to-cart/", BasketAddView.as_view(), name="add_to_card"),
    path("basket/", BasketListView.as_view(), name="basket"),
    path("basket-delete/<int:pk>", BasketDeleteView.as_view(), name="basket_delete"),

]
