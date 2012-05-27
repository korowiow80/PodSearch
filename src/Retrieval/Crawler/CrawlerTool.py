

class CrawlerTool:
    def derive (self, url):
        domain = self.getDomain(url)
        spiderName = self.getSpiderNameFromUrl(domain)
        directoryPath = self.getDirectoryPath(domain)
        feedListFilePath = self.getFeedListPath(domain)
        self.ensurePathExists(directoryPath)        
        baseUrl = self.getBaseUrl(url)
        return baseUrl, feedListFilePath, spiderName, directoryPath
