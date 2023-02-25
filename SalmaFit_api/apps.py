from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SalmafitApiConfig(AppConfig):
    name = 'SalmaFit_api'
    verbose_name = 'Salma Style'

    def ready(self):
        import SalmaFit_api.signals

