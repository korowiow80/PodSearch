Concept - Challenges And Implementation Ideas 
----------------------------------------

1. Heterogenous Data

-   **Normalize data** by detecting and converting encodings
-   **Normalize data** by detecting and consolidating information from iTunes tags and other namespace extensions
-   **Normalize data** by translating iTunes 'Preview' (html) back to feeds (rss/atom)
-   **Normalize data** by parsing each feed into a document collection using Lucene
-   **Index unindexable data** by indexing audio files using their podcast feeds

2. Heterogenous Data Sources

-   **Bring podcasts together** by scraping podcast directories via webinterface/API/feed
-   **Open up another data source** by implementing adding/pinging podcasts via webinterace/API
-   **Consolidate data** and deduplicate Podcast entries from directories

3. Interactivity

-   **Give fast Feedback** by getting search results using AJAX
-   **Give fast Feedback** by searching on each keystroke
-   **Be interactive** and augment the search through drag and drop of result entries
-   **Give fast Feedback** and offer interface for adding/pinging feeds via Javascript

4. Consistency, Integrity

-   **Guarantee Consistency** by checking whether an actualized feed has less data then the one indexed last time
-   **Guarantee Integrity** by merging actualized feeds that contain the most-current episodes, only with older versions of them
-   **Guarantee Consitency** by hardening the scraping pipeline using tests
-   **Guarantee Integrity** by minimizing latencies through spliting the scraping pipeline into processes

5. Security

-   **Distrust user input** and check feeds for contained attacks before indexing
-   **Support paranoid** usage by offering a fallback to use the site without Javascript
-   **Establish confidentiality** by encrypting the data transfer on the search server
-   **Protect integrity** by separting the scraping-pipeline into multiple users
-   **Check authenticity** of the feeds by checking certificates on downloading
-   **Check authenticity** of the API clients using API keys associated with an email-address
-   **Establish non-deniability** by protocolling multiple stages of a ping/addition of a podcast
-   **Guarantee availability** by limiting the request fequency of the API to sane rates

6. Scalability

-   **Achieve scalability for much data** by using the mature search engine Lucene
-   **Improve scalability for many users** by using a lucene server to get search results in JSON through a Webservice (Solr, Webbit or similar)
-   **Improve scalability for many requests** by delivering static content using a special server (lighttpd?)
-   **Improve scalability for many requests** by enabling client-side caching of static content
-   **Improve scalability for many requests** by using an individual server for adding/pinging feeds
-   **Achieve scalability for frequent updates** through parallelization of the scraping pipeline
-   **Reduce load** on the servers by using Javascript for internationalization
-   **Improve scalability** by implementing the webinterface using static content (html, js, css, images), only

7. Openness

-   **Guarantee functionality** with exotic browsers (IE, Safari, Opera, mobile browsers)
-   **Guarantee layout** with exotic browsers (IE, Safari, Opera, mobile browsers)
-   **Guarantee functionality** with screenreaders
-   **Openness for world-wide usergroup** by Internationalization of the webinterface
-   **Openness for user input** on adding/pinging feeds via webinterface/API
-   **Be open for other applications** and offer a webinterface/feed/API for recently added episodes/feeds

8. Adaption (especially mobiles Web)

-   **Guarantee functionality** with low resolutions by adpting the layout dynamically using media-queries
-   **Adapt to users** by tracking their behaviour through cookies and modifying the search results accordingly

