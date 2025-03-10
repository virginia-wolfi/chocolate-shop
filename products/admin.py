from django.contrib import admin

from products.models import ProductCategory, Product, Basket, Review


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "group")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "discount_price", "get_categories")
    search_fields = ("name", "description")
    list_filter = ("categories",)
    prepopulated_fields = {"slug": ("name",)}

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    get_categories.short_description = "Categories"


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity", "created_timestamp")
    search_fields = ("user__username", "product__name")
    list_filter = ("user", "product")
    ordering = ("-created_timestamp",)
    readonly_fields = ("created_timestamp",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "created_at", "text_preview")
    search_fields = ("user__username", "product__name", "text")
    list_filter = ("product", "user")
    ordering = ("-created_at",)

    def text_preview(self, obj):
        """
        Return a short preview of the review text.
        """
        return obj.text[:50] + ("..." if len(obj.text) > 50 else "")

    text_preview.short_description = "Review Preview"
