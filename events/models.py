from django.db import models
from rest_framework import serializers


# Create your models here.
class Event(models.Model):
    type = models.CharField(max_length=50)
    timestamp = models.DateTimeField()
    elements = models.TextField(null=True, blank=True)


    class Meta:
        abstract = True

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

class PinchZoom(Event):
    percentage = models.FloatField(null=True, blank=True)

class Scroll(Event):
    scroll_points = models.TextField()
    scroll_objects = models.TextField()
