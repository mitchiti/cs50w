from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
import json

from .models import User, Post


def index(request):
    return render(request, "network/index.html")

def user(request, username):
    u = User.objects.filter(username=username)[0]
    return JsonResponse(u.serialize(request.user), safe=False)


@csrf_exempt
@login_required
def submit_post(request):
    print ("Posting")
    # Posting a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    text = data.get("text", "")
    if data.get("id") is not None:
        print("edited")
        post = Post.objects.get(pk=data.get("id"))
        post.text = text
    else:    
        post = Post(user=request.user, text=text)

    post.save()
    return JsonResponse({"message": "Post posted successfully."}, status=201)

def paginate_posts(request, posts):

    paginator = Paginator(posts, 10) 
    page_number = request.GET.get('page')
    print(page_number)
    page_obj = paginator.get_page(page_number)
    return JsonResponse({"posts": [post.serialize(request.user) for post in page_obj],
    "num_pages": paginator.num_pages}, safe=False)


@login_required
def posts(request):

    posts = Post.objects.all()

    # Return posts in reverse chronologial order
    posts = posts.order_by("-timestamp").all()
    # return JsonResponse([post.serialize(request.user) for post in posts], safe=False)
    return paginate_posts(request, posts)

@login_required
def aPost(request, post_id):

    post = Post.objects.filter(pk=post_id)
    return JsonResponse(post.serialize(request.user), safe=False)

@login_required
def following(request):

    user_is_following = request.user.following.all()
    posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all()
    following_posts = []
    for post in posts:
        if post.user in user_is_following:
            following_posts.append(post)

    return paginate_posts(request, following_posts)

@login_required
def user_posts(request, user):

    posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all()
    user_posts = []
    for post in posts:
        if post.user.username == user:
            user_posts.append(post)

    return paginate_posts(request, user_posts)

@login_required
@csrf_exempt
def follow(request, user_id):
    
    currentUser = request.user
    followedUser = User.objects.get(pk=user_id)

    data = json.loads(request.body)
    if data.get("follow"):
        currentUser.following.add(followedUser)
    else:
        currentUser.following.remove(followedUser)

    currentUser.save()

    return HttpResponse(status=204)

@login_required
@csrf_exempt
def like(request, post_id):
    
    currentUser = request.user
    post = Post.objects.get(pk=post_id)

    data = json.loads(request.body)
    if data.get("like"):
        post.likers.add(currentUser)
    else:
        post.likers.remove(currentUser)

    post.save()

    return HttpResponse(status=204)

#-----------------------------------------------------------------
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
