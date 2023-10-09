import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    return render(request, "network/index.html")

def allposts(request):
    p = Paginator(Post.objects.all().order_by("-timestamp").all(), 10)
    page = request.GET.get('page')
    posts = p.get_page(page)

    liked_posts = get_liked_posts(request)

    return render(request, "network/allPosts.html", {
        "posts": posts,
        "liked_posts": liked_posts
    })

def followingPosts(request):
    current_user = request.user
    following_users = current_user.user_following.all()

    p = Paginator(Post.objects.filter(user__in=following_users).order_by("-timestamp").all(), 10)
    page = request.GET.get('page')
    posts = p.get_page(page)

    liked_posts = get_liked_posts(request)

    #If the user clicks 'following posts' this variable denotes to change the heading 
    PostsFromFollowing = True
    
    return render(request, "network/allPosts.html", {
        "posts": posts,
        "liked_posts": liked_posts,
        "PostsFromFollowing": PostsFromFollowing
    })

# For rendering user's own profile 
def profile(request):
    current_user = request.user

    p = Paginator(Post.objects.filter(user=request.user).order_by("-timestamp").all(), 10)
    page = request.GET.get('page')
    posts = p.get_page(page)

    liked_posts = get_liked_posts(request)

    followers = current_user.user_followers.all()
    following = current_user.user_following.all()

    return render(request, "network/profile.html", {
        "posts": posts,
        "followers": followers,
        "following": following,
        "liked_posts": liked_posts
    })

def user_profile(request, post_user):
    current_user = request.user
    user = User.objects.get(id=post_user)
    if current_user == user:
        return profile(request)
    else:
        p = Paginator(Post.objects.filter(user=user).order_by("-timestamp").all(), 10)
        page = request.GET.get('page')
        posts = p.get_page(page)
        
        # Setting IsFollowing to False for those who are not authenticated
        IsFollowing = False
        
        if current_user.is_authenticated:
            # Checking if someone's profile is following or not by the current user
             
            IsFollowing = user in current_user.user_following.all()

        followers = user.user_followers.all()
        following = user.user_following.all()

        liked_posts = get_liked_posts(request)

        return render(request, "network/user_profile.html", {
            "posts": posts,
            "user": user,
            "IsFollowing": IsFollowing,
            "followers": followers,
            "following": following,
            "liked_posts": liked_posts
        })


def get_liked_posts(request):
    # This function is designed to add all liked posts from the current user:
    # Through the webpage and by this list we check if each post is within
    # Then we assign the like/unlike button 
    liked_posts = []
    if request.user.is_authenticated:
        current_user = request.user
        liked_posts = current_user.likes.values_list('id', flat=True)
    return liked_posts


@csrf_exempt
@login_required
def create(request):
    # Composing a new email must be via POST
    if request.method == "POST":
        body = request.POST['body']
        post = Post(
            user=request.user,
            body=body,
        )
        post.save()
        return HttpResponseRedirect(reverse("profile"))

@csrf_exempt
@login_required
def like(request, post_id):
    user = User.objects.get(id=request.user.id)
    post = Post.objects.get(id=post_id)

    # If has already liked the post: 
    if user in post.likes.all():
        post.likes.remove(user)    
    else:
        post.likes.add(user)

    return JsonResponse({"message": "Post was liked/disliked"})

@csrf_exempt
@login_required
def edit(request, post_id):
    # Get original post
    post = Post.objects.get(pk=post_id)

    # Gets new text (edited) in JSON format
    data = json.loads(request.body)
    new_text = data.get("post", "t")
    # Update post to new text
    post.body = new_text
    post.save()

    return JsonResponse({"message": "Post was edited", "new_text": new_text}, status=201)


@csrf_exempt
@login_required
def follow(request, post_user):
    user = User.objects.get(id=int(post_user))
    subscriber = request.user
    user.user_followers.add(subscriber)
    subscriber.user_following.add(user)
    return HttpResponseRedirect(reverse("user",args=(post_user, )))

@csrf_exempt
@login_required
def unfollow(request, post_user):
    user = User.objects.get(id=int(post_user))
    subscriber = request.user
    user.user_followers.remove(subscriber)
    subscriber.user_following.remove(user)
    return HttpResponseRedirect(reverse("user",args=(post_user, )))


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