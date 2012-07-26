all: Retrieval_all Search_all

retrieve_all: crawl_all download_all

start_scrapyd:
	cd src/Crawler/PodSearchBot && PYTHONPATH=:../../ scrapy server --logfile=scrapyd.log --pidfile=scrapyd.pid &
stop_scrapyd:
	kill `cat src/Crawler/PodSearchBot/scrapyd.pid`

crawl_all: Scrapy_Podfeed_net Scrapy_Podster_de

crawl_digitalpodcast_com:
	curl http://localhost:6800/schedule.json -d project=default -d spider=Digitalpodcast_com
crawl_fluctu8_com:
	curl http://localhost:6800/schedule.json -d project=default -d spider=Fluctu8_com
crawl_podcast_at:
	curl http://localhost:6800/schedule.json -d project=default -d spider=Podcast_at
crawl_podcast_feedarea_de:
	curl http://localhost:6800/schedule.json -d project=default -d spider=Podcast_feedarea_de
crawl_podster_de:
	curl http://localhost:6800/schedule.json -d project=default -d spider=Podster_de
crawl_podfeed_net:
	curl http://localhost:6800/schedule.json -d project=default -d spider=Podfeed_net

download_all: FeedDownloader ImageDownloader
FeedsDownloaderRunner:
	export PYTHONPATH=$$PYTHONPATH:`pwd`/src/Retrieval/Crawler:`pwd`/src/Retrieval/LibGatherer:`pwd`/src/Retrieval/Downloader && cd src/Retrieval/Downloader/Feeds/ && python FeedsDownloaderRunner.py
ImageDownloader:
	export PYTHONPATH=$$PYTHONPATH:`pwd`/src/Retrieval/Crawler && cd src/Retrieval/Downloader && python ImageDownloader.py

search_all: Search_Solr_Start Search_Indexer

start_solr:
	cd lib/apache-solr-3.6.0/example && java -jar start.jar
empty_solr:
	cd lib/apache-solr-3.6.0/example/exampledocs && java -Ddata=args -jar post.jar "<delete><query>*:*</query></delete>"
index_all:
	export PYTHONPATH=$$PYTHONPATH:`pwd`/src/Search/Indexer2 && cd src/Search/Indexer2 && python SolrClient.py

