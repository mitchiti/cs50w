from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("categories", views.register, name="categories"),
    path("watchlist", views.register, name="watchlist"),
    path("create", views.register, name="create")


]
