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

urlpatterns = [
    path('', index, name='index'),
    path('reset', reset, name='index'),
]

urlpatterns += router.urls
