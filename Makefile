all: Retrieval_all Search_all


Retrieval_all: Scrapy_all Downloader_all

Scrapy_all: Scrapy_Podfeed_net Scrapy_Podster_de
Scrapy_Podfeed_net:
	cd src/Retrieval/Crawler && scrapy crawl Podfeed_net
Scrapy_Podster_de:
	cd src/Retrieval/Crawler && scrapy crawl Podster_de

Downloader_all: FeedDownloader ImageDownloader
FeedsDownloaderRunner:
	export PYTHONPATH=$$PYTHONPATH:`pwd`/src/Retrieval/Crawler:`pwd`/src/Retrieval/LibGatherer:`pwd`/src/Retrieval/Downloader && cd src/Retrieval/Downloader/Feeds/ && python FeedsDownloaderRunner.py
ImageDownloader:
	export PYTHONPATH=$$PYTHONPATH:`pwd`/src/Retrieval/Crawler && cd src/Retrieval/Downloader && python ImageDownloader.py


Search_all: Search_Indexer
Search_Indexer:
	echo "Implement me!"
