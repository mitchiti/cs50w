from re import search
from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/search", views.search, name='search'),
    path("wiki/new_entry", views.new_entry, name="new_entry"),
    path("wiki/edit_entry/<str:entry>", views.edit_entry, name="edit_entry"),
    path("wiki/save_entry/<str:entry>", views.save_entry, name="save_entry"),
    path("wiki/random_entry", views.random_entry, name="random_entry"),
    path("wiki/<str:entry>", views.entry, name="entry")

]
