from django.urls import include, path

from djoser import views, serializers


urlpatterns = [
    path("auth/", include("djoser.urls")),
    path('auth/', include('djoser.urls.jwt')),
]

