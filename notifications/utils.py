from .models import Notification

def create_notification(recipient, actor, verb, target=None):
    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target=target
    )
