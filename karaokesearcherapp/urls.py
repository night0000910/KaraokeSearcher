from django.contrib import admin
from django.urls import path
from .views import searchview, displayview, signupview, loginview, logoutview, settingview, search_historyview
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("signup/", signupview, name="signup"),
    path("login/", loginview, name="login"),
    path("logout/", logoutview, name="logout"),
    path("search/", searchview, name="search"),
    path("display/<str:keyword>/", displayview, name="display"),
    path("setting/", settingview, name="setting"),
    path("search_history/", search_historyview, name="search_history")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)