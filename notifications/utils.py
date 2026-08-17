from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notification


def send_notification(user, notif_type, message):
    # Always save to the database first — so it's not lost if the user is offline
    Notification.objects.create(user=user, type=notif_type, message=message)

    # Then push it live if they happen to be connected right now
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_{user.id}",
        {
            "type": "send_notification",   # must match the method name in the consumer
            "notification_type": notif_type,
            "message": message,
        }
    )