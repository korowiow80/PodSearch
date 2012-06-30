import urllib2

updateURL = "http://localhost:8983/solr/update"

solrReq = urllib2.Request(updateURL, '<commit waitFlush="false" waitSearcher="false"/>')
solrReq.add_header("Content-Type", "text/xml")
solrPoster = urllib2.urlopen(solrReq)
response = solrPoster.read()
solrPoster.close()