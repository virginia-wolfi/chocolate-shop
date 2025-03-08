from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now

class BasketQuerySet(models.QuerySet):
    def user_baskets(self, user):
        """Returns baskets filtered by user."""
        return self.filter(user=user)

    def total_sum(self, user, promo_code=None) -> Decimal:
        """Returns the total sum of all items in the user's basket, applying a promo code if valid."""
        baskets = self.filter(user=user)
        total = Decimal(sum(basket.sum(promo_code) for basket in baskets))
        return total.quantize(Decimal("0.05"), rounding=ROUND_HALF_UP)

    def total_quantity(self, user):
        """Returns the total quantity of all items in the user's basket."""
        return sum(basket.quantity for basket in self.user_baskets(user))

    def json(self, user, promo_code=None):
        """Returns the user's basket as a JSON-like list."""
        return [basket.de_json(promo_code) for basket in self.user_baskets(user)]




