from django.urls import path

from accounts.views import ProfileView, PromoCodeApplyView, RemovePromoView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path("apply-promo/", PromoCodeApplyView.as_view(), name="apply_promo"),
    path('remove-promo/', RemovePromoView.as_view(), name='remove_promo'),
]