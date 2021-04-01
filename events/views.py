from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
# Create your views here.

class MisClicksViewSet(ModelViewSet):
    queryset = MisClicks.objects.all()
    serializer_class = MisClicksSerializer


class PinchZoomViewSet(ModelViewSet):
    queryset = PinchZoom.objects.all()
    serializer_class = PinchZoomSerializer


class ScrollViewSet(ModelViewSet):
    queryset = Scroll.objects.all()
    serializer_class = ScrollSerializer

class EventViewSet(ModelViewSet):
    def get_queryset(self):
        print(self.request.data)
        if self.request.data["type"] == 'misclicks':
            return MisClicks.objects.all()
        elif self.request.data["type"] == 'pinchzoom':
            return PinchZoom.objects.all()
        elif self.request.data["type"] == 'scroll':
            return Scroll.objects.all()

    def get_serializer_class(self):
        print(self.request.data)
        if self.request.data["type"] == 'misclick':
            return MisClicksSerializer
        elif self.request.data["type"] == 'pinchzoom':
            return PinchZoomSerializer
        elif self.request.data["type"] == 'scroll':
            return ScrollSerializer
