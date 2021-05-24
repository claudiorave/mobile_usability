import json
from django.forms.models import model_to_dict
from .models import MisClicks, Scroll, PinchZoom
import channels.layers
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from .serializers import MisClicksSerializer, ScrollSerializer, PinchZoomSerializer
from rest_framework.renderers import JSONRenderer


@receiver(post_save, sender=MisClicks)
def create_misclicks(sender, instance, created, **kwargs):
    channel_layer = channels.layers.get_channel_layer()
    group_name = 'chat'
    serializer = MisClicksSerializer(instance)
    if created:
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'chat_message',
                'message': json.dumps(serializer.data)
            }
        )


@receiver(post_save, sender=Scroll)
def create_scroll(sender, instance, created, **kwargs):
    channel_layer = channels.layers.get_channel_layer()
    group_name = 'chat'
    serializer = ScrollSerializer(instance)
    if created:
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'chat_message',
                'message': json.dumps(serializer.data)
            }
        )


@receiver(post_save, sender=PinchZoom)
def create_pinchzoom(sender, instance, created, **kwargs):
    channel_layer = channels.layers.get_channel_layer()
    group_name = 'chat'
    serializer = PinchZoomSerializer(instance)
    if created:
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'chat_message',
                'message': json.dumps(serializer.data)
            }
        )
