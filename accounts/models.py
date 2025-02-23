from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.managers import UserManager



class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(
        _("username"), max_length=255, blank=True, unique=False
    )  # не уникальный

    USERNAME_FIELD = "email"  # аутентификация по email
    REQUIRED_FIELDS = [
        "username"
    ]  # добавляем username в обязательные поля при регистрации

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def basket_total_sum(self):
        from products.models import Basket
        return Basket.objects.total_sum(self.pk)


