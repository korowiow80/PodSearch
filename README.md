PodSearch
=========

PodSearch is a search engine for Podcasts.

Dependencies
------------

-   [tldextract](https://github.com/john-kurkowski/tldextract) needs to be installed.
-   [Lucene](https://lucene.apache.org/core/) is expected to reside in `lib/lucene-3.6.0/`.
-   [Python](http://www.python.org/) needs to be installed.
-   [Scrapy](http://scrapy.org/) needs to be installed.
-   [PyTZ](http://pypi.python.org/pypi/pytz/) needs to be installed.

-   The working copy needs to be placed on a filesystem that supports names with newlines.
    NTFS will work, FAT32 will not work.

Installing Dependencies on Fedora Linux
---------------------------------------

These additional requirements for scrapy need to be installed first:
    
    sudo yum install python-devel libxml2-devel libxlst-devel

    sudo yum install python python-pip
    sudo pip-python install --upgrade feedparser scrapy tldextract pytz

Installing dependcies
---------------------

feedparser, chardet, httplib2
    
    sudo yum install python3-chardet python3-feedparser python3-httplib2

beautifulsoup

    wget http://www.crummy.com/software/BeautifulSoup/bs4/download/4.1/beautifulsoup4-4.1.1.tar.gz
    tar -xvf beautifulsoup4-4.1.1.tar.gz 
    cd beautifulsoup4-4.1.1
    sudo python3.2 setup.py install

python3-lxml

    sudo yum install python3-lxml

python-magic
 
    wget http://pypi.python.org/packages/source/p/python-magic/python-magic-0.4.2.tar.gz#md5=7266bf9d79ba2dc8ecc85764aeb45afd
    tar -xvf python-magic-0.4.2.tar.gz
    cd python-magic-0.4.2
    sudo python3.2 setup.py install

tldextract

    wget http://pypi.python.org/packages/source/t/tldextract/tldextract-1.1.tar.gz#md5=f317536f8924beb5cb0d0b0fe02e144b
    tar -xvf tldextract-1.1.tar.gz
    cd tldextract-1.1
    2to3 -w .
    sudo python3.2 setup.py install

scrapy

    wget 
         
Installing Dependencies on Ubuntu Linux
---------------------------------------

    sudo apt-get install python-setuptools
    sudo easy_install --upgrade feedparser scrapy tldextract pytz

Note: Tested with 10.10, so this information might be out of date.

Downloading
-----------

    git clone git@github.com:bigben87/PodSearch.git

Downloading the Content
----------------------

    git submodule update --init


Downloading Dependencies For The Presentations
----------------------------------------------

    git submodule update --init --recursive

Installing
----------

   cd PodSearch/web
   
   sudo ln -s `pwd` /var/www/lighttpd/PodSearch

To verify open [/Podsearch](http://localhost/Podsearch) in a browser.

Running The Presentations
-------------------------

    cd doc/1-Proposal/ && google-chrome *.html &
    cd doc/2-Concept/ && google-chrome *.html &
    cd doc/3-Prototype/ && google-chrome *.html &
    cd doc/4-Final_Report/ && google-chrome *.html &

Running all other Components
----------------------------

See

    make `tab``tab`
    
Conventions
-----------

-   We list all made conventions here.
-   We develop in English.
-   We use Eclipse as our integrated development enviroment.
-   We use Git as version control system.
-   We use GitHub for source code hosting and issue tracking.
-   We use deck.js and deck.js-transition-cube for or presentations.
-   We license everthing in this repository as three-clause BSD.
-   We use Scrapy for crawling.
-   We use Lucene for as our search engine.
-   We use GitHub issues to document allmost all our communication.
