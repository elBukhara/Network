from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    #
    path("profile", views.profile, name="profile"),
    path("profile/<int:post_user>", views.user_profile, name="user"),
    path("all", views.allposts, name="allposts"),
    path("following", views.followingPosts, name="following"),
    #
    path("create", views.create, name="create"),
    path("follow/<int:post_user>", views.follow, name="follow"),
    path("unfollow/<int:post_user>", views.unfollow, name="unfollow"),
    path("like/<int:post_id>", views.like, name="like"), #API CALL
    path("edit/<int:post_id>", views.edit, name="edit") #API CALL
]