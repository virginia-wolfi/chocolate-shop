from django.db import models
from django.utils.text import slugify
from decimal import Decimal, ROUND_HALF_UP

from accounts.models import User
from products.managers import BasketQuerySet


class CategoryGroup(models.Model):
    """
    Represents a category group, which is a higher-level classification for categories.
    Each category group can contain multiple product categories.
    """

    name = models.CharField("Category group name", max_length=100, unique=True)

    def __str__(self) -> str:
        """
        Returns the name of the category group.
        """
        return self.name


class ProductCategory(models.Model):
    """
    Represents a product category within a category group.
    A category can have many products, and each product can belong to one or more categories.
    """

    name = models.CharField("Category name", max_length=128, unique=True)
    slug = models.SlugField("Category slug", unique=True, blank=True, null=True)
    description = models.TextField("Category description", null=True, blank=True)
    group = models.ForeignKey(
        CategoryGroup, on_delete=models.CASCADE, related_name="categories"
    )

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ["name"]

    def save(self, *args, **kwargs) -> None:
        """
        Automatically generates a slug based on the category name before saving the category.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """
        Returns the name of the product category.
        """
        return self.name


class Product(models.Model):
    """
    Represents a product that can be added to the basket or ordered in the system.
    Each product belongs to one or more categories and has various attributes, including price, description, and image.
    """

    name = models.CharField("Product name", max_length=256)
    slug = models.SlugField("Product slug", unique=True, blank=True, null=True)
    description = models.TextField("Product description")
    price = models.DecimalField("Product price", max_digits=4, decimal_places=2)
    discount_price = models.DecimalField(
        "Discounted price",
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
    )
    image = models.ImageField(
        "Product image", upload_to="products_images", null=True, blank=True
    )
    ingredients = models.TextField("Product ingredients", null=True, blank=True)
    categories = models.ManyToManyField(
        ProductCategory,
        verbose_name="Product categories",
        blank=True,
        related_name="products",
    )

    def get_final_price(self) -> Decimal:
        """
        Returns the final price of the product, considering any discount.
        """
        return self.discount_price if self.discount_price else self.price

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        ordering = ["name"]

    def save(self, *args, **kwargs) -> None:
        """
        Automatically generates the slug from the product's name before saving.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """
        Returns the name of the product.
        """
        return f"Product: {self.name}"


class Basket(models.Model):
    """
    Represents a basket that contains products added by a user.
    A basket is associated with a specific user and includes product details and quantity.
    """

    user = models.ForeignKey(
        to=User, verbose_name="User", on_delete=models.CASCADE, related_name="baskets"
    )
    product = models.ForeignKey(
        to=Product,
        verbose_name="Product",
        on_delete=models.CASCADE,
        related_name="baskets",
    )
    quantity = models.PositiveSmallIntegerField("Quantity", default=0)
    created_timestamp = models.DateTimeField("Created timestamp", auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    class Meta:
        verbose_name = "basket"
        verbose_name_plural = "baskets"
        ordering = ["-created_timestamp"]

    def __str__(self) -> str:
        """
        Returns the username of the user and the name of the product in the basket.

        """
        return f"Basket for {self.user.username} | Product: {self.product.name}"

    def sum(self, promo_code=None) -> Decimal:
        """
        Calculates the total price for this basket item, applying a promo code if valid.
        """
        price = self.product.get_final_price()

        if promo_code:
            if not promo_code.is_valid_for_user(self.user):
                raise ValueError("Invalid or expired promo code.")

            if not self.product.discount_price:
                discount_amount = price * Decimal(promo_code.discount)
                price = (price - discount_amount).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )

        total = price * self.quantity
        return total.quantize(Decimal("0.05"), rounding=ROUND_HALF_UP)

    def de_json(self, promo_code=None) -> dict:
        """
        Returns the basket item as a JSON-compatible dictionary with promo applied.
        """
        return {
            "product_name": self.product.name,
            "quantity": self.quantity,
            "price": str(self.product.get_final_price()),
            "sum": str(self.sum(promo_code)),
        }


class Review(models.Model):
    """
    Represents a review for a product made by a user.
    Each review contains text written by the user and is associated with a specific product.
    """

    product = models.ForeignKey(
        "products.Product",
        verbose_name="Product",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    user = models.ForeignKey(
        User, verbose_name="User", on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField("Review text", blank=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)

    class Meta:
        unique_together = ("product", "user")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """
        Returns a string representing the review by the user for the product.
        """
        return f"Review by {self.user} for {self.product}"
