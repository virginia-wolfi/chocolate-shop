from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from accounts.managers import UserManager


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(
        _("username"), max_length=255, blank=True, unique=False
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username"
    ]

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def basket_total_sum(self):
        from products.models import Basket
        return Basket.objects.total_sum(self.pk)

    @property
    def basket_total_quantity(self):
        from products.models import Basket
        return Basket.objects.total_quantity(self.pk)


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.01), MaxValueValidator(0.99)]
    )
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def is_valid_for_user(self, user):
        is_valid =  self.valid_from <= now() <= self.valid_to
        return (is_valid and not
                UsedPromoCode.objects.filter(user=user, promo_code=self).exists())

    def __str__(self):
        return self.code

class UsedPromoCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="used_promo_codes")
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE, related_name="used_by_users")
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'promo_code')

    def __str__(self):
        return f"{self.user.username} used {self.promo_code.code}"


