from django.db import models

class Feed(models.Model):
    link = models.CharField(max_length=100, default="")
    title = models.CharField(max_length=100, default="")
    description = models.TextField()

class Entry(models.Model):
    entry_id = models.CharField(max_length=200, default="")
    link = models.CharField(max_length=200, default="")
    published = models.DateTimeField()
    summary = models.TextField()

class Category(models.Model):
    name = models.CharField(max_length=20)

class RssChannel(models.Model):
    name = models.CharField(max_length=30, default="")
    url = models.CharField(max_length=200, default="")
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    feed_id = models.ForeignKey(Feed, on_delete=models.CASCADE, null=True, blank=True)
    entries_ids = models.ManyToManyField(Entry)

class Users(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=10, default="")
    password = models.CharField(max_length=10, default="")
    is_admin = models.BooleanField()
    channels_ids = models.ManyToManyField(RssChannel)
