from django.contrib import admin
from django.urls import path
from .views import searchview, displayview
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("search/", searchview, name="search"),
    path("display/", displayview, name="display"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)