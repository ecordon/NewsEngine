from Navigator import Navigator
import Seeker
import MaxSubSequence
import TrendingExtract

_author__ = "Lucas Ou-Yang, Evan O'Keeffe"
__date__ = "April 6th, 2013"
__version__ = "0.0.1"
# This method creates a blob file
# of the extracted news websites
def extract_news(trending_terms, get_objects=False, dangerous=False, safe=True):
    # Returns a list of NewsWebsite Objects
    websites = Navigator.navigate(trending_terms, dangerous, safe)
    # Returns a list of Link Objects
    articles = Seeker.seek(websites)
    links = []
    # Writes to file, to be FTP'ed, additionally returns as Link objects if specified
    if get_objects:
        for article in articles:
            link = MaxSubSequence.extract_data(article, get_objects)
            if link: links.append(link)
        return links
    else:
        for article in articles:
            MaxSubSequence.extract_data(article, get_objects)

if __name__ == '__main__':
    #extract_news(["bmw cars", "surfing", "programming", "tom cruise"])
    trending = TrendingExtract.extract_trending()
    extract_news(trending)




