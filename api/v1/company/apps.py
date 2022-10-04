from django.apps import AppConfig


class CompanyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.v1.company'
    label = 'company'
    
    def ready(self):
        from api.v1.company import (
            signals,
            handlers,
        )
