from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from .models import Post, Follow
from .serializers import PostSerializer, UserPublicSerializer, MeUpdateSerializer

# Create your views here.

User = get_user_model()

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, "author_id", None) == request.user.id

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    def get_queryset(self):
        return Post.objects.select_related("author")
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.annotate(
        followers_count=Count("followers"),
        following_count=Count("following"),
    )
    lookup_field = "username"
    serializer_class = UserPublicSerializer

class MeUpdate(generics.UpdateAPIView):
    serializer_class = MeUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user

class FollowToggle(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, user_id):
        if request.user.id == int(user_id):
            return Response({"detail": "You cannot follow yourself."}, status=400)
        Follow.objects.get_or_create(follower=request.user, following_id=user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    def delete(self, request, user_id):
        Follow.objects.filter(follower=request.user, following_id=user_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Feed(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        me = self.request.user.id
        following_ids = Follow.objects.filter(follower_id=me).values_list("following_id", flat=True)
        return Post.objects.select_related("author").filter(Q(author_id__in=following_ids) | Q(author_id=me))
