from django.apps import AppConfig

class CoreConfig(AppConfig): # Replace 'CoreConfig' with your actual app config class name
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core' # Replace 'core' with your actual app name

    def ready(self):
        """
        Import signals here so they are connected when the app is ready.
        """
        import core.signals # Replace 'core' with your actual app name
