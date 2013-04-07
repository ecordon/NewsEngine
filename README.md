
# NewsEngine -- Webcrawling Engine tailored towards news topics
Created for our news aggregator startup Wintria: http://wintria.com Please Visit :)
        -- By Lucas Ou-Yang and Evan O'Keeffe, UCI Students. April 6th, 2013.

NewsEngine uses BeautifulSoup for html extraction and parsing.
We also use nltk and feedparser for html cleaning and rss extaction respectively.

Example Usage:

--Your data will be written to a txt file named Saved_Articles.txt
--Articles are delimited by u'$$', Article properties are delimited by u';;'

from NewsEngine.NewsEngine import extract_news

topics = ["kate middleton", "bmw cars"]

article_links = extract_news(topics, True)
for article in article_links:
    print article.href

Read the source code for more details on what you can do, i'll update the README later.

