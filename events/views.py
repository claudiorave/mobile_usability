from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
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


def index(request):
    misclicks_list = MisClicks.objects.order_by('timestamp')[:25]
    pinchzoom_list = PinchZoom.objects.order_by('timestamp')[:25]
    scroll_list = Scroll.objects.order_by('timestamp')[:25]
    template = loader.get_template('events/index.html')
    context = {
        'misclicks_list': misclicks_list,
        'pinchzoom_list': pinchzoom_list,
        'scroll_list': scroll_list,
    }
    return HttpResponse(template.render(context, request))

def reset(request):
    MisClicks.objects.all().delete()
    PinchZoom.objects.all().delete()
    Scroll.objects.all().delete()
    return redirect('/')
