all: Retrieval_all Search_all

retrieve_all: start_crawl_all download_all

start_scrapyd:
	cd src/Crawler/PodSearchBot && PYTHONPATH=:../../ scrapy server --pidfile=scrapyd.pid &
stop_scrapyd:
	kill `cat src/Crawler/PodSearchBot/scrapyd.pid`

start_crawl_all: start_crawl_digitalpodcast_com start_crawl_fluctu8_com start_crawl_podcast_at start_crawl_feedarea_de start_crawl_podster_de start_crawl_podfeed_net

start_crawl_digitalpodcast_com:
	curl http://localhost:6800/schedule.json -d project=default -d spider=Digitalpodcast_com
start_crawl_fluctu8_com:
	curl http://localhost:6800/schedule.json -d project=default -d spider=Fluctu8_com
start_crawl_podcast_at:
	curl http://localhost:6800/schedule.json -d project=default -d spider=Podcast_at
start_crawl_feedarea_de:
	curl http://localhost:6800/schedule.json -d project=default -d spider=Feedarea_de
start_crawl_podster_de:
	curl http://localhost:6800/schedule.json -d project=default -d spider=Podster_de
start_crawl_podfeed_net:
	curl http://localhost:6800/schedule.json -d project=default -d spider=Podfeed_net

stop_crawl_all: stop_crawl_digitalpodcast_com stop_crawl_fluctu8_com stop_crawl_podcast_at stop_crawl_feedarea_de stop_crawl_podster_de stop_crawl_podfeed_net

stop_crawl_digitalpodcast_com:
	curl http://localhost:6800/cancel.json -d project=default -d spider=Digitalpodcast_com
stop_crawl_fluctu8_com:
	curl http://localhost:6800/cancel.json -d project=default -d spider=Fluctu8_com
stop_crawl_podcast_at:
	curl http://localhost:6800/cancel.json -d project=default -d spider=Podcast_at
stop_crawl_feedarea_de:
	curl http://localhost:6800/cancel.json -d project=default -d spider=Feedarea_de
stop_crawl_podster_de:
	curl http://localhost:6800/cancel.json -d project=default -d spider=Podster_de
stop_crawl_podfeed_net:
	curl http://localhost:6800/cancel.json -d project=default -d spider=Podfeed_net

download_all: FeedDownloader ImageDownloader
FeedsDownloaderRunner:
	export PYTHONPATH=$$PYTHONPATH:`pwd`/src/Retrieval/Crawler:`pwd`/src/Retrieval/LibGatherer:`pwd`/src/Retrieval/Downloader && cd src/Retrieval/Downloader/Feeds/ && python FeedsDownloaderRunner.py
ImagesDownloader:
	# export PYTHONPATH=$$PYTHONPATH:`pwd`/src/:`pwd`/src/ImagesDownloader/:/usr/lib64/python2.7/site-packages/ && cd src/ImagesDownloader/ && pypy ImagesDownloader.py
	# pypy wont find feedparser, so:
	export PYTHONPATH=$$PYTHONPATH:`pwd`/src/:`pwd`/src/ImagesDownloader/ && cd src/ImagesDownloader/ && python ImagesDownloader.py
    	
search_all: Search_Solr_Start Search_Indexer

start_solr:
	cd lib/apache-solr-3.6.0/example && java -jar start.jar
empty_solr:
	cd lib/apache-solr-3.6.0/example/exampledocs && java -Ddata=args -jar post.jar "<delete><query>*:*</query></delete>"
index_all:
	#export PYTHONPATH=$$PYTHONPATH:`pwd`/src:`pwd`/src/Indexer:/usr/lib64/python2.7/site-packages/ && cd src/Indexer/ && pypy SolrClient.py
	# pypy wont find sunburnt, so
	export PYTHONPATH=$$PYTHONPATH:`pwd`/src:`pwd`/src/Indexer && cd src/Indexer/ && python SolrClient.py
