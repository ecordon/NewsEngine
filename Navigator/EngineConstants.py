_author__ = "Lucas Ou-Yang, Evan O'Keeffe"
__date__ = "April 6th, 2013"
__version__ = "0.0.1"


# If we see that a query result has these terms
# in the description, domain, url, etc, we punish them,
# as it's not news, or news we want.
# Terms and their respective weights. News pages which have many positives
# words are probably actually news sites, and vice versa
POSITIVES = [
    ("news", 10),
    ("new", 5),
    ("breaking", 3),
    ("headline", 5),
    ("trending", 3),
    ("global", 2),
    ("blog", 3),
    ("forum", 2)
]

NEGATIVES = [
    ("tube", -10),
    ("wiki", -20),
    ("gov", -5),
    ("encyclopedia", -5),
    ("free", -7),
    ("buy", -7),
    ("sell", -7),
    ("facebook", -3),
    ("myspace", -3),
    ("porn", -10)
]
