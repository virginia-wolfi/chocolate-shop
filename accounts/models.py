from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

from django.utils import timezone

from accounts.managers import UserManager


class User(AbstractUser):
    """
    Custom user model that extends the built-in AbstractUser to use email for authentication
    and provides methods to calculate the total sum and quantity of items in the user's basket.
    """

    email = models.EmailField("Email address", unique=True)
    username = models.CharField("Username", max_length=255, blank=True, unique=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self) -> str:
        """
        String representation of the user, using the email address.
        """
        return self.email

    @property
    def basket_total_sum(self) -> float:
        """
        Property to calculate and return the total sum of items in the user's basket.

        Returns:
            float: The total sum of the user's basket.
        """
        from products.models import Basket

        return Basket.objects.total_sum(self.pk)

    @property
    def basket_total_quantity(self) -> int:
        """
        Property to calculate and return the total quantity of items in the user's basket.

        """
        from products.models import Basket

        return Basket.objects.total_quantity(self.pk)


class PromoCode(models.Model):
    """
    Model representing a promo code with a discount, valid within a given date range.
    This model is used for discount logic in the application.
    """

    code = models.CharField("Promo Code", max_length=50, unique=True)
    discount = models.DecimalField(
        "Discount",
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.01), MaxValueValidator(0.99)],
    )
    valid_from = models.DateTimeField("Valid From")
    valid_to = models.DateTimeField("Valid To")

    def is_valid_for_user(self, user: User) -> bool:
        """
        Check if the promo code is valid for the given user. A promo code is considered valid if:
        - The promo code is within the valid date range.
        - The user has not already used the promo code.
        """
        is_valid = self.valid_from <= timezone.now() <= self.valid_to
        return (
            is_valid
            and not UsedPromoCode.objects.filter(user=user, promo_code=self).exists()
        )

    def __str__(self) -> str:
        """
        String representation of the promo code.
        """
        return self.code


class UsedPromoCode(models.Model):
    """
    Model to track which promo codes have been used by which users.
    This ensures that each promo code can only be used once per user.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="used_promo_codes",
        verbose_name="User",
    )
    promo_code = models.ForeignKey(
        PromoCode,
        on_delete=models.CASCADE,
        related_name="used_by_users",
        verbose_name="Promo Code",
    )
    used_at = models.DateTimeField(auto_now_add=True, verbose_name="Used At")

    class Meta:
        unique_together = ("user", "promo_code")

    def __str__(self) -> str:
        """
        String representation of the used promo code, showing the user and the promo code.
        """
        return f"{self.user.username} used {self.promo_code.code}"
