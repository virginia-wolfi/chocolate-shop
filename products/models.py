from django.db import models
from django.utils.text import slugify

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
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="products_images", null=True, blank=True)
    ingredients = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(ProductCategory, blank=True, related_name="products")

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

    def __str__(self):
        return f"Basket for {self.user.username} | Product: {self.product.name}"

    def sum(self):
        return self.product.price * self.quantity

    def de_json(self):
        basket_item = {
            "product_name": self.product.name,
            "quantity": self.quantity,
            "price": float(self.product.price),
            "sum": float(self.sum()),
        }
        return basket_item
