from django.urls import path

from accounts import views

urlpatterns = [
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("apply-promo/", views.PromoCodeApplyView.as_view(), name="apply_promo"),
    path("remove-promo/", views.PromoCodeRemoveView.as_view(), name="remove_promo"),
]
