from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class EventsConfig(AppConfig):
    name = 'events'

    def ready(self):
        import events.signals  # noqa