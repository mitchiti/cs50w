from pyexpat import model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.serializers import serialize


class User(AbstractUser):
    pass
    following = models.ManyToManyField("User", null=True, related_name="followers")

    def serialize(self, user):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.first_name,
            "lastname": self.last_name,
            "following": serialize("json", self.following.all()),
            "followers": serialize("json", self.followers.all()),
            "userfollowing": user in self.followers.all(),
            "current": self.username == user.username
        }


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField("User", related_name="posts_liked")

    def serialize(self, user):
        return {
            "id": self.id,
            "poster": self.user.username,
            "text": self.text,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likers": serialize("json", self.likers.all()),
            "editable": self.user == user,
            "user_likes": user in self.likers.all()

        }

