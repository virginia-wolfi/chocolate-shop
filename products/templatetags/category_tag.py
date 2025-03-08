from django import template
from products.models import ProductCategory

register = template.Library()


@register.simple_tag
def get_categories():
    return ProductCategory.objects.filter(group__name="Format").all()
