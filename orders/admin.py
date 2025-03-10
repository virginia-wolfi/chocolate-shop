from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone_number", "status", "created", "total_sum")
    list_filter = ("status", "created")
    search_fields = ("full_name", "phone_number", "address")
    ordering = ("-created",)
    readonly_fields = ("created", "basket_history")
