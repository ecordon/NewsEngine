"""
    This module is one level up from seeker (A module which
    extracts "valid news" <a> links from a given HTML page.
    It uses the Google REST API to crawl relevant news
    articles based on previous searches in Wintria's
    history. It also queries general news articles.

    The goal is to implement niche detection in this module.

    Browser API Key:    Your key here

    Google Custom Search:
    =================================================
    Name:               Ex. Wintria News
    Unique ID/Key:      Your id here

"""
_author__ = "Lucas Ou-Yang, Evan O'Keeffe"
__date__ = "April 6th, 2013"
__version__ = "0.0.1"

import urllib2
import json
from NewsWebsite import NewsWebsite
from EngineConstants import POSITIVES, NEGATIVES
import google as g

GOOGLE_API_KEY = "Your Key Here"
GOOGLE_CUSTOM_ID = "Your ID Here"

# This method is guaranteed to work because we are using Google's official search API
# However, it's very limited and weak. We will alongside this use a much more
# powerful 3rd party API.
# Currently we are extracting 10 articles per topic as default (topic depth)
def safe_retrieve_urls(topic, topic_depth = 10):
    # It is possible to navigate the pages in a google
    # results page via the "start" parameter. No parameter
    # indicates starting at result 1, &start=11 indicates
    # starting at result 11, aka page 2, and so on.

    # Here is a url link for more params:
    # https://developers.google.com/custom-search/v1/using_rest#query-params

    if "news" != topic[-4:]: # If the last four chars don't equal news
        topic = topic + " news"
    query = topic.replace(" ", "%20") # Encode the spaces for a url

    all_results = []
    # To choose which page to land on, use &start= (default 1)
    # Number of elements on page = &num= (default 10) (Page 2 start at 11 for example)
    iteration = 0
    while iteration < (topic_depth / 10):
        page = str((iteration * 10) + 1)

        target_url = \
            "https://www.googleapis.com/customsearch/v1?" \
            "key=%s&cx=%s&q=%s&start=%s" %(GOOGLE_API_KEY, GOOGLE_CUSTOM_ID, query, page)

        opener = urllib2.build_opener()
        try: response = opener.open(target_url)
        except Exception: # Google only allows 100 queries a day
            print "We have reached google's daily query limit"
            return []

        # This is an insane comprehensive list haha
        results = [
            [0, NewsWebsite(
                result["link"],
                result["title"],
                result["snippet"]
            )]
            for result in json.load(response)["items"]
        ]

        for index, result in enumerate(results):
            # A NewsWebsite object
            site = result[1]
            # We don't need a special case for either, negatives
            # have negative point values
            for term, score in POSITIVES + NEGATIVES:
                # If any positive term is present, increase
                # the point value of the result
                if term in site.raw_link or term \
                    in site.title or term in site.summary:
                    results[index][0] += score

        all_results += results
        iteration += 1

    # Remove news with a low score
    new_results = []
    for score_obj in all_results:
        if score_obj[0] >= 10:
            new_results.append(score_obj[1])

    #for r in new_results:
    #    print r.domain
    return new_results

def dangerous_retrieve_urls(topic, num = 10, saftey = 5.0):
    '''
    Add a exception check that if this method returns
    a list of size zero, google has ip blocked us and we
        can use our backup crawler, (via google's official api)
    '''
    top_news, niche_news = [], []
    query = ""
    if "news" != topic[-4:]: # If the last four chars don't equal news
        query = str(topic) + " news"

    try:
        for top in g.search(query, tld='com', lang='en',
                            num=num, start=0, stop=num, pause=saftey):
            if is_news_link(top):
                # Note that we are appending tuples of the date
                # and the news link, not just the link
                top_news.append(NewsWebsite(raw_link=top))
        for niche in g.search(query, tld='com', lang='en',
                              num=num, start=300, stop=300+num, pause=saftey):
            if is_news_link(niche):
                niche_news.append(NewsWebsite(raw_link=niche))
    except Exception:
        print "Google has blocked us"
        return None

    return top_news + niche_news

def is_news_link(link):
    for kill, score in NEGATIVES:
        if kill in link:
            return False
    return True

def navigate(list_of_terms, dangerous=False, safe=True):
    news_sites = []
    for term in list_of_terms:
        if safe:
            news_sites.extend(safe_retrieve_urls(term))
        if dangerous:
            news_sites.extend(dangerous_retrieve_urls(term))
    uniquify = { news.domain:news for news in news_sites }
    return uniquify.values()

if __name__ == '__main__':
    sites = navigate(["bmw cars", "girls", "technology"])
    for site in sites:
        print site.raw_link, site.domain
