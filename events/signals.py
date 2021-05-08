from .models import MisClicks, Scroll, PinchZoom
import channels.layers
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=MisClicks)
@receiver(post_save, sender=Scroll)
@receiver(post_save, sender=PinchZoom)
def create_user_profile(sender, instance, created, **kwargs):
    channel_layer = channels.layers.get_channel_layer()
    group_name = 'chat'
    if created:
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'chat_message',
                'message': 'Elemento creado'
            }
        )

