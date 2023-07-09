from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.views import View

from .forms import CustomUserCreationForm, LoginForm


class IndexView(View):
    def get(self, request):
        return render(request, "auctions/index.html")


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "auctions/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            
            else:
                form = LoginForm()
                return render(
                    request,
                    "auctions/login.html",
                    {"message": "Invalid username and/or password.",
                    "form": form}
                )     

class LogoutView(View):
    def get(self, request):
        logout(request)
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