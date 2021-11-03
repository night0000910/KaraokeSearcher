from django.contrib import admin
from .models import UserModel, SearchHistoryModel, SettingModel

admin.site.register(UserModel)
admin.site.register(SearchHistoryModel)
admin.site.register(SettingModel)
