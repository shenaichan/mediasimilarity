from django.urls import path

from core.views import index

from .api import api

urlpatterns = [
    path("", index, name="index"),
    path("api/", api.urls),
]
