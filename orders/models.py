from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from accounts.models import User, PromoCode, UsedPromoCode


class Order(models.Model):
    class OrderStatus(models.IntegerChoices):
        CREATED = 0, "Created"
        PAID = 1, "Paid"
        ON_WAY = 2, "In way"
        DELIVERED = 3, "Delivered"

    full_name = models.CharField("Full name", max_length=64)
    phone_number = PhoneNumberField("Phone number", region='US')
    address = models.CharField("Address", max_length=256)
    basket_history = models.JSONField("Basket history", default=list)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=OrderStatus.CREATED, choices=OrderStatus.choices)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='orders')
    total_sum = models.DecimalField(max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))])
    promo_code = models.ForeignKey(PromoCode, null=True, blank=True, on_delete=models.SET_NULL)


    def __str__(self):
        return f'Order #{self.pk}. {self.full_name}'

    def clean(self):
        errors = {}

        # Проверяем промокод
        if self.promo_code and not self.promo_code.is_valid_for_user(self.initiator):
            errors["promo_code"] = "This promo code is not valid for this user."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.clean()
        if self.promo_code :
            UsedPromoCode.objects.create(
                user=self.initiator,
                promo_code=self.promo_code,
            )
        self.initiator.baskets.all().delete()
        super().save(*args, **kwargs)
