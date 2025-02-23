from django.db import models


class BasketQuerySet(models.QuerySet):
    def total_sum(self, user_pk):
        return sum(basket.sum() for basket in self.filter(user=user_pk))

    def total_quantity(self, user_pk):
        return sum(basket.quantity for basket in self.filter(user=user_pk))

    def get_basket_json(self, user_pk):
        return [basket.de_json() for basket in self.filter(user=user_pk)]


