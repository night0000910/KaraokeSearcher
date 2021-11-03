from os import WIFSIGNALED
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    pass

class SearchHistoryModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    keyword = models.TextField(default="")
    datetime = models.DateTimeField(auto_now_add=True)

class SettingModel(models.Model): # 特定のユーザーの検索設定
    RANGE_CHOICES = ((1, "300m以内"), (2, "500m以内"), (3, "1000m以内"), (4, "2000m以内"), (5, "3000m以内"))
    COUNT_CHOICES = ((10, "10件"), (20, "20件"), (30, "30件"), (40, "40件"), (50, "50件"), (60, "60件"), (70, "70件"), (80, "80件"), (90, "90件"), (100, "100件"))
    ORDER_CHOICES = ((1, "店名かな順"), (4, "おすすめ順"))
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    range = models.IntegerField(default=3, choices=RANGE_CHOICES)
    count = models.IntegerField(default=100, choices=COUNT_CHOICES)
    order = models.IntegerField(default=4, choices=ORDER_CHOICES)
    capacity = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    card = models.BooleanField(default=False)
    non_smoking = models.BooleanField(default=False)
    other_memo = models.BooleanField(default=False)
    midnight = models.BooleanField(default=False)
    shop_detail_memo = models.BooleanField(default=False)


