from distutils.core import setup

setup(
    name='NewsEngine',
    version='0.0.1',
    packages=['NewsEngine'],
    install_requires=['BeautifulSoup>=3.2.1', 'nltk>=2.0.4'],
    url='http://wintria.com',
    license='',
    author='Lucas Ou-Yang, Evan O\'Keeffe',
    author_email = 'lucasyangpersonal@gmail.com, evanokeeffe@gmail.com',
               description = 'Text extraction module tailored for gathering news.'
)
