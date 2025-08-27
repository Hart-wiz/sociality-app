from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Notification
from  users.models import CustomUser  # Adjust if your user model is elsewhere

class UserSummarySerializer(serializers.ModelSerializer):
    """Minimal serializer for users (actor & recipient)."""
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "avatar_url"]  # add avatar if you have it


class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserSummarySerializer(read_only=True)
    actor = UserSummarySerializer(read_only=True)
    target_object = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            "id",
            "recipient",
            "actor",
            "verb",
            "target_object",
            "timestamp",
            "read",
        ]

    def get_target_object(self, obj):
        """Serialize the target of the notification."""
        if obj.target is None:
            return None

        # Example: handle known types (Post, Comment, etc.)
        if obj.target_content_type.model == "post":
            return {
                "id": obj.target.id,
                "title": getattr(obj.target, "title", None),
                "content": getattr(obj.target, "content", None),
            }
        elif obj.target_content_type.model == "comment":
            return {
                "id": obj.target.id,
                "text": getattr(obj.target, "text", None),
            }

        # Default if not explicitly handled
        return {"id": obj.target.id, "type": obj.target_content_type.model}
