from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.views import View

from auctions.forms import CustomUserCreationForm, LoginForm, ListingForm
from auctions.models import Listing


class IndexView(View):
    def get(self, request):
        listings = Listing.objects.all()
        return render(request, "auctions/index.html", {"listings": listings})


class CreateListingView(LoginRequiredMixin,View):
    form_class = ListingForm
    login_url = reverse_lazy("login")
    
    def post(self, request):
        form = self.form_class(request.POST,request.FILES)
        
        if form.is_valid():
            data = {**form.cleaned_data, "seller": request.user}
            Listing.objects.create(**data)
            messages.success(request, "The listing was successfully created.")
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {"form": form})
        
        
    def get(self, request):
        form =self.form_class
        return render(request, "auctions/create.html", {"form": form})


class DetailListingView(View):
    def get(self, request, slug):
        listing = Listing.objects.get(slug=slug)
        return render(request, "auctions/detail.html", {"listing": listing})


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


# def register(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         email = request.POST["email"]

#         # Ensure password matches confirmation
#         password = request.POST["password"]
#         confirmation = request.POST["confirmation"]
#         if password != confirmation:
#             return render(
#                 request, "auctions/register.html", {"message": "Passwords must match."}
#             )


#         # Attempt to create new user
#         try:
#             user = User.objects.create_user(username, email, password)
#             user.save()
#         except IntegrityError:
#             return render(
#                 request,
#                 "auctions/register.html",
#                 {"message": "Username already taken."},
#             )
#         login(request, user)
#         return HttpResponseRedirect(reverse("index"))
#     else:
#         return render(request, "auctions/register.html")
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "auctions/register.html"
