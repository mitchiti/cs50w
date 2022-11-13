from operator import truediv
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.db.models import Max
from decimal import Decimal

from .models import Category, Listing, User, Bid, Comment

class NewEntryForm (forms.Form):
    title =  forms.CharField(widget=forms.TextInput(attrs={'name':'title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'name':'description', 'style': 'height: 5em;'}))
    image =  forms.CharField(widget=forms.TextInput(attrs={'name':'image'}))
    price =  forms.CharField(widget=forms.TextInput(attrs={'name':'price'}))
    category =  forms.CharField(widget=forms.TextInput(attrs={'name':'category'}))
    # category = forms.MultipleChoiceField(["1", "2"])

class NewBidForm (forms.Form):
    bidValue =  forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Bid'}))

class NewCommentForm (forms.Form):
    text =  forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Comment'}))
 
def index(request):
    listings = Listing.objects.all()
    prices = []
    for listing in listings:
        bids = listing.ListingBids.all()
        if len(bids) > 0:
            max = listing.ListingBids.all().aggregate(Max('price'))["price__max"]
            price = f"${max:.2f}"
        else:
            price = f"${listing.price:.2f}"
        prices.append(price)

    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(), "prices": prices
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def category(request, category_id):
    category = Category.objects.get(pk=category_id)

    listings = Listing.objects.all()
    watching = []
    prices = []
    for listing in listings:
        if listing.category == category:
            watching.append(listing)
            bids = listing.ListingBids.all()
            if len(bids) > 0:
                max = listing.ListingBids.all().aggregate(Max('price'))["price__max"]
                price = f"${max:.2f}"
            else:
                price = f"${listing.price:.2f}"
            prices.append(price)

    return render(request, "auctions/category.html", {
        "listings": watching, "prices": prices, "category": category.name
    })

def watching(request):
    listings = Listing.objects.all()
    watching = []
    prices = []
    for listing in listings:
        if request.user in listing.watching_users.all():
            watching.append(listing)
            bids = listing.ListingBids.all()
            if len(bids) > 0:
                max = listing.ListingBids.all().aggregate(Max('price'))["price__max"]
                price = f"${max:.2f}"
            else:
                price = f"${listing.price:.2f}"
            prices.append(price)

    return render(request, "auctions/watching.html", {
        "listings": watching, "prices": prices
    })


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bids = listing.ListingBids.all()
    value = ""
    if request.method == "POST":
        if 'bid' in request.POST:
            form = NewBidForm(request.POST)
            if form.is_valid():
                bid = float(form.cleaned_data["bidValue"])           
                max = listing.ListingBids.all().aggregate(Max('price'))["price__max"]
                if (len(bids) == 0 and bid > listing.price) or (len(bids) > 0 and bid > max):
                    b = Bid(listing=listing, bidder=request.user, price=bid)
                    b.save()
                else:
                    value = 'Enter higher price'
        if 'comment' in request.POST:
            form = NewCommentForm(request.POST)
            if form.is_valid():
                c = Comment(listing=listing, text=form.cleaned_data["text"])
                c.save()
        if 'close' in request.POST:
            listing.sold = True
            listing.save()
        if 'watch' in request.POST:
            listing.watching_users.add(request.user)
            listing.save()
        if 'stopwatch' in request.POST:
            listing.watching_users.remove(request.user)
            listing.save()

    bids = listing.ListingBids.all()
    if len(bids) > 0:
        max_bid = bids[0]
        for bid in bids:
            if bid.price > max_bid.price:
                max_bid = bid

        max = max_bid.price
        max_bidder = max_bid.bidder
        if request.user == max_bidder:
            bid_message = f'{len(bids)} bids so far. Your bid is the current bid.'
        else:
            bid_message = f'{len(bids)} bids so far. {max_bidder} has the current bid.'
        price = f"${max:.2f}"
    else:
        max_bidder = "-"
        price = f"${listing.price:.2f}"
        bid_message = "No bids yet"

    form = NewBidForm()
    commentForm = NewCommentForm()
    comments = listing.ListingComments.all()
    watchers = listing.watching_users.all()
    owner = request.user == listing.seller
    return render(request, "auctions/listing.html", {
    "listing": listing, "price": price, "form": form, "commentform": commentForm,
    "message": value, "comments": comments, "owner": owner, "bid_message": bid_message, 
    "watching": request.user in watchers, "max_bidder": max_bidder
    })

def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            image = form.cleaned_data["image"]
            price = Decimal(form.cleaned_data["price"]) 
            print (request.POST["category"])
            for cat in Category.objects.all():
                if cat.name == request.POST["category"]:
                    category = cat

        l = Listing(title=title, description=description, image_source=image, seller=request.user, price=price, category=category)
        l.save()

        form = NewBidForm()
        commentForm = NewCommentForm()
        comments = l.ListingComments.all()
        watchers = l.watching_users.all()
        owner = True
        price = f"${l.price:.2f}"
        return render(request, "auctions/listing.html", {
        "listing": l, "price": price, "form": form, "commentform": commentForm,
        "message": "", "comments": comments, "owner": owner, "bid_message": "No bids yet", 
        "watching": request.user in watchers
        })
    else:
        form = NewEntryForm()
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "form": form, "categories": categories
        })




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
