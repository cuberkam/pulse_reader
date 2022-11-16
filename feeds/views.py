import feedparser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import QueryDict
from django.shortcuts import render
from django.views import View

from .models import RssUrl, UserRss


class Feed(LoginRequiredMixin, View):
    def get(self, request):
        context = all_feeds(request)
        return render(request, "index.html", context)


@login_required
def all_feeds(request):
    user = request.user
    user_rss_urls = UserRss.objects.select_related().filter(user=user)
    all_feeds = []
    all_entries = []

    for item in user_rss_urls:
        d = feedparser.parse(str(item.rss_url))
        all_feeds.append({"title": d["feed"]["title"], "link": d["feed"]["link"]})

        for data in d["entries"]:
            summary = str(data["summary"]).split(">")
            try:
                text = summary[1]
            except Exception:
                text = summary[0]

            all_entries.append(
                {
                    "feed": d["feed"]["title"],
                    "title": data["title"],
                    "text": text,
                    "link": data["link"],
                }
            )

    context = {"all_feeds": all_feeds, "all_entries": all_entries}
    return context


@login_required
def subscribe_rss(request):
    post_data = QueryDict(request.body).dict()
    try:
        post_rss_url = post_data["rss_url"].split()[0]
    except Exception:
        return render(request, "partials/feed.html")

    is_rss_url = RssUrl.objects.filter(url=post_rss_url)

    if is_rss_url.exists():
        response = render(request, "partials/feed.html")
        return response

    rss_url = RssUrl.objects.create(url=post_rss_url)
    UserRss.objects.create(user=request.user, rss_url=rss_url)

    context = all_feeds(request)

    return render(request, "partials/feed.html", context)


@login_required
def unsubscribe_rss(request):
    pass
