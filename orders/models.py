from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from accounts.models import User


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

    def __str__(self):
        return f'Order #{self.pk}. {self.full_name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



