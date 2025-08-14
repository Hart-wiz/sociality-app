from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, UserDetail, MeUpdate, FollowToggle, Feed

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
    path("users/<str:username>/", UserDetail.as_view()),
    path("users/me/", MeUpdate.as_view()),
    path("follow/<int:user_id>", FollowToggle.as_view()),
    path("feed/", Feed.as_view()),
]
