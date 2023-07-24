from django.urls import path

from . import views

urlpatterns = [
    path("watchlist", views.WatchlistView.as_view(), name="watchlist"),
    path("<slug:slug>", views.DetailListingView.as_view(), name="detail"),
    path("category/<slug:slug>", views.CategoryListView.as_view(), name="category"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("create", views.CreateListingView.as_view(), name="create"),
    path("", views.IndexView.as_view(), name="index"),
]
