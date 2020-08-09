import feedparser
import logging
logger = logging.getLogger(__name__)

class RssChannelData:
    error = ""

    def get_data(self, url):
        this = self
        this.error = ""
        feeds = entries = {}, []
        intents = 1

        while intents <= 3:
            try:
                data = feedparser.parse(url)
                feeds = self._get_feed()
                entries = self._get_entries()
                intents = 3
            except Exception as e:
                intents += 1
                if intents >= 3:
                    this.error = e
                    logger.error(e)
        return feeds, entries

    def _get_feed(self):
        feed = self.data['feed']

        return {
            'link': feed['link'],
            'title': feed['title'],
            'description': feed['description']
        }

    def _get_entries(self):
        articles = []
        entries = self.data['entries']

        for entry in entries:
            articles.append({
                'id': entry['id'],
                'link': entry['link'],
                'published': entry['published'],
                'summary': entry['summary']
            })

        return articles