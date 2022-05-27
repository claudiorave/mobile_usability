from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .models import *
from .serializers import *
from itertools import chain
from json import dumps


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

class SessionViewSet(ModelViewSet):
    queryset = Session.objects.all()
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
        elif self.request.data["type"] == 'orientationchange':
            return Event.objects.filter(type='orientationchange')
        elif self.request.data["type"] == 'device':
            return Device.objects.all()
        elif self.request.data["type"] == 'click':
            return Click.objects.all()

    def get_serializer_class(self):
        if self.request.data["type"] == 'misclick':
            return MisClicksSerializer
        elif self.request.data["type"] == 'pinchzoom':
            return PinchZoomSerializer
        elif self.request.data["type"] == 'scroll':
            return ScrollSerializer
        elif self.request.data["type"] == 'orientationchange':
            return OrientationChangeSerializer
        elif self.request.data["type"] == 'device':
            return DeviceSerializer
        elif self.request.data["type"] == 'click':
            return ClickSerializer

def home(request):
    session = Session.objects.all()
    context = {
        'session_list':session
    }
    template =loader.get_template('events/home.html')
    return HttpResponse(template.render(context, request))


def index(request, session):
    misclicks_list = MisClicks.objects.filter(session=session).order_by('-timestamp')[:25]
    click_list = Click.objects.filter(session=session).order_by('-timestamp')[:25]
    pinchzoom_list = PinchZoom.objects.filter(session=session).order_by('-timestamp')[:25]
    scroll_list = Scroll.objects.filter(session=session).order_by('-timestamp')[:25]
    orientation_change_list = Event.objects.filter(type="orientationchange", session= session).order_by('-timestamp')[:25]
    device = Device.objects.filter(session=session).last()
    template = loader.get_template('events/index.html')
    context = {
        'click_list': click_list,
        'misclicks_list': misclicks_list,
        'pinchzoom_list': pinchzoom_list,
        'scroll_list': scroll_list,
        'orientation_change_list': orientation_change_list,
        'device': device,
         'session': session,
    }
    return HttpResponse(template.render(context, request))


def unificada(request, session):
    misclicks_list = MisClicks.objects.filter(session=session).order_by('-timestamp')[:25]
    click_list = Click.objects.filter(session=session).order_by('-timestamp')[:25]
    pinchzoom_list = PinchZoom.objects.filter(session=session).order_by('-timestamp')[:25]
    scroll_list = Scroll.objects.filter(session=session).order_by('-timestamp')[:25]
    orientation_change_list = Event.objects.filter(type="orientationchange", session= session).order_by('-timestamp')[:25]
    device = Device.objects.filter(session=session).last()
    template = loader.get_template('events/unificada.html')
    eventos_list = list(chain(misclicks_list, pinchzoom_list, scroll_list, orientation_change_list, click_list))
    context = {
        'eventos_list': eventos_list,
        'device': device,
        'session': session,
    }
    return HttpResponse(template.render(context, request))


def timeline(request, session):
    session_list = Session.objects.all()
    misclicks_list = MisClicks.objects.filter(session=session).order_by('-timestamp')[:25]
    serializer = MisClicksSerializer(misclicks_list, many=True)
    misclicks_data = serializer.data
    clicks_list = Click.objects.filter(session=session).order_by('-timestamp')[:25]
    serializer = ClickSerializer(clicks_list, many=True)
    clicks_data = serializer.data
    pinchzoom_list = PinchZoom.objects.filter(session=session).order_by('-timestamp')[:25]
    serializer = PinchZoomSerializer(pinchzoom_list, many=True)
    pinchzoom_data = serializer.data
    scroll_list = Scroll.objects.filter(session=session).order_by('-timestamp')[:25]
    serializer = ScrollSerializer(scroll_list, many=True)
    scroll_data = serializer.data
    orientation_change_list = Event.objects.filter(type="orientationchange", session= session).order_by('-timestamp')[:25]
    serializer = OrientationChangeSerializer(orientation_change_list, many=True)
    orientation_change_data = serializer.data
    device = Device.objects.filter(session=session).last()
    template = loader.get_template('events/timeline.html')
    eventos_list = list(chain(misclicks_list, pinchzoom_list, scroll_list, orientation_change_list))
    data_list = list(chain(clicks_data, misclicks_data, pinchzoom_data, scroll_data, orientation_change_data))
    sorted(data_list, key=lambda i: (i['timestamp']))
    eventos = Event.objects.order_by('-timestamp')[:25]
    serializer = EventSerializer(eventos, many=True)
    context = {
        'eventos_list': eventos_list,
        'device': device,
        'dataJSON': dumps(data_list),
        'data_list': dumps(data_list),
        'session': session,
        'session_list': session_list



    }
    return HttpResponse(template.render(context, request))

def timeline_extra(request, session):
    session_list = Session.objects.all()
    misclicks_list = MisClicks.objects.filter(session=session).order_by('-timestamp')[:25]
    serializer = MisClicksSerializer(misclicks_list, many=True)
    misclicks_data = serializer.data
    pinchzoom_list = PinchZoom.objects.filter(session=session).order_by('-timestamp')[:25]
    serializer = PinchZoomSerializer(pinchzoom_list, many=True)
    pinchzoom_data = serializer.data
    scroll_list = Scroll.objects.filter(session=session).order_by('-timestamp')[:25]
    serializer = ScrollSerializer(scroll_list, many=True)
    scroll_data = serializer.data
    orientation_change_list = Event.objects.filter(type="orientationchange", session= session).order_by('-timestamp')[:25]
    serializer = OrientationChangeSerializer(orientation_change_list, many=True)
    orientation_change_data = serializer.data
    device = Device.objects.filter(session=session).last()
    template = loader.get_template('events/timeline_extra.html')
    eventos_list = list(chain(misclicks_list, pinchzoom_list, scroll_list, orientation_change_list))
    data_list = list(chain(misclicks_data, pinchzoom_data, scroll_data, orientation_change_data))
    sorted(data_list, key=lambda i: (i['timestamp']))
    eventos = Event.objects.order_by('-timestamp')[:25]
    serializer = EventSerializer(eventos, many=True)
    context = {
        'eventos_list': eventos_list,
        'device': device,
        'dataJSON': dumps(data_list),
        'data_list': dumps(data_list),
        'session': session,
        'session_list': session_list



    }
    return HttpResponse(template.render(context, request))

def reset(request, path):
    MisClicks.objects.all().delete()
    PinchZoom.objects.all().delete()
    Scroll.objects.all().delete()
    Event.objects.all().delete()
    Device.objects.all().delete()
    if path == "index":
        return redirect("/")
    else:
        return redirect("/eventos/" + path)
