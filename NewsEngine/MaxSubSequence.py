import re, os
import urllib2
from nltk import clean_html
from BeautifulSoup import BeautifulSoup

from Link import Link
from EasyUnicode import *
from DataMiner import DataMiner

# Maximum Subsequence Segmentation
_author__ = "Lucas Ou-Yang, Evan O'Keeffe"
__date__ = "April 6th, 2013"
__version__ = "0.0.1"
# Algorithm by Jeff Pasternack and Dan Roth University of Illinois
# First step remove any <Table> or <IFrame> tags
# Second remove remove any Div tags that contain (<A>),
# <IFRAME>, <TABLE>,<IMG>,<EMBED>,<APPLET> or <OBJECT>

class MaxSubSequence(DataMiner):
    '''
	#Algorithm by Jeff Pasternack and Dan Roth University of Illinois
	#################################################################
	#First step remove any <Table> or <IFrame> tags
	#Second remove remove any Div tags that contain (<A>),
	#<IFRAME>, <TABLE>,<IMG>,<EMBED>,<APPLET> or <OBJECT>
	#################################################################
	'''

    def MaxSubSequence(self, word_cap=1000):
        '''
			First
			Remove the table and iframe from html entirely with their contents
			We assume they hold no information here
			Second
			Now to actively scan through the div tags that contain 
			<A>,<IFRAME>,<TABLE>,<IMG>,<EMBED>,<APPLET>,<OBJECT> tags
			and remove the div from the equation
		'''
        try:
            soup = BeautifulSoup(self.html)
        except Exception:
            return None  # Beautiful Soup unicode error we need to account for
        #remove the table and iframe
        if re.search("<iframe", self.html):
            tag = soup.iframe
            if tag is not None:
                tag.clear()

        if re.search("<table", self.html):
            tag = soup.table
            if tag is not None:
                tag.clear()

        #get all the div tags
        div_tags = [x.extract() for x in soup.findAll('div')]
        #getDivs(div_tags)
        return ' '.join(self.extract(div_tags).split(' ')[:word_cap])

    def extract(self, div_tags):
        #Tags and their names
        tagnames = ["a", "script", "iframe", "img", "embed", "applet", "object"]
        tags = ["<a", "<script", "<iframe", "<img", "<embed", "<applet", "<object", "<li"]

        cleaned = []
        output = ""
        unwanted = False

        for div in div_tags:
            string = str(div)
            for tag in tags:
                if re.search(tag, string):
                    end_tag = tag[1:] + ">"
                    regex = tag + '(.*)/' + end_tag
                    string = re.sub(regex, "", string)
            clean = clean_html(string)
            if (clean != ""): cleaned.append(clean)

        for i in range(0, len(cleaned)):
            cleaned[i] = re.sub("\s\s", " ", cleaned[i])


        maxx = 0
        for txt in cleaned:
            if len(txt) >= maxx:
                maxx = len(txt)
                output = txt

        return output

    def getDivs(self, divs):
        output = ""
        for div in divs:
            output += "\n----------------------------\n"
            output += str(div)
        return output

SAVED_DIRECTORY = "Saved_Articles.txt"
PROPERTY_DELIMITER = u";;"
ARTICLE_DELIMITER = u"$$"
from Seeker import MEMO_DIRECTORY
def extract_data(link, get_objects):
    # If we are in the memo directory, get out of it
    directories = os.getcwd().split('/')
    if directories[-1] == MEMO_DIRECTORY:
        os.chdir('..')

    try:
        html = urllib2.urlopen(link.href).read()
    except Exception:
        return # Bust link, keep going

    obj = MaxSubSequence(html)
    txt, title = obj.MaxSubSequence(), ""
    if txt is None:
        return # Beautiful Soup unicode error we need to account for
    title = obj.getTitle()
    if link.title is None: # If the title was not captured in the seeker, try once more
        link.title = title

    # Create txt file with link, title, date, body, all in UNICODE
    total = PROPERTY_DELIMITER.join([link.href,
                        safe_unicode(title), safe_unicode(txt)]) + ARTICLE_DELIMITER
    write_unicode_to_file(SAVED_DIRECTORY, total, "a+")
    if get_objects:
        link.text = txt
        return link

if __name__ == '__main__':
    link = raw_input("Enter website to extract from\n:")
    link_obj = Link(href=link, website=link)
    extract_data(link_obj, True)


