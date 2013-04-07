from urlparse import urlparse

_author__ = "Lucas Ou-Yang, Evan O'Keeffe"
__date__ = "April 6th, 2013"
__version__ = "0.0.1"

class Link:
    def __init__(self, href, website, img_src = None, title = None):
        self.href = href
        self.title = title
        self.domain = urlparse(website).netloc
        self.img_src = img_src
        self.text = None

        # If the href is relative, begins with / ...
        # then just construct the absolute url
        if self.href[0] == "/":
            self.href = urlparse(website).scheme + "://" + self.domain + self.href

    def set_text(self, text):
        self.text = text

    def is_news(self):
        if self.title == None or not self.match_href() or \
                not self.match_length() or not self.match_slashes():
            return False
        return True

    # If the news websites are from the same domain, it's news.
    def match_href(self):
        if self.domain in self.href or self.href[0] == "/":
            return True
        return False

    # If the title exists and has fewer than four words,
    # or if its fewer than 20 chars, it's not news.
    def match_length(self):
        if self.title is not None and len(self.title.split(" ")) >= 4 \
            and len(self.title) >= 20:
            return True
        return False

    # If the title has
    def match_slashes(self):
        chunked = self.href.replace("http://", "")
        if chunked.count("/") > 1:
            return True
        return False