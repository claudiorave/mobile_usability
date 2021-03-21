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