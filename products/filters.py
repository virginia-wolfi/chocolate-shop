import django_filters
from django.db.models import Subquery
from django import forms
from django_filters.widgets import LinkWidget

from .models import ProductCategory, Product


def available_types(request):
    """
    Retrieves the available product categories of a certain type based on the slug provided in the request.
    Filters categories that are associated with products belonging to a specific category group named "Type".
    """
    format = request.resolver_match.kwargs.get("slug")
    product_ids = Product.objects.filter(categories__slug=format).values("id")
    return ProductCategory.objects.filter(
        products__in=Subquery(product_ids), group__name="Type"
    ).distinct()


class ProductFilterByType(django_filters.FilterSet):
    """
    A filter set for filtering products by category type.
    This filter allows users to filter products based on their associated category type.

    The filter uses a `ModelChoiceFilter` to allow selecting a category type from a list of available product categories.
    """

    type = django_filters.ModelChoiceFilter(
        field_name="categories",
        queryset=available_types,
        to_field_name="slug",
        widget=LinkWidget(),
    )

    class Meta:
        fields = ["type"]


class ProductFilter(django_filters.FilterSet):
    """
    A filter set for searching products by name.
    This filter allows users to search for products by their name with an 'icontains' lookup expression.
    """

    name = django_filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(
            attrs={
                "class": "search-field",
                "placeholder": "What are you looking for?",
            }
        ),
    )

    class Meta:
        model = Product
        fields = ["name"]
