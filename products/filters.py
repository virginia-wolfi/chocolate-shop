import django_filters
from django.db.models import Subquery
from django import forms
from django_filters.widgets import LinkWidget

from .models import ProductCategory, Product


def available_types(request):
    format = request.resolver_match.kwargs.get("slug")
    product_ids = Product.objects.filter(categories__slug=format).values("id")
    return ProductCategory.objects.filter(
        products__in=Subquery(product_ids),
        group__name="Type"
    ).distinct()

class ProductFilterByType(django_filters.FilterSet):
    type = django_filters.ModelChoiceFilter(
        field_name="categories",
        queryset=available_types,
        to_field_name="slug",
        widget=LinkWidget()
    )

    class Meta:
        fields = ["type"]

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={
            'class': 'search-field',
            'placeholder': 'What are you looking for?',
  # стили
        }))

    class Meta:
        model = Product
        fields = ["name"]
