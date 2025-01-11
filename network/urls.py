
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("newPost", views.newPost, name="newPost"),
    path("posts/<int:post_id>", views.post_detail, name="post_detail"),
    path("posts/feed/<str:feed_type>", views.load_newsfeed, name="newsfeed"),
]
