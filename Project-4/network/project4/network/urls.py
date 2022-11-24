
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("post/", views.submit_post, name="submit_post"),
    path("posts/", views.posts, name="posts"),
    path("following/", views.following, name="following"),
    path("user_posts/<str:user>", views.user_posts, name="user_posts"),
    path("user/<str:username>", views.user, name="user"),
    path("follow/<str:user_id>", views.follow, name="follow"),
    path("like/<str:post_id>", views.like, name="like"),
    path("aPost/<str:post_id>", views.like, name="like"),

]
