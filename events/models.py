from django.db import models

# Create your models here.

class MisClicks(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    timestamp = models.DateTimeField()

class PinchZoom(models.Model):
    elements = models.TextField()
    percentage = models.FloatField()
    timestamp = models.DateTimeField()

class Scroll(models.Model):
    dom_object = models.TextField()
    x = models.FloatField()
    y = models.FloatField()
    timestamp = models.DateTimeField()
