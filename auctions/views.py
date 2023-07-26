from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.views import View

from auctions.forms import (
    CustomUserCreationForm,
    LoginForm,
    ListingForm,
    BidForm,
    CommentForm,
)
from auctions.models import Listing, Category


class IndexView(View):
    def get(self, request):
        listings = Listing.objects.get_active()
        return render(request, "auctions/index.html", {"listings": listings})


class WatchlistView(LoginRequiredMixin, View):
    def get(self, request):
        listings = request.user.watchlist.all()
        return render(request, "auctions/watchlist.html", {"listings": listings})


class WatchlistAPIView(LoginRequiredMixin, View):
    def post(self, request, pk):
        listing = get_object_or_404(Listing, pk=pk)
        user = request.user
        listing.watchlist.add(user)
        return JsonResponse({"message": "Item added to watchlist!", "tags": "info"})

    def delete(self, request, pk):
        listing = get_object_or_404(Listing, pk=pk)
        user = request.user
        listing.watchlist.remove(user)
        return JsonResponse(
            {"message": "Item removed from watchlist!", "tags": "danger"}
        )


class CreateListingView(LoginRequiredMixin, View):
    form_class = ListingForm
    login_url = reverse_lazy("login")

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            data = {**form.cleaned_data, "seller": request.user}
            Listing.objects.create(**data)
            messages.success(request, "The listing was successfully created.")
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {"form": form})

    def get(self, request):
        form = self.form_class
        return render(request, "auctions/create.html", {"form": form})


class DetailListingView(View):
    form_class = BidForm
    comment_form_class = CommentForm

    def get(self, request, slug):
        listing = get_object_or_404(
            Listing.objects.select_related("seller")
            .select_related("category")
            .prefetch_related("comments")
            .prefetch_related("comments__user"),
            slug=slug,
        )
        context = {"listing": listing}

        if request.user.is_authenticated:
            context["form"] = self.form_class(listing=listing, user=request.user)
            context["comment_form"] = self.comment_form_class(
                listing=listing, user=request.user
            )
        return render(request, "auctions/detail.html", context)

    @method_decorator(login_required)
    def post(self, request, slug):
        listing = get_object_or_404(Listing, slug=slug)
        context = {"listing": listing}
        form = BidForm(request.POST, listing=listing, user=request.user)
        comment_form = CommentForm(request.POST, listing=listing, user=request.user)
        if "form" in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, "You are the high bidder!")
                return HttpResponseRedirect(reverse("detail", args=[listing.slug]))
        if "comment_form" in request.POST:
            if comment_form.is_valid():
                comment_form.save()
                messages.success(request, "Your comment has been added!")
                return HttpResponseRedirect(reverse("detail", args=[listing.slug]))
        context["comment_form"] = comment_form
        context["form"] = form
        return render(request, "auctions/detail.html", context)

    @method_decorator(login_required)
    def patch(self, request, slug):
        """Updates the listing to CLOSE."""
        listing = get_object_or_404(Listing, slug=slug)

        if request.user != listing.seller:
            return JsonResponse(
                {"message": "The action could not be completed.", "tags": "danger"}
            )
        else:
            listing.is_active = False
            listing.save()
            if listing.number_of_bids == 0:
                winner = "nobody"
            else:
                winner = listing.high_bid.user.username

            return JsonResponse(
                {
                    "message": "The listing has been closed.",
                    "tags": "info",
                    "winner": winner,
                }
            )


class CategoryListView(View):
    def get(self, request, slug):
        category = Category.objects.get(slug=slug)
        listings = Listing.objects.get_active().filter(category=category)

        return render(
            request,
            "auctions/category.html",
            {"category": category.title, "listings": listings},
        )


class LoginView(View):
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, "auctions/login.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))

            else:
                form = self.form_class()
                messages.error(request, "Invalid username and/or password.")
                return render(
                    request,
                    "auctions/login.html",
                    {"form": form},
                )


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out.")
        return HttpResponseRedirect(reverse("index"))


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "auctions/register.html"
