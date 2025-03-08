from django.contrib import messages
from django.http import HttpRequest
from django.views.generic import TemplateView

from accounts.models import PromoCode
from products.filters import ProductFilter
from products.models import Basket


class TitleMixin:
    """
    A mixin for adding a dynamic title to the context of views.
    The title can be set using the `title` attribute and will be
    included in the context data for rendering.
    """

    title = None

    def get_context_data(self, **kwargs) -> dict:
        """
        Adds the dynamic title to the context data.

        This method is used to include the `title` attribute into
        the context data, which will be used for rendering the view's template.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context


class IndexView(TitleMixin, TemplateView):
    """
    A view that renders the main page (home page) with the title "Main page".

    This view extends `TitleMixin` to include the dynamic title in the context
    and uses the `TemplateView` to render the `home.html` template.
    It also provides the `product_name_filter` to filter products on the page.
    """

    template_name = "home.html"
    title = "Main page"
    extra_context = {"product_name_filter": ProductFilter}


class PromoCodeMixin:
    """
    A mixin for handling promo codes in the basket and during the checkout process.

    It retrieves the promo code from the session, calculates the total after applying
    the promo code, and adds this information to the context.
    """

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        """
        Retrieves the promo code from the session and calculates the total amount after applying it.

        This method checks if a valid promo code is stored in the session, and if so, retrieves the promo
        code from the database and calculates the new total with the promo code applied.
        """
        self.promo_code_str = request.session.get("promo_code", None)
        self.promo_code = None
        self.total_after_promo = None

        if self.promo_code_str is not None:
            try:
                self.promo_code = PromoCode.objects.filter(
                    code=self.promo_code_str
                ).first()
                self.total_after_promo = Basket.objects.total_sum(
                    request.user, self.promo_code
                )
            except (PromoCode.DoesNotExist, ValueError):
                messages.error(request, "Invalid promo code.")
                del request.session["promo_code"]

        self.basket_total_sum = Basket.objects.total_sum(request.user)
        super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        """
        Adds the basket's total sum and the total after applying the promo code to the context data.

        This method retrieves the total sum of the user's basket and, if a valid promo code is applied,
        the total sum after the promo code discount. It adds these values to the context for the view.
        """
        context = super().get_context_data(**kwargs)
        context["basket_total_sum"] = self.basket_total_sum
        if self.promo_code is not None:
            context["total_after_promo"] = self.total_after_promo
        return context
