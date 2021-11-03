from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate, login, logout
from .models import UserModel, SearchHistoryModel, SettingModel

import urllib.request
import urllib.parse
import requests
import datetime


def signupview(request):
    if request.method == "GET":
        return render(request, "signup.html")

    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user_set = get_user_model().objects.all()
        duplicate = False

        for user in user_set:
            if username == user.username:
                duplicate = True
        
        if not duplicate:
            user = get_user_model().objects.create_user(username, "", password)
            SettingModel.objects.create(user=user)
            return redirect("login")

        else:
            return render(request, "signup.html", {"error" : "既に同じ名前のユーザーが存在します"})


def loginview(request):
    if request.method == "GET":
        return render(request, "login.html")

    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print(f"ユーザー : {user}")
        if user is not None:
            login(request, user)
            return redirect("search")
        else:
            return render(request, "login.html", {"error" : "ユーザー名、またはパスワードが間違っています"})

def logoutview(request):
    logout(request)
    return redirect("login")

def searchview(request):
    if request.method == "GET":
        return render(request, "search.html")
    elif request.method == "POST":
        keyword = request.POST["keyword"]

        if not keyword:
            return redirect("search")

        return redirect("display", keyword=keyword)


def displayview(request, keyword):
    if request.method == "GET":
        if request.user.is_authenticated:
            setting = SettingModel.objects.get(user=request.user.id)
            request_url = "https://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
            parameters = urllib.parse.urlencode({"key" : "e506073f251a9ca1", "keyword" : "カラオケ", "range" : str(setting.range), "format" : "json", "address" : keyword, "count" : str(setting.count), "order" : str(setting.order)})
            url = f"{request_url}?{parameters}"

            user = request.user
            if SearchHistoryModel.objects.filter(user=user.id).exists():
                if SearchHistoryModel.objects.last().keyword == keyword:
                    history = SearchHistoryModel.objects.last()
                    history.datetime = datetime.datetime.today()
                    history.save()
                else:
                    SearchHistoryModel.objects.create(user=user, keyword=keyword)
            else:
                SearchHistoryModel.objects.create(user=user, keyword=keyword)

        else:
            request_url = "https://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
            parameters = urllib.parse.urlencode({"key" : "e506073f251a9ca1", "keyword" : "カラオケ", "range" : "3", "format" : "json", "address" : keyword, "count" : "100", "order" : "4"})
            url = f"{request_url}?{parameters}"
            setting = {"capacity" : False, "wifi" : False, "card" : False, "non_smoking" : False, "other_memo" : False, "midnight" : False, "special_detail_memo" : False}

        res = requests.request("get", url)

        # resにはきちんと値が格納されている

        res_data = res.json()

        # res_dataにはきちんと値が格納されている

        shop_list = res_data["results"]["shop"]
        return render(request, "display.html", {"shop_list" : shop_list, "keyword" : keyword, "setting" : setting})


    elif request.method == "POST":
        keyword = request.POST["keyword"]

        if not keyword:
            previous_keyword = request.POST["previous_keyword"]
            return redirect("display", keyword=previous_keyword)

        print(f"検索キーワード : {keyword}")
        return redirect("display", keyword=keyword)

def settingview(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, "setting.html")
        elif request.method == "POST":

            if request.POST["range"] == "300m以内":
                range_data = 1
            elif request.POST["range"] == "500m以内":
                range_data = 2
            elif request.POST["range"] == "1000m以内":
                range_data = 3
            elif request.POST["range"] == "2000m以内":
                range_data = 4
            elif request.POST["range"] == "3000m以内":
                range_data = 5
            
            if request.POST["count"] == "10件":
                count_data = 10
            elif request.POST["count"] == "20件":
                count_data = 20
            elif request.POST["count"] == "30件":
                count_data = 30
            elif request.POST["count"] == "40件":
                count_data = 40
            elif request.POST["count"] == "50件":
                count_data = 50
            elif request.POST["count"] == "60件":
                count_data = 60
            elif request.POST["count"] == "70件":
                count_data = 70
            elif request.POST["count"] == "80件":
                count_data = 80
            elif request.POST["count"] == "90件":
                count_data = 90
            elif request.POST["count"] == "100件":
                count_data = 100

            if request.POST["order"] == "店名かな順":
                order_data = 1
            elif request.POST["order"] == "おすすめ順":
                order_data = 4

            capacity_data = request.POST["capacity"]
            wifi_data = request.POST["wifi"]
            card_data = request.POST["card"]
            non_smoking_data = request.POST["non_smoking"]
            other_memo_data = request.POST["other_memo"]
            midnight_data = request.POST["midnight"]
            shop_detail_memo_data = request.POST["shop_detail_memo"]

            user = request.user
            settings = SettingModel.objects.get(user=user.id)
            if request.POST["range"] != "サーチ範囲":
                settings.range = range_data
            if request.POST["count"] != "サーチ件数":
                settings.count = count_data
            if request.POST["order"] != "並び順":
                settings.order = order_data
            if request.POST["capacity"] != "総席数":
                settings.capacity = capacity_data
            if request.POST["wifi"] != "Wifiの有無":
                settings.wifi = wifi_data
            if request.POST["card"] != "カード可":
                settings.card = card_data
            if request.POST["non_smoking"] != "禁煙席":
                settings.non_smoking = non_smoking_data
            if request.POST["other_memo"] != "その他設備":
                settings.other_memo = other_memo_data
            if request.POST["midnight"] != "23時以降も営業":
                settings.midnight = midnight_data
            if request.POST["shop_detail_memo"] != "備考":
                settings.shop_detail_memo = shop_detail_memo_data
            settings.save()

            return redirect("setting")
    else:
        return redirect("login")

def search_historyview(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            user = request.user
            history_set = SearchHistoryModel.objects.filter(user=user.id)
            history_list = []

            for history in history_set:
                history_list.append(history)

            history_list.sort(key=lambda x: x.datetime.timestamp())
            history_list.reverse()

            return render(request, "search_history.html", {"history_list" : history_list})

        elif request.method == "POST":
            if request.POST["keyword"]:
                keyword = request.POST["keyword"]
                return redirect("display", keyword=keyword)
            else:
                return redirect("search_history")
    else:
        return redirect("login")
