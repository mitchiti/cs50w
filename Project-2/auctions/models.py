from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__ (self):
        return self.name

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    image_source = models.CharField(max_length=640)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="UserListings")
    date = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    sold = models.BooleanField(default=False)
    watching_users = models.ManyToManyField(User, blank=True, related_name="watchers")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="CategoryListings")

    def __str__ (self):
        return self.title

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="ListingBids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="UserBids")
    price = models.DecimalField(max_digits=6, decimal_places=2)


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="ListingComments")
    text = models.CharField(max_length=64)

