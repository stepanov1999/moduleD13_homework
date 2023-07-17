from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    PostCreateView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    UserLoginView,
    UserRegisterView,
    UserProfileView,
    EmailVereficationView,
    CommentCreateView,
    CommentListView,
    CommentDetailView,
    confirm_comment,
)


app_name = "users"

urlpatterns = [
    path("", PostCreateView.as_view(), name="add_post"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post"),
    path("post/<int:pk>/update", PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete", PostDeleteView.as_view(), name="post_delete"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("profile/<int:pk>/", UserProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "verify/<str:email>/<uuid:code>/",
        EmailVereficationView.as_view(),
        name="email_verefication",
    ),
    path(
        "comments/<int:pk>/comment_create",
        CommentCreateView.as_view(),
        name="comment_create",
    ),
    path("comments/", CommentListView.as_view(), name="comments"),
    path("comment/<int:pk>/", CommentDetailView.as_view(), name="comment"),
    path("comment/<int:pk>/confrim", confirm_comment, name="confirm"),
]
