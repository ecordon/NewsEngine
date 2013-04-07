from urlparse import urlparse

_author__ = "Lucas Ou-Yang, Evan O'Keeffe"
__date__ = "April 6th, 2013"
__version__ = "0.0.1"

class NewsWebsite:
    def __init__(self, raw_link, title = None, summary = None):
        self.raw_link = raw_link
        self.domain = urlparse(self.raw_link).scheme + "://" + urlparse(self.raw_link).netloc
        self.title = title
        self.summary = summary

        # If we are not setting a default title, manually guess and
        # create it based on the domain
        if self.title is None:
            objs = urlparse(raw_link).netloc.split(".")[1:-1]
            objs = [obj.capitalize() for obj in objs]
            self.title = ' '.join(objs)
