from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *

app_name = "events"

router = DefaultRouter()

# url de grupo_permiso
router.register(r'pinchzoom', PinchZoomViewSet, basename='pinchzoom')
router.register(r'misclicks', MisClicksViewSet, basename='misclicks')
router.register(r'scroll', ScrollViewSet, basename='scroll')
router.register(r'event', EventViewSet, basename='event')
router.register(r'session', SessionViewSet, basename='session')

urlpatterns = [
    path('', home, name='home'),
    path('metrica', metrica, name='metrica'),
    path('crear', crear, name='crear'),
    path('tiempo_eventos_sitio', tiempo_eventos_sitio, name='tiempo_eventos_sitio'),
    path('tiempo_eventos_sitio_sesiones', tiempo_eventos_sitio_sesiones, name='tiempo_eventos_sitio_sesiones'),
    path('tiempo_eventos_sitio_tipo', tiempo_eventos_sitio_tipo, name='tiempo_eventos_sitio_tipo'),
    path('tiempo_eventos_sitio_tarea', tiempo_eventos_sitio_tarea, name='tiempo_eventos_sitio_tarea'),
    path('eventos/<str:session>/', index, name='index'),
    path('reset/<str:path>/', reset, name='index'),
    path('unificada/<str:session>/', unificada, name='unificada'),
    path('timeline/<str:session>/', timeline, name='timeline'),
    path('timeline_extra/<str:session>/', timeline_extra, name='timeline'),

]

urlpatterns += router.urls
