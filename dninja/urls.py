from django.urls import path
from dninja.api import api


urlpatterns = [
    path("", api.urls)
]