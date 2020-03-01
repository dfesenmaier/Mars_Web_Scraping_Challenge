from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from pprint import pprint
import urllib
import time
import requests


def read_scrape():
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)
    
    # Declare the database
    db = client.mars_db

    # Declare the collection
    collection = db.mars_data

    return db.mars_data.find({})
    

def save_scrape(scrape):
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)
    
    # Declare the database
    db = client.mars_db
    
    # Declare the collection
    collection = db.mars_data

    # Drop collection if exists
    if collection.count() > 0:
        collection.drop()

    collection.insert_one(scrape)

def scrape():
    NEWS_URL = "https://mars.nasa.gov/news/"
    IMAGE_URL = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    WEATHER_URL = "https://twitter.com/marswxreport?lang=en"
    FACTS_URL = "http://space-facts.com/mars/"
    HEMISP_URL = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    driver = webdriver.Firefox()
    driver.get(NEWS_URL)
    html_news = driver.page_source

    driver.get(IMAGE_URL)
    html_image = driver.page_source

    driver.get(WEATHER_URL)
    time.sleep(3)
    html_weather = driver.page_source

    driver.get(FACTS_URL)
    html_hemispheres = driver.page_source

    driver.close()

    #Scrape Mars News
    soup = BeautifulSoup(html_news, "html.parser")
    news = soup.find("div", class_="list_text")

    news_dict = {
        
        "Date": news.contents[0].text,
        "Title": news.contents[1].text,
        "Body": news.contents[2].text
    }

    soup = BeautifulSoup(html_image, "html.parser")
    mars_image = soup.find_all("a", class_="fancybox")

    featured_image_url = urllib.parse.urljoin("https://www.jpl.nasa.gov", mars_image[1]["data-fancybox-href"])

    soup = BeautifulSoup(html_weather, "html.parser")
    mars_weather = soup.find("div", class_="css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")

    request = requests.get(FACTS_URL)
    mars_facts_soup = BeautifulSoup(request.text, "html.parser")

    facts = f'{mars_facts_soup.find("table", class_="tablepress tablepress-id-p-mars")}'

    driver = webdriver.Firefox()
    driver.get(HEMISP_URL)
    driver.implicitly_wait(10)


    hem_list = []

    links = driver.find_elements_by_class_name("thumb")

    for l in range(len(links)):
        driver.find_elements_by_class_name("thumb")[l].click()

        title = driver.find_element_by_class_name("title")
        image_url = driver.find_element_by_link_text("Sample")

        hem_list.append({
            
            "title": title.text, 
            "img_url": image_url.get_attribute("href")
        })
        driver.back()

    driver.close()

    scrape_dict = {
        
        "News": news_dict,
        "Image":featured_image_url,
        "Tweet":mars_weather.text,
        "Facts": facts,
        "Hemisphere":hem_list
    }

    pprint(scrape_dict)