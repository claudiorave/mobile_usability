from rest_framework import serializers
from .models import *

# class EventSerializer(serializers.ModelSerializer):
#     timestamp = serializers.SerializerMethodField()
#
#     class Meta:
#         model = MisClicks
#         fields = ['type', 'elements', 'timestamp']
#
#     def get_timestamp(self, obj):
#         print(obj)
#         return obj["timestamp"]


class MisClicksSerializer(serializers.ModelSerializer):

    class Meta:
        model = MisClicks
        fields = ['type', 'x', 'y', 'elements', 'timestamp']


class PinchZoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = PinchZoom
        fields = ['type', 'elements', 'percentage', 'timestamp']


class ScrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scroll
        fields = ['type', 'scroll_points', 'scroll_objects', 'timestamp']
