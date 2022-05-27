import json
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from .models import MisClicks, Scroll, PinchZoom, Element
import channels.layers
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from .serializers import *
from rest_framework.renderers import JSONRenderer


@receiver(event_created)
def my_callback(sender, instance, **kwargs):
    channel_layer = channels.layers.get_channel_layer()
    group_name = instance.session.token
    print(instance)
    if instance.type == 'misclick':
        serializer = MisClicksSerializer(instance)
    elif instance.type == "pinchzoom":
        serializer = PinchZoomSerializer(instance)
    elif instance.type == "scroll":
        serializer = ScrollSerializer(instance)
    elif instance.type == "orientationchange":
        serializer = OrientationChangeSerializer(instance)
    elif instance.type == "device":
        serializer = DeviceSerializer(instance)
    elif instance.type == "click":
        serializer = ClickSerializer(instance)

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'chat_message',
            'message': serializer.data
        }
    )

