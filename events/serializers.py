from rest_framework import serializers
from .models import *


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
