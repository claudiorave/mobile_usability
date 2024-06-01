from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse
from django.template import loader
from django.db import connection
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
    queryset = Session.objects.filter(complete_balcon=True)
    serializer_class = SessionSerializer

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
    session = Session.objects.filter(complete_balcon=True)
    context = {
        'session_list':session
    }
    template =loader.get_template('events/home.html')
    return HttpResponse(template.render(context, request))

def tiempo_eventos_sitio(request):
    def my_custom_sql():

        with connection.cursor() as cursor:
            cursor.execute('''
          SELECT 
   sitio_id,
   nombre,
   corregido,
AVG(tiempo_total),
ROUND( AVG(conteo)::numeric, 2 ) as conteo_eventos
FROM
(SELECT 
   session_id,
   nombre,
   corregido,
   sitio_id,
   COUNT(*) as conteo,
   MAX(timestamp) - MIN(timestamp) as tiempo_total
FROM 
   public.events_event E JOIN public.events_session S ON E.session_id = S.token JOIN public.events_sitio SI ON E.sitio_id = SI.id
WHERE
 S.complete = true 
GROUP BY 
   session_id,
 nombre,
   corregido,
   sitio_id
ORDER BY
   session_id
) AS popcorn
GROUP BY
   sitio_id,
   nombre,
   corregido
ORDER BY
   sitio_id
   ;

            ''')
            row = cursor.fetchall()

        return row
    session = Session.objects.filter(complete_balcon=True)

    sitios = Sitio.objects.all()
    context = {
        'session_list': session,
        'sitios':sitios,
        'custom_sql': my_custom_sql(),
    }
    template =loader.get_template('events/tiempo_eventos_sitio.html')
    return HttpResponse(template.render(context, request))

def tiempo_eventos_sitio_sesiones(request):
    def my_custom_sql():
        raw_query = """
    SELECT 
  session_id,
   sitio_id,
   nombre,
   corregido,
AVG(tiempo_total),
ROUND( AVG(conteo)::numeric, 2 ) as conteo_eventos
FROM
(SELECT 
   session_id,
   nombre,
   corregido,
   sitio_id,
   COUNT(*) as conteo,
   MAX(timestamp) - MIN(timestamp) as tiempo_total
FROM 
   public.events_event E JOIN public.events_session S ON E.session_id = S.token JOIN public.events_sitio SI ON E.sitio_id = SI.id
WHERE
 S.complete = true 
GROUP BY 
   session_id,
 nombre,
   corregido,
   sitio_id
ORDER BY
   session_id
) AS popcorn
GROUP BY
   sitio_id,
   nombre,
   corregido,
   session_id
ORDER BY
   sitio_id
   ;
"""
        with connection.cursor() as cursor:
            cursor.execute(raw_query)
            row = cursor.fetchall()

        return row
    session = Session.objects.filter(complete_balcon=True)

    context = {
        'session_list': session,
        'custom_sql':my_custom_sql()
    }
    template =loader.get_template('events/tiempo_eventos_sitio_sesiones.html')
    return HttpResponse(template.render(context, request))
def tiempo_eventos_sitio_tipo(request):
    def my_custom_sql():
        raw_query = """
        SELECT 
        sitio_id,
        nombre,
        corregido,
        type,
        AVG(tiempo_total),
        ROUND( AVG(conteo)::numeric, 2 ) as conteo_eventos
        FROM
        (SELECT 
           session_id,
           sitio_id,
           nombre,
           corregido,
           type,
           COUNT(*) as conteo,
           MAX(timestamp) - MIN(timestamp) as tiempo_total
        FROM 
           public.events_event E JOIN public.events_session S ON E.session_id = S.token JOIN public.events_sitio SI ON E.sitio_id = SI.id
        WHERE
         S.complete = true 
        GROUP BY 
           session_id,
           sitio_id,
         nombre,
           corregido,
           tarea,
           type
        ORDER BY
           session_id
        ) AS popcorn
        GROUP BY
           sitio_id,
           nombre,
           corregido,
           type
        ORDER BY
        sitio_id
           ;
            """
        with connection.cursor() as cursor:
            cursor.execute(raw_query)
            row = cursor.fetchall()

        return row

    myorder = [0, 5, 2, 3, 1, 6, 10, 12, 9, 14, 16, 19, 17, 20, 15, 18]
    mylist = [my_custom_sql()[i] for i in myorder]
    session = Session.objects.filter(complete_balcon=True)

    context = {
        'session_list': session,
        'custom_sql':mylist
    }
    template =loader.get_template('events/tiempo_eventos_sitio_tipo.html')
    return HttpResponse(template.render(context, request))

def tiempo_eventos_sitio_tarea(request):
    def my_custom_sql():
        raw_query = """
        SELECT 
sitio_id,
tarea,
nombre,
corregido,
AVG(tiempo_total),
ROUND( AVG(conteo)::numeric, 2 ) as conteo_eventos
FROM
(SELECT 
   session_id,
   sitio_id,
   nombre,
   corregido,
   tarea,
   COUNT(*) as conteo,
   MAX(timestamp) - MIN(timestamp) as tiempo_total
FROM 
   public.events_event E JOIN public.events_session S ON E.session_id = S.token JOIN public.events_sitio SI ON E.sitio_id = SI.id
WHERE
 S.complete = true 
GROUP BY 
   session_id,
   sitio_id,
 nombre,
   corregido,
   tarea
ORDER BY
   session_id,
   tarea
) AS popcorn
GROUP BY
   sitio_id,
   nombre,
   corregido,
   tarea
ORDER BY
sitio_id,
tarea
   ;

            """
        with connection.cursor() as cursor:
            cursor.execute(raw_query)
            row = cursor.fetchall()

        return row

    dict = {
        "IOMA0": "Intro",
        "IOMA1": "Cerrar popups",
        "IOMA2": "Encontrar texto",
        "IOMA3": "Usar buscador",
        "Balcon0": "Intro",
        "Balcon1": "Abrir menú y encontrar opción",
        "Balcon2": "Usar buscador",
        "Balcon3": "Usar form con submit",
        "Balcon4": "Encontrar planta menor precio",
        "Kabytes0": "Intro",
        "Kabytes1": "Abrir menú y encontrar opción",
        "Kabytes2": "Usar buscador",
        "Kabytes3": "Presionar 3 botones LEER MÁS"
    }
    myorder = [0, 4, 1, 5, 2, 6, 3, 7, 8, 12, 9 , 13, 10, 14, 11, 15, 16, 20, 17, 21, 18, 22, 19, 23]
    mylist = [my_custom_sql()[i] for i in myorder]
    session = Session.objects.filter(complete_balcon=True)

    context = {
        'session_list': session,
        'custom_sql':mylist,
        'dict': dict
    }
    template =loader.get_template('events/tiempo_eventos_sitio_tarea.html')
    return HttpResponse(template.render(context, request))
def index(request, session):
    misclicks_list = MisClicks.objects.filter(session=session).order_by('-timestamp')
    click_list = Click.objects.filter(session=session).order_by('-timestamp')
    pinchzoom_list = PinchZoom.objects.filter(session=session).order_by('-timestamp')
    scroll_list = Scroll.objects.filter(session=session).order_by('-timestamp')
    orientation_change_list = Event.objects.filter(type="orientationchange", session= session).order_by('-timestamp')
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
    misclicks_list = MisClicks.objects.filter(session=session).order_by('-timestamp')
    click_list = Click.objects.filter(session=session).order_by('-timestamp')
    pinchzoom_list = PinchZoom.objects.filter(session=session).order_by('-timestamp')
    scroll_list = Scroll.objects.filter(session=session).order_by('-timestamp')
    orientation_change_list = Event.objects.filter(type="orientationchange", session= session).order_by('-timestamp')
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
    session_list = Session.objects.filter(complete_balcon=True)
    misclicks_list = MisClicks.objects.filter(session=session).order_by('-timestamp')
    serializer = MisClicksSerializer(misclicks_list, many=True)
    misclicks_data = serializer.data
    clicks_list = Click.objects.filter(session=session).order_by('-timestamp')
    serializer = ClickSerializer(clicks_list, many=True)
    clicks_data = serializer.data
    pinchzoom_list = PinchZoom.objects.filter(session=session).order_by('-timestamp')
    serializer = PinchZoomSerializer(pinchzoom_list, many=True)
    pinchzoom_data = serializer.data
    scroll_list = Scroll.objects.filter(session=session).order_by('-timestamp')
    serializer = ScrollSerializer(scroll_list, many=True)
    scroll_data = serializer.data
    orientation_change_list = Event.objects.filter(type="orientationchange", session= session).order_by('-timestamp')
    serializer = OrientationChangeSerializer(orientation_change_list, many=True)
    orientation_change_data = serializer.data
    device = Device.objects.filter(session=session).last()
    template = loader.get_template('events/timeline.html')
    eventos_list = list(chain(misclicks_list, pinchzoom_list, scroll_list, orientation_change_list))
    data_list = list(chain(clicks_data, misclicks_data, pinchzoom_data, scroll_data, orientation_change_data))
    sorted(data_list, key=lambda i: (i['timestamp']))
    eventos = Event.objects.order_by('-timestamp')
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
    session_list = Session.objects.filter(complete_balcon=True)
    misclicks_list = MisClicks.objects.filter(session=session).order_by('-timestamp')
    serializer = MisClicksSerializer(misclicks_list, many=True)
    misclicks_data = serializer.data
    pinchzoom_list = PinchZoom.objects.filter(session=session).order_by('-timestamp')
    serializer = PinchZoomSerializer(pinchzoom_list, many=True)
    pinchzoom_data = serializer.data
    scroll_list = Scroll.objects.filter(session=session).order_by('-timestamp')
    serializer = ScrollSerializer(scroll_list, many=True)
    scroll_data = serializer.data
    orientation_change_list = Event.objects.filter(type="orientationchange", session= session).order_by('-timestamp')
    serializer = OrientationChangeSerializer(orientation_change_list, many=True)
    orientation_change_data = serializer.data
    device = Device.objects.filter(session=session).last()
    template = loader.get_template('events/timeline_extra.html')
    eventos_list = list(chain(misclicks_list, pinchzoom_list, scroll_list, orientation_change_list))
    data_list = list(chain(misclicks_data, pinchzoom_data, scroll_data, orientation_change_data))
    sorted(data_list, key=lambda i: (i['timestamp']))
    eventos = Event.objects.order_by('-timestamp')
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

def metrica(request):
    session = Session.objects.filter(complete_balcon=True)
    context = {
        'session_list':session
    }
    template =loader.get_template('events/metrica.html')
    return HttpResponse(template.render(context, request))

def crear(request):
    session = Session.objects.filter(complete_balcon=True)
    context = {
        'session_list':session
    }
    template =loader.get_template('events/crear.html')
    return HttpResponse(template.render(context, request))
