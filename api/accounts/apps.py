from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.accounts'
    
    def ready(self):
        import api.accounts.signals.handlers
