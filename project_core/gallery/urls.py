from django.urls import include, path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from .views import *

app_name = 'gallery'

urlpatterns = [
    path('api/v1/', include('gallery.api.v1.urls')),
 
]
