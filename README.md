PodSearch
=========

PodSearch is a search engine for Podcasts.

Dependencies
------------

-   [tldextract](https://github.com/john-kurkowski/tldextract) needs to be installed.
-   [Lucene](https://lucene.apache.org/core/) is expected to reside in `lib/lucene-3.6.0/`.
-   [Python](http://www.python.org/) needs to be installed.
-   [Scrapy](http://scrapy.org/) needs to be installed.

-   The working copy needs to be placed on a filesystem that supports names with newlines.
    NTFS will work, FAT32 will not work.

Installing Dependencies on Fedora Linux
---------------------------------------

    yum install python python pip
    pip-python install tldextract scrapy

Installing Dependencies on Ubuntu Linux
---------------------------------------

    sudo apt-get install python-setuptools
    sudo easy_install tldextract
    sudo easy_install feedparser

Note: Tested with 10.10, so this information might be out of date.

Downloading
-----------

    git clone git@github.com:bigben87/PodSearch.git


Downloading Dependencies For The Presentations
----------------------------------------------

    git submodule update --init --recursive

Running The Presentations
-------------------------

    cd doc/1-Proposal/ && google-chrome *.html &
    cd doc/2-Concept/ && google-chrome *.html &
    cd doc/3-Prototype/ && google-chrome *.html &
    cd doc/4-Final_Report/ && google-chrome *.html &
    
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
