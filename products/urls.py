from django.urls import path

from products import views

urlpatterns = [
    path(
        "category/<slug:slug>/",
        views.CategoryProductsView.as_view(),
        name="category_products",
    ),
    path("product/", views.ProductListView.as_view(), name="product_list"),
    path(
        "product/<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"
    ),
    path("add-to-cart/", views.BasketAddView.as_view(), name="add_to_card"),
    path("basket/", views.BasketListView.as_view(), name="basket"),
    path(
        "basket-delete/<int:pk>", views.BasketDeleteView.as_view(), name="basket_delete"
    ),
    path(
        "product/<slug:slug>/add-review/",
        views.ReviewCreateView.as_view(),
        name="add_review",
    ),
    path(
        "product/<slug:slug>/delete-review/<int:review_id>/",
        views.ReviewDeleteView.as_view(),
        name="delete_review",
    ),
]
