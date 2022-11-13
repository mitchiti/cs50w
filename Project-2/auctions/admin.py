from django.contrib import admin
from .models import Category, User, Listing, Bid, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
