import urllib2
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse
import os

from Link import Link
from EasyUnicode import *

__author__ = "Lucas Ou-Yang, Evan O'Keeffe"
__date__ = "April 6th, 2013"
__version__ = "0.0.1"
# Feeds in a list of news websites, goes into each website
# and extracts all suspected news links. Uses educated guessing
# along with memoization to decide. Outputs a big list of
# all of the link objects to these news websites

# Performs a depth check on the <> html tag, we want the title
# Which is usually the text NOT present inside a tag. So we scan and
# Extract the title out by filtering out unneeded tags.

def grab_img_src(link):
    try:
        # Searches for a nested <img> tag in the html, then
        # extracts the source value if avalible, None if not.
        return link.find("img")["src"]
    except Exception:
        return None

def find_articles(website):
    results = []
    try:
        html = urllib2.urlopen(website).read()
    except Exception:
        print "403 Forbidden"
        return []
    seeker_soup = BeautifulSoup(html)
    news_list = seeker_soup.findAll("a") # Extract all potential links

    for link in news_list:
        if link.get("href"): # Make sure it's not deformed
            link = Link(href = link["href"], website = website,
                        img_src = grab_img_src(link), title = link.getText())
            if link.is_news():
                results.append(link)

    results = set(results)
    return results

def domain_to_key(domain):
    return domain.split("://")[1] + ".txt"

MEMO_DIRECTORY = "Memoized_Articles"
def memoize(links, domain):
    directories = os.getcwd().split('/')
    if directories[-1] == "NewsEngine":
        if not os.path.exists(os.path.join(os.getcwd(), MEMO_DIRECTORY)):
            os.mkdir(MEMO_DIRECTORY)
        os.chdir(MEMO_DIRECTORY)
    # Else, we are already in the memoized articles file
    memo = {link.href : link for link in links}

    # If we are on our 2nd run or above, we begin to memoize
    if os.path.exists(domain_to_key(domain)):
        # r+ means open to reading and writing, file is not truncated down
        file_obj = open(domain_to_key(domain), "r+")
        # Python automatically handles platform differences \n handles \r\n also
        # Do not refactor into file_obj.read().split("\n"), for whatever reason,
        # that gives an empty string as output, as some weird bug?
        saved_links = file_obj.read()
        # Chop off the last element, it's just an empty string
        saved_links = saved_links.split("\n")[:-1]
        file_obj.close()
        for link in saved_links:
            if memo.get(link): # If the link lasts so long on a page, it's not news
                del memo[link]

    text = ""
    for link in memo.keys():
        text += link + "\n"

    # Override the txt file with a new list of links, for next time
    write_unicode_to_file(domain_to_key(domain) ,safe_unicode(text), "w")

    # Construct the new list of links (objects)
    survived_links = memo.values()
    return survived_links

# Input is a list of tuples (URL, date) to news websites in
# string format
MIN_ARTICLE_COUNT = 10
def seek(news_site_list):
    results = []
    for website in news_site_list:
        articles = find_articles(website.domain)
        # Another quick optimization
        if len(articles) >= MIN_ARTICLE_COUNT:
            articles = memoize(articles, website.domain) # Optional, but recomended
            results.extend(articles)
    return results

test_news_source = "http://www.cbsnews.com/"
if __name__ == "__main__":
    results = find_articles(test_news_source)
    results = memoize(results, urlparse(test_news_source).netloc)
    for link in results:
        print link.href
