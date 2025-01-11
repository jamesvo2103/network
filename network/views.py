from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json

from .models import User, Post

def index(request):
        # Authenticated users view their inbox
    if request.user.is_authenticated:
        allPosts = Post.objects.order_by('-date').all()
        return render(request, "network/index.html", {
        "allPosts": allPosts
        })

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

def newPost(request):
    if request.method =="POST":
        content = request.POST.get('content', '').strip()
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content, user=user)
    
        post.save()

    return HttpResponseRedirect(reverse(index))


@login_required
def load_newsfeed(request, filter_type):
    # Filter posts based on filter type
    if filter_type == "all":
        posts = Post.objects.all()
    elif filter_type == "user":
        posts = Post.objects.filter(user=request.user)
    else:
        return JsonResponse({"error": "Invalid filter type."}, status=400)

    # Return posts in reverse chronological order
    posts = posts.order_by("-date").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)
@login_required
def post_detail(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    return JsonResponse(post.serialize())
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
