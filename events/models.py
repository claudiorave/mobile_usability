from django.db import models
from rest_framework import serializers


# Create your models here.
class Event(models.Model):
    type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(null=True, blank=True)
    session = models.ForeignKey("Session", on_delete=models.CASCADE, related_name="events", null=True, blank=True)
    tarea= models.PositiveIntegerField(null=True, blank=True)
    sitio = models.ForeignKey("Sitio", on_delete=models.CASCADE, related_name="events", null=True, blank=True, default=None)

    class Meta:
        abstract = False

    @classmethod
    def get_serializer(cls):
        class BaseSerializer(serializers.ModelSerializer):
            class Meta:
                model = cls
                fields = '__all__'

        return BaseSerializer


class MisClicks(Event):
    x = models.FloatField()
    y = models.FloatField()

class Click(Event):
    x = models.FloatField(null=True, blank=True)
    y = models.FloatField(null=True, blank=True)

class PinchZoom(Event):
    percentage = models.FloatField(null=True, blank=True)


class Scroll(Event):
    scroll_points = models.TextField()


class Element(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="elements", null=True, blank=True)
    xpath = models.TextField(null=True, blank=True)


class Device(models.Model):
    phone = models.CharField(max_length=100, null=True)
    mobile = models.CharField(max_length=100, null=True)
    os = models.CharField(max_length=100, null=True)
    tablet = models.CharField(max_length=100, null=True)
    user_agent = models.CharField(max_length=100, null=True)
    build = models.CharField(max_length=100, null=True)
    height = models.FloatField(null=True)
    width = models.FloatField(null=True)
    webkit = models.FloatField(null=True)
    type = models.CharField(max_length=50)
    session = models.OneToOneField("Session", on_delete=models.CASCADE, related_name="device", null=True, blank=True)


class Session(models.Model):
    token = models.CharField(max_length=100, unique=True, primary_key= True)
    active = models.BooleanField(default=True)

class Sitio(models.Model):
    nombre = models.CharField(max_length=100)
    corregido = models.BooleanField()
