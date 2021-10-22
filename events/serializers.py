from rest_framework import serializers
from .models import *
import django.dispatch

event_created = django.dispatch.Signal()


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = ['event', 'xpath']


class OrientationChangeSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        event = Event.objects.create(**validated_data)
        event_created.send(sender=self.__class__, instance=event)
        return event

    class Meta:
        model = Event
        fields = ['type', 'timestamp']


class MisClicksSerializer(serializers.ModelSerializer):
    elements = ElementSerializer(many=True)

    def create(self, validated_data):
        elements_data = validated_data.pop('elements')
        event = MisClicks.objects.create(**validated_data)
        for element_data in elements_data:
            Element.objects.create(event=event, **element_data)

        event_created.send(sender=self.__class__, instance=event)

        return event

    class Meta:
        model = MisClicks
        fields = ['type', 'x', 'y', 'elements', 'timestamp']


class PinchZoomSerializer(serializers.ModelSerializer):
    elements = ElementSerializer(many=True)

    def create(self, validated_data):
        elements_data = validated_data.pop('elements')
        event = PinchZoom.objects.create(**validated_data)
        for element_data in elements_data:
            Element.objects.create(event=event, **element_data)
        event_created.send(sender=self.__class__, instance=event)
        return event

    class Meta:
        model = PinchZoom
        fields = ['type', 'elements', 'percentage', 'timestamp']


class ScrollSerializer(serializers.ModelSerializer):
    elements = ElementSerializer(many=True)

    def create(self, validated_data):
        elements_data = validated_data.pop('elements')
        event = Scroll.objects.create(**validated_data)
        for element_data in elements_data:
            Element.objects.create(event=event, **element_data)
        event_created.send(sender=self.__class__, instance=event)
        return event

    class Meta:
        model = Scroll
        fields = ['type', 'scroll_points', 'timestamp', 'elements']


class DeviceSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        print(validated_data)
        event = Device.objects.create(**validated_data)
        event_created.send(sender=self.__class__, instance=event)
        return event

    class Meta:
        model = Device
        fields = ['type', 'phone', 'mobile', 'tablet', 'os', 'webkit', 'build', 'user_agent', 'height', 'width']
