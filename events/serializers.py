from rest_framework import serializers
from .models import *
import django.dispatch

event_created = django.dispatch.Signal()


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = ['event', 'xpath']


class OrientationChangeSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        session_token = validated_data.pop('session')
        if Session.objects.filter(token=session_token).count() == 0:
            session = Session.objects.create(token=session_token)
        else:
            session = Session.objects.get(token=session_token)
        event = Event.objects.create(**validated_data, session=session)
        event_created.send(sender=self.__class__, instance=event)
        return event

    class Meta:
        model = Event
        fields = ['type', 'timestamp']


class MisClicksSerializer(serializers.ModelSerializer):
    elements = ElementSerializer(many=True)
    session = serializers.CharField(max_length=200)

    def create(self, validated_data):
        session_token = validated_data.pop('session')
        if Session.objects.filter(token=session_token).count() == 0:
            session = Session.objects.create(token=session_token)
        else:
            session = Session.objects.get(token=session_token)
        elements_data = validated_data.pop('elements')
        event = MisClicks.objects.create(**validated_data, session=session)
        for element_data in elements_data:
            Element.objects.create(event=event, **element_data)

        event_created.send(sender=self.__class__, instance=event)

        return event

    class Meta:
        model = MisClicks
        fields = ['type', 'x', 'y', 'elements', 'timestamp', 'session']


class PinchZoomSerializer(serializers.ModelSerializer):
    elements = ElementSerializer(many=True)
    session = serializers.CharField(max_length=200)

    def create(self, validated_data):
        session_token = validated_data.pop('session')
        if Session.objects.filter(token=session_token).count() == 0:
            session = Session.objects.create(token=session_token)
        else:
            session = Session.objects.get(token=session_token)
        elements_data = validated_data.pop('elements')
        event = PinchZoom.objects.create(**validated_data, session=session)
        for element_data in elements_data:
            Element.objects.create(event=event, **element_data)
        event_created.send(sender=self.__class__, instance=event)
        return event

    class Meta:
        model = PinchZoom
        fields = ['type', 'elements', 'percentage', 'timestamp', 'session']


class ScrollSerializer(serializers.ModelSerializer):
    elements = ElementSerializer(many=True)
    session = serializers.CharField(max_length=200)

    def create(self, validated_data):
        session_token = validated_data.pop('session')
        if Session.objects.filter(token=session_token).count() == 0:
            session = Session.objects.create(token=session_token)
        else:
            session = Session.objects.get(token=session_token)
        elements_data = validated_data.pop('elements')
        event = Scroll.objects.create(**validated_data, session=session)
        for element_data in elements_data:
            Element.objects.create(event=event, **element_data)
        event_created.send(sender=self.__class__, instance=event)
        return event

    class Meta:
        model = Scroll
        fields = ['type', 'scroll_points', 'timestamp', 'elements', 'session']


class DeviceSerializer(serializers.ModelSerializer):
    session = serializers.CharField(max_length=200)

    def create(self, validated_data):
        session_token = validated_data.pop('session')
        if Session.objects.filter(token=session_token).count() == 0:
            session = Session.objects.create(token=session_token)
        else:
            session = Session.objects.get(token=session_token)
        device = Device.objects.create(**validated_data, session=session)
        event_created.send(sender=self.__class__, instance=device)
        return device

    class Meta:
        model = Device
        fields = ['type', 'phone', 'mobile', 'tablet', 'os', 'webkit', 'build', 'user_agent', 'height', 'width',
                  'session']
