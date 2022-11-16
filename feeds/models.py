from django.db import models


class RssUrl(models.Model):
    url = models.URLField(null=False, blank=False)

    def __str__(self):
        return self.url


class UserRss(models.Model):
    user = models.ForeignKey("users.CustomUser", models.CASCADE)
    rss_url = models.ForeignKey(RssUrl, models.CASCADE)

    def __str__(self):
        return f"User: {self.user} - Rss: {self.rss_url}"
