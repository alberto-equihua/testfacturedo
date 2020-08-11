import feedparser
from rssapp.models import Log

class RssChannelData():
    
    def __init__(self):
        self.feed = {}
        self.entries = []

    def get_data(self, url):
        feeds = entries = {}, []
        intents = 1
        data = None

        while intents <= 3:
            try:
                data = feedparser.parse(url)

                feeds = self._get_feed(data)
                entries = self._get_entries(data)
                intents = 4
            
            except Exception as e:
                intents += 1
                
                if intents == 3:
                    Log.objects.create(
                        url = url,
                        error = str(e)
                    )

        self.feed = feeds
        self.entries = entries

    def _get_feed(self, data):
        feed = data['feed']

        return {
            'link': feed['link'],
            'title': feed['title'],
            'description': feed['description']
        }

    def _get_entries(self, data):
        articles = []
        entries = data['entries']

        for entry in entries:
            articles.append({
                'id': entry['id'],
                'link': entry['link'],
                'published': entry['published'],
                'summary': entry['summary']
            })

        return articles