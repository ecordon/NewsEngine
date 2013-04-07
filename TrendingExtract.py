import feedparser

_author__ = "Lucas Ou-Yang, Evan O'Keeffe"
__date__ = "April 6th, 2013"
__version__ = "0.0.1"

def extract_trending(url='http://www.google.com/trends/hottrends/atom/feed?pn=p1'):
    listing = feedparser.parse(url)['entries']
    trends = []
    for item in listing:
        trends.append(item['title'])
    return trends