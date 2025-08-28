# users/views.py or posts/views.py (depending on app structure)
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Post, Follow
from .serializers import PostSerializer, UserPublicSerializer, MeUpdateSerializer

User = get_user_model()

# ----------------------------
# Custom Permissions
# ----------------------------
class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Allow only the author of a post to edit/delete it.
    Read-only for everyone else.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, "author_id", None) == request.user.id


# -----------------------------
# Post ViewSet
# -----------------------------
class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD for posts.
    Anyone can read posts, only authors can edit/delete.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        # Optimize queries by selecting author data
        return Post.objects.select_related("author").all()

    def perform_create(self, serializer):
        # Automatically assign logged-in user as author
        serializer.save(author=self.request.user)


# -----------------------------
# User Detail View
# -----------------------------
class UserDetail(generics.RetrieveAPIView):
    """
    Retrieve public user info + followers/following counts
    """
    queryset = User.objects.annotate(
        followers_count=Count("followers"),
        following_count=Count("following"),
    )
    lookup_field = "username"
    serializer_class = UserPublicSerializer


# -----------------------------
# Update Logged-in User (Me)
# -----------------------------
class MeUpdate(generics.UpdateAPIView):
    """
    Update the profile of the currently logged-in user.
    """
    serializer_class = MeUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# -----------------------------
# Follow/Unfollow View
# -----------------------------
class FollowToggle(generics.GenericAPIView):
    """
    Toggle following/unfollowing a user.
    POST -> follow
    DELETE -> unfollow
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        if request.user.id == int(user_id):
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user exists
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Create follow if it doesn't exist
        Follow.objects.get_or_create(follower=request.user, following=target_user)
        return Response({"message": "followed"},status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, user_id):
        Follow.objects.filter(follower=request.user, following_id=user_id).delete()
        return Response({"message": "unfollowed"},status=status.HTTP_204_NO_CONTENT)


# -----------------------------
# Feed Pagination
# -----------------------------
class FeedPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


# -----------------------------
# Feed View
# -----------------------------
class Feed(generics.ListAPIView):
    """
    Display posts from users the logged-in user follows + own posts.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = FeedPagination

    def get_queryset(self):
        me_id = self.request.user.id
        # Get all user IDs that the current user follows
        following_ids = Follow.objects.filter(follower_id=me_id).values_list("following_id", flat=True)
        # Return posts by followed users or own posts
        return Post.objects.select_related("author").filter(
            Q(author_id__in=following_ids) | Q(author_id=me_id)
        ).order_by('-created_at')  # latest posts first
