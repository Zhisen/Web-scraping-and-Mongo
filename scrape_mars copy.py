from bs4 import BeautifulSoup as bs
import requests
import pandas as pd 
from splinter import Browser

scrape_dict = {}


def get_hemisphere(browser, url):
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    img_url = soup.find('div', class_='downloads').img['src']
    title = soup.find('title').text.split(" ")
    title = title[0] + ' ' + title[1]
    d = ({'title':title,'img_url': img_url}) 
    return d

def scrape(url1, url2, url3, url4, urla, urlb, urlc, urld):
    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    browser.visit(url1)
    html = browser.html
    soup = bs(html, 'html.parser')
    title = soup.find('div', class_= "content_title").text
    paragraph = soup.find('div', class_="article_teaser_body").text
    news = {'title': title, 'paragraph': paragraph}
    scrape_dict['news'] = news

    browser.visit(url2)
    html = browser.html
    soup = bs(html, 'html.parser')
    featured_image_url = soup.find('figure', class_="lede").a['href']
    scrape_dict['featured_image_url']= featured_image_url

    browser.visit(url3)
    html = browser.html
    soup = bs(html, 'html.parser')
    weather_soup = bs(html, 'html.parser')
    weather = weather_soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    scrape_dict['weather'] = weather

    tables = pd.read_html(url4)
    df = tables[0]
    df.columns = ['Measurement', 'Values']
    df.set_index('Measurement', inplace=True)
    html_table = df.to_html()
    scrape_dict['facts'] = html_table



    dict1 = get_hemisphere(browser, urla)
    dict2 = get_hemisphere(browser,urlb)
    dict3 = get_hemisphere(browser,urlc)
    dict4 = get_hemisphere(browser,urld)
    hemisphere_image_urls = [dict1, dict2, dict3, dict4]
    scrape_dict['hemispheres'] = hemisphere_image_urls

    return scrape_dict


url1 = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
url2 = "https://www.jpl.nasa.gov/spaceimages/details.php?id=PIA16606"
url3 = 'https://twitter.com/marswxreport?lang=en'
url4 = "https://space-facts.com/mars/"
urla = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
urlb = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
urlc = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
urld = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'


scrape(url1, url2, url3, url4, urla, urlb, urlc, urld)



    