from django.core.validators import MinValueValidator
from accounts.models import User, PromoCode, UsedPromoCode

from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from accounts.models import User


class Order(models.Model):
    """
    A model representing an order in the system. This model includes information about
    the customer's order, including their details, the status of the order, the total sum,
    and any promo code used.
    """

    class OrderStatus(models.IntegerChoices):
        CREATED = 0, "Created"
        PAID = 1, "Paid"
        ON_WAY = 2, "In way"
        DELIVERED = 3, "Delivered"

    full_name = models.CharField("Full name", max_length=64)
    phone_number = PhoneNumberField("Phone number", region="US")
    address = models.CharField("Address", max_length=256)
    basket_history = models.JSONField("Basket history", default=list)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(
        default=OrderStatus.CREATED, choices=OrderStatus.choices
    )
    initiator = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="orders"
    )
    total_sum = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    promo_code = models.ForeignKey(
        PromoCode, null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        """
        Returns a string representation of the order.
        """
        return f"Order #{self.pk}. {self.full_name}"

    def clean(self) -> None:
        """
        Validates the order's attributes before saving.

        This method checks if the promo code is valid for the user and raises a validation error if it is not.
        """
        if self.promo_code and not self.promo_code.is_valid_for_user(self.initiator):
            raise ValidationError("This promo code is not valid for this user.")

    def save(self, *args, **kwargs) -> None:
        """
        Saves the order to the database after validation.
        """
        self.clean()

        if self.promo_code:
            UsedPromoCode.objects.create(
                user=self.initiator,
                promo_code=self.promo_code,
            )

        # Delete the user's basket items
        self.initiator.baskets.all().delete()

        super().save(*args, **kwargs)
