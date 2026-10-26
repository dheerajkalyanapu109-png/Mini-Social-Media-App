from django.contrib.auth import views as auth
from django.urls import path
from . import views as v
urlpatterns = [
    path("", v.feed, name="feed"),
    path("post/new/", v.post_create, name="post_create"),
    path("post/<int:pk>/", v.post_detail, name="post_detail"),
    path("post/<int:pk>/comment/", v.comment_add, name="comment_add"),
    path("post/<int:pk>/like/", v.like_toggle, name="like_toggle"),
    path("u/<str:username>/", v.profile, name="profile"),
    path("u/<str:username>/follow/", v.follow_toggle, name="follow_toggle"),
    path("settings/profile/", v.edit_profile, name="edit_profile"),
    path("register/", v.register, name="register"),
    path("login/", auth.LoginView.as_view(), name="login"),
    path("logout/", auth.LogoutView.as_view(), name="logout"),
]
