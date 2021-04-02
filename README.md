# web-scraping-challenge

I built a web application that scrapes various websites for data releated to the Mission to Mars and displays the information in a single HTML page.

BeautifulSoup, Pandas and Splinter requests were used for the scraping and analysis tasks.

The Nasa Mars News Site was scraped to collect the latest News Title and Paragraph Text. 

I used splinter to navigate the JPL Featured Space Image site to find the url of the Featured Mars Image.

The Mars Facts webpage was visited an Pandas was used to scrape the table containing the planet's facts. This data was convered into an HTML table. 

The USGS Astrogeology site was visited and I obtained high resolution images for each of Mar's hemispheres.  The URL for each images was obtianed and stored in a Python dictionary. 

I built a MongDB and Flask Application and created an HTML page that displays all of the information scraped above. 

