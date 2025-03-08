from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now

from accounts.models import User
from products.managers import BasketQuerySet

class CategoryGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    group = models.ForeignKey(CategoryGroup, on_delete=models.CASCADE, related_name="categories")

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "category"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=4, decimal_places=2)
    image = models.ImageField(upload_to="products_images", null=True, blank=True)
    ingredients = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(ProductCategory, blank=True, related_name="products")
    discount_price = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def get_final_price(self):
        return self.discount_price if self.discount_price else self.price

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Product: {self.name}"


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='baskets')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='baskets')
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    class Meta:
        verbose_name = "basket"
        verbose_name_plural = "baskets"
        ordering = ['-created_timestamp']

    def __str__(self):
        return f"Basket for {self.user.username} | Product: {self.product.name}"

    def sum(self, promo_code=None):
        """Returns the total price for this basket item, applying a promo code if valid."""
        price = self.product.get_final_price()

        if promo_code:
            if not promo_code.is_valid_for_user(self.user):
                raise ValueError("Invalid or expired promo code.")

            if not self.product.discount_price:
                discount_amount = price * Decimal(promo_code.discount)
                price = (price - discount_amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        total = price * self.quantity
        return total.quantize(Decimal("0.05"), rounding=ROUND_HALF_UP)


    def de_json(self, promo_code=None):
        """Returns the basket item as a JSON-compatible dictionary with promo applied."""
        return {
            "product_name": self.product.name,
            "quantity": self.quantity,
            "price": str(self.product.get_final_price()),
            "sum": str(self.sum(promo_code)),
        }


class Review(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField("Review text", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f"Review by {self.user} for {self.product}"
