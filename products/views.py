from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.http import (
    HttpResponseRedirect,
    HttpResponseBadRequest,
    HttpRequest,
    HttpResponse,
    HttpResponseForbidden,
)
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    DeleteView,
    FormView,
)
from django_filters.views import FilterView

from accounts.forms import PromoCodeForm
from common.views import TitleMixin, PromoCodeMixin

from products.filters import ProductFilterByType, ProductFilter
from products.forms import ReviewForm
from products.models import ProductCategory, Product, Basket, Review


class CategoryProductsView(TitleMixin, FilterView):
    """
    A view that displays a list of products within a specific category.

    This view applies a filter to the products in the selected category based on the type (using `ProductFilterByType`).
    It retrieves the products based on the category's slug and orders them by the product's slug.
    """

    title = "Category Products"
    template_name = "category/category_products.html"
    context_object_name = "category_products"
    filterset_class = ProductFilterByType
    extra_context = {"product_name_filter": ProductFilter}

    def get_queryset(self) -> QuerySet:
        """
        Retrieves the products related to the category based on the category slug provided in the URL.

        The queryset filters products by the category and orders them by their slug.
        """
        self.category = get_object_or_404(ProductCategory, slug=self.kwargs["slug"])
        return self.category.products.all()

    def get_context_data(self, **kwargs) -> dict:
        """
        Adds the selected category to the context data.

        The category is retrieved based on the slug, and it's added to the context to be rendered in the template.
        """
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class ProductListView(TitleMixin, FilterView):
    """
    A view that displays a list of all products with an option to filter them by name.

    This view applies a filter to the list of products using the `ProductFilter` form to search for products by name.

    Attributes:
        template_name (str): The template used for rendering the view. Set to "product/list.html".
        context_object_name (str): The name of the context variable containing the filtered products.
        filterset_class (class): The filter class used to filter products by name (`ProductFilter`).
        extra_context (dict): Additional context passed to the template, in this case, `product_name_filter` for searching products by name.
    """

    title = "Filtered Products"
    template_name = "product/list.html"
    context_object_name = "products"
    filterset_class = ProductFilter
    extra_context = {"product_name_filter": ProductFilter}


class ProductDetailView(TitleMixin, DetailView):
    """
    A view that displays the detailed information of a product, including whether the user has already submitted a review.
    """

    title = "Product Detail"
    model = Product
    template_name = "product/detail.html"
    context_object_name = "product"
    extra_context = {
        "product_name_filter": ProductFilter,
        "product_review_form": ReviewForm,
    }

    def get_context_data(self, **kwargs) -> dict:
        """
        Retrieves additional context data, including checking if the user has already reviewed the product.
        """
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        if self.request.user.is_authenticated:
            user_review_exists = Review.objects.filter(
                user=self.request.user, product=product
            ).exists()
        else:
            user_review_exists = False

        context["user_review_exists"] = user_review_exists
        return context


class BasketListView(PromoCodeMixin, TitleMixin, LoginRequiredMixin, ListView):
    """
    A view that displays the list of products in the user's basket, with the option to apply a promo code.
    """

    title = "Basket"
    template_name = "basket/list.html"
    context_object_name = "baskets"
    form_class = PromoCodeForm
    extra_context = {"product_name_filter": ProductFilter, "promo_form": PromoCodeForm}
    success_url = reverse_lazy("basket")

    def get_queryset(self) -> QuerySet:
        """
        Retrieves the list of baskets associated with the current user.
        """
        return self.request.user.baskets.all()


class BasketAddView(LoginRequiredMixin, View):
    """
    A view that adds a product to the user's basket. If the product is already in the basket, its quantity is updated.
    """

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Adds a product to the basket or updates its quantity.
        """
        user = request.user
        product = get_object_or_404(Product, pk=request.POST["product_pk"])
        quantity = int(request.POST["quantity"])
        basket = Basket.objects.get_or_create(user=user, product=product)[0]
        basket.quantity += quantity
        basket.save()
        return HttpResponseRedirect(request.META["HTTP_REFERER"])


class BasketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    A view that allows the user to delete an item from their basket.
    """

    model = Basket
    template_name = "basket/list.html"
    success_url = reverse_lazy("basket")

    def test_func(self) -> bool:
        """
        Checks if the basket item belongs to the current user.
        """
        basket = self.get_object()
        return basket.user == self.request.user


class ReviewCreateView(LoginRequiredMixin, FormView):
    """
    A view for creating a review for a product.
    """

    form_class = ReviewForm

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Initializes the product object based on the provided slug in the URL.
        Checks if the user has already submitted a review for this product.
        If a review exists, returns a forbidden response.
        """
        self.product = get_object_or_404(Product, slug=self.kwargs["slug"])

        # Check if the user has already submitted a review for this product
        if Review.objects.filter(user=request.user, product=self.product).exists():
            return HttpResponseForbidden(
                "You have already submitted a review for this product."
            )

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: ReviewForm) -> HttpResponse:
        """
        Saves the review and associates it with the current user and product.
        """
        form.instance.user = self.request.user
        form.instance.product = self.product
        form.save()

        messages.success(self.request, "Your review has been submitted successfully.")
        return super().form_valid(form)

    def form_invalid(self, form: ReviewForm) -> HttpResponse:
        """
        Displays an error message if the form is invalid.
        """
        messages.error(self.request, "There was an error with your review.")
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        """
        Returns the success URL to redirect the user to the product detail page after a successful review.
        """
        return reverse_lazy("product_detail", kwargs={"slug": self.product.slug})


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    A view that allows the user to delete their review for a product.
    """

    model = Review
    pk_url_kwarg = "review_id"

    def get_success_url(self) -> str:
        """
        Returns the success URL after the review is deleted.
        """
        messages.success(self.request, "Your review has been deleted successfully.")
        return reverse_lazy("product_detail", kwargs={"slug": self.object.product.slug})

    def test_func(self) -> bool:
        """
        Ensures that the user is the owner of the review before allowing deletion.
        """
        review = get_object_or_404(Review, pk=self.kwargs["review_id"])
        return review.user == self.request.user
