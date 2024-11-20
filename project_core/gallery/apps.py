from django.apps import AppConfig


class GalleryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gallery'
    
    def ready(self):
        import project_core.gallery.api.v1.signals


