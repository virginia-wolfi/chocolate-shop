from django.contrib import messages

from accounts.models import PromoCode
from products.filters import ProductFilter
from products.models import Product, Basket


class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context

class PromoCodeMixin:
    """Миксин для работы с промокодами в корзине и при оформлении заказа."""

    def setup(self, request, *args, **kwargs):
        """Извлекает промокод из сессии и вычисляет итоговую сумму."""
        self.promo_code_str = request.session.get("promo_code", None)
        self.promo_code = None
        self.total_after_promo = None

        if self.promo_code_str is not None:
            try:
                self.promo_code = PromoCode.objects.filter(code=self.promo_code_str).first()
                self.total_after_promo = Basket.objects.total_sum(request.user, self.promo_code)
            except (PromoCode.DoesNotExist, ValueError):
                messages.error(request, "Invalid promo code.")
                del request.session["promo_code"]

        self.basket_total_sum = Basket.objects.total_sum(request.user)
        super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Добавляет сумму корзины и сумму с промокодом в контекст."""
        context = super().get_context_data(**kwargs)
        context["basket_total_sum"] = self.basket_total_sum
        if self.promo_code is not None:
            context["total_after_promo"] = self.total_after_promo
        return context



