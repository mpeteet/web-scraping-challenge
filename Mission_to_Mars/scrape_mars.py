# Import dependencies
import pandas as pd
import requests
import datetime as dt

# Import beautiful soup and splinter dependencies
!pip install splinter
from bs4 import BeautifulSoup
from splinter import Browser

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return browser = Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dictionary = {}

    ### NASA Mars News
    
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(news_url)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')
    news_title = slide_elem.find('div', class_='content_title').get_text()
    slide_elem2 = news_soup.select_one('div.list_text')
    news_p = news_soup.find('div', class_='article_teaser_body').get_text()

    ### JPL Mars Space Images - Featured Image 
    
    mars_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(mars_url)
    mars_html = browser.html
    images_soup = BeautifulSoup(mars_html, 'html.parser')
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    images_overlay = BeautifulSoup(browser.html, 'html.parser')
    img_url_rel = images_overlay.find('img', class_='fancybox-image').get('src')
    featured_image_url = f'https://spaceimages-mars.com/{img_url_rel}'

    ### Mars Facts, scrape and convert to HTML
    facts_url = 'https://space-facts.com/mars/
    mars_facts = pd.read_html(facts_url)
    mars_dataframe = mars_facts[0]
    mars_dataframe = mars_dataframe.rename(columns={0: 'Attribute', 1 : 'Value'}).set_index(['Attribute'])
    mars_html = mars_dataframe.to_html()
  
    ### Mars Hemispheres
    # Visit USGS Astrogeology site obtain high resolution images for each hemispheres
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    hemisphere_main_url = 'https://astrogeology.usgs.gov'
    html_hemispheres = browser.html
    hemispheres_soup = BeautifulSoup(html_hemispheres, 'html.parser')
    hemisphere_items = hemispheres_soup.find_all('div', class_='item')
    hemisphere_image_urls = []
    # Loop through the urls
    for i in hemisphere_items:
        # store the titles
        hemisphere = i.find('div', class_='description')
        hemi_title = hemisphere.h3.text
        # store the links to the images -- browse the page
        hemi_image_url = hemisphere.a['href']
        browser.visit(hemisphere_main_url + hemi_image_url)
        image_html = browser.html
        hemispheres_soup = BeautifulSoup(image_html, 'html.parser')
        full_image_link = hemispheres_soup.find('div', class_='downloads')
        full_image_url = full_image_link.find('li').a['href']
        # Append this information to the url dictionary
        hemi_image_dict = {}
        hemi_image_dict['title'] = hemi_title
        hemi_image_dict['img_url'] = full_image_url
        hemisphere_image_urls.append(hemi_image_dict)
   
    ### Scraping dictionary
    mars_dictionary = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "featured_image_url": featured_image_url(browser),
        "facts": str(mars_html),
        "hemispheres": hemisphere_image_urls,
        "last_modified": dt.datetime.now()
    }
    
    # Close the browser
    browser.quit()

    # Return the results
    return mars_dictionary
