from rest_framework import serializers
from rssapp.models import Users, RssChannel, Category, Feed, Entry

class UsersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = ['id','name','username','is_admin']
    
class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id','name']

class FeedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Feed
        fields = ['id','link','title','description']

class EntrySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Entry
        fields = ['id','entry_id','link','published','summary']

class RssChannelSerializer(serializers.ModelSerializer):
    category_id = CategorySerializer(many=False, read_only=False)
    feed_id = FeedSerializer(many=False, read_only=False)
    entries_ids = EntrySerializer(many=True, read_only=False)

    class Meta:
        model = RssChannel
        fields = ['id','name','url','category_id', 'feed_id', 'entries_ids']

