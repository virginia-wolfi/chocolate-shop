from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, FormView
from django_filters.views import FilterView

from accounts.forms import PromoCodeForm
from common.views import TitleMixin, PromoCodeMixin

from products.filters import ProductFilterByType, ProductFilter
from products.forms import ReviewForm
from products.models import ProductCategory, Product, Basket, Review


class IndexView(TitleMixin, TemplateView):
    template_name = "home.html"
    title = "Chocolate Store"
    extra_context = {'product_name_filter': ProductFilter}


class CategoryProductsView(TitleMixin, FilterView):
    template_name = "category/category_products.html"
    context_object_name = "category_products"
    filterset_class = ProductFilterByType
    extra_context = {'product_name_filter': ProductFilter}

    def get_queryset(self):
        self.category = get_object_or_404(ProductCategory, slug=self.kwargs["slug"])
        print(self.category.products.all().order_by("slug"))
        return self.category.products.all().order_by("slug")

    def get_context_data(self, *, object_list = ..., **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class ProductListView(FilterView):
    template_name = "product/list.html"
    context_object_name = "products"
    filterset_class = ProductFilter
    extra_context = {'product_name_filter': ProductFilter}



class ProductDetailView(DetailView):
    model = Product
    template_name = "product/detail.html"
    context_object_name = "product"
    extra_context = {'product_name_filter': ProductFilter, 'product_review_form': ReviewForm}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        user_review_exists = Review.objects.filter(user=self.request.user, product=product).exists()

        context['user_review_exists'] = user_review_exists
        return context


class BasketAddView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        product = get_object_or_404(Product, pk=request.POST["product_pk"])
        quantity = int(request.POST["quantity"])
        basket = Basket.objects.get_or_create(user=user, product=product)[0]
        basket.quantity += quantity
        basket.save()
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

class BasketListView(PromoCodeMixin, TitleMixin, ListView):
    template_name = 'basket/basket.html'
    context_object_name = 'baskets'
    form_class = PromoCodeForm
    extra_context = {'product_name_filter': ProductFilter, 'promo_form': PromoCodeForm}
    success_url = reverse_lazy("basket")


    def get_queryset(self):
        return self.request.user.baskets.all()

class BasketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Basket
    template_name = 'basket/basket.html'
    success_url = reverse_lazy('basket')

    def test_func(self):
        basket = self.get_object()
        return basket.user == self.request.user


class ReviewCreateView(LoginRequiredMixin, FormView):
    form_class = ReviewForm

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, slug=self.kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = self.product
        form.save()

        messages.success(self.request, "Your review has been submitted successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your review.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'slug': self.product.slug})

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    pk_url_kwarg = 'review_id'

    def get_success_url(self):
        messages.success(self.request, "Your review has been deleted successfully.")
        return reverse_lazy('product_detail', kwargs={'slug': self.object.product.slug})

    def test_func(self):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        return review.user == self.request.user






