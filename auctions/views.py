from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.views import View

from auctions.forms import CustomUserCreationForm, LoginForm, ListingForm, BidForm
from auctions.models import Listing


class IndexView(View):
    def get(self, request):
        listings = Listing.objects.get_active()
        return render(request, "auctions/index.html", {"listings": listings})


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

    def get(self, request, slug):
        listing = Listing.objects.prefetch_related("seller").get(slug=slug)
        context = {"listing": listing}

        if request.user.is_authenticated:
            context["form"] = self.form_class(listing=listing, user=request.user)
        return render(request, "auctions/detail.html", context)

    def post(self, request, slug):
        if request.user.is_authenticated:
            listing = get_object_or_404(Listing, slug=slug)
            context = {"listing": listing}
            form = BidForm(request.POST, listing=listing, user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "You are the high bidder!")
            else:
                context["form"] = form
                return render(request, "auctions/detail.html", context)
            return HttpResponseRedirect(listing.get_absolute_url())


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


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out.")
        return HttpResponseRedirect(reverse("index"))


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "auctions/register.html"
