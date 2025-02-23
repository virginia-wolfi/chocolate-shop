from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, DeleteView

from common.views import TitleMixin
from products.models import ProductCategory, Product, Basket


class IndexView(TitleMixin, TemplateView):
    template_name = "home.html"
    title = "Chocolate Store"


class CategoryProductsView(ListView):
    template_name = "category/category_products.html"
    context_object_name = "category_products"

    def get_queryset(self):
        category = get_object_or_404(ProductCategory, slug=self.kwargs["slug"])
        return category.products.all()


class ProductDetailView(DetailView):
    model = Product
    template_name = "product/product.html"
    context_object_name = "product"


class BasketAddView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        product = get_object_or_404(Product, pk=request.POST["product_pk"])
        quantity = int(request.POST["quantity"])
        basket = Basket.objects.get_or_create(user=user, product=product)[0]
        basket.quantity += quantity
        basket.save()
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

class BasketListView(LoginRequiredMixin, ListView):
    template_name = 'basket/basket.html'
    context_object_name = 'baskets'

    def get_queryset(self):
        return self.request.user.baskets.all()

class BasketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Basket
    template_name = 'basket/basket.html'
    success_url = reverse_lazy('checkout_card')

    def test_func(self):
        basket = self.get_object()
        return basket.user == self.request.user






