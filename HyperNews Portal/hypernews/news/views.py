from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from datetime import datetime
import json


# Create your views here.
class ComingSoon(View):
    def get(self, request, *args, **kwargs):
        return redirect("/news/")


class NewsFromJSON(View):
    def get(self, request, number, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH) as f:
            json_file = json.load(f)
            for i in json_file:
                for key, value in i.items():
                    if i["link"] == number:
                        context = i
        return render(request, 'news/news.html', context=context)


class MainMenu(View):
    def get(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, encoding="utf-8") as f:
            json_file = json.load(f)
        news_dict = sorted(json_file, key=lambda x: x["created"], reverse=True)
        for i in news_dict:
            i["created"] = i["created"][:10]
        return render(request, 'news/menu.html', context={"data": news_dict})
        with open(settings.NEWS_JSON_PATH) as json_file:
            news_list = json.load(json_file)
            query = request.GET.get('q')
            if query:
                news_list = [
                    news for news in news_list if query in news['title']]
        return render(request, "news/menu.html", context={"news_list": news_list})


class CreateNews(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html', context={})

    def post(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, encoding="utf-8") as f:
            json_file = json.load(f)
        news_id = 1
        numbers = set([n["link"] for n in json_file])
        while news_id in numbers:
            news_id += 1
        news_to_add = {
            "created": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "text": request.POST["text"],
            "title": request.POST["title"],
            "link": news_id
        }
        json_file.append(news_to_add)
        with open(settings.NEWS_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(json_file, f)
        return redirect("/news")
