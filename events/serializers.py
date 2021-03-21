from rest_framework import serializers
from .models import *


class MisClicksSerializer(serializers.ModelSerializer):
    class Meta:
        model = MisClicks
        fields = ['x', 'y', 'timestamp']


class PinchZoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = PinchZoom
        fields = ['elements', 'percentage', 'timestamp']


class ScrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scroll
        fields = ['dom_object', 'x', 'y', 'timestamp']
