from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=640)
    price = models.IntegerField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="UserListings")
    date = models.DateField(auto_now_add=True)

    def __str__ (self):
        return self.title

class Bid(models.Model):
    pass

class Comment(models.Model):
    pass