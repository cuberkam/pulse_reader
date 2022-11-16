from django.urls import path

from .views import Feed, subscribe_rss

urlpatterns = [
    path("", Feed.as_view(), name="feed"),
    path("subscribe_rss", subscribe_rss, name="subscribe_rss"),
]
