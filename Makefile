ake all: Retrieval_all Search_all


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


Search_all: Search_Solr_Start Search_Indexer
Search_Solr_Start:
	cd lib/apache-solr-3.6.0/example && java -jar start.jar
Search_Solr_Empty:
	cd lib/apache-solr-3.6.0/example/exampledocs && java -Ddata=args -jar post.jar "<delete><query>*:*</query></delete>"
Search_Indexer:
	export PYTHONPATH=$$PYTHONPATH:`pwd`/src/Search/Indexer2 && cd src/Search/Indexer2 && python SolrClient.py
