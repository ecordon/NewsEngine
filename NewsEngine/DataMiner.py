# base class for all the extraction methods
import re

_author__ = "Lucas Ou-Yang, Evan O'Keeffe"
__date__ = "April 6th, 2013"
__version__ = "0.0.1"

class DataMiner:
    def __init__(self, html):
        self.html = html

    def getTitle(self):
        title = '"'
        if re.search(r'<title(.*)/title>', self.html):
            title = re.search(r'<title(.*)/title>', self.html).group(0)

        else:
            for i in range(1, 5):
                header = r'<h%d(.*)/h%d>'%(i, i)
                if re.search(header, self.html):
                    title = re.search(header, self.html).group(0)
                    break

        title = re.compile(r'<[^<]*?/?>').sub('"', title)
        title = title.replace('"','')
        return title
