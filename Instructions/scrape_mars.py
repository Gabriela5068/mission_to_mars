import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time


scraped_data = {}

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    # site 1 -
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    response = requests.get(news_url)

    soup = bs(response.text, 'html.parser')
    print(soup.prettify())

    # use bs to find() the example_title_div and filter on the class_='content_tile'
    news_title = soup.find('div', class_="content_title").get_text()
    print(news_title)
    scraped_data['news_title'] = news_title

    # use bs to find() the example_title_div and filter on the class_='article_teaser_body'
    news_p = soup.find('div', class_="rollover_description_inner").get_text()
    scraped_data['news_p'] = news_p
    print(news_p)

    #site 2

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    base_url = "https://www.jpl.nasa.gov"
    browser.visit(featured_image_url)
    #splinter used for navigating websites 
    browser.find_by_id('full_image').click()
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    #saving the website, beautiful soup captures website 
    html = browser.html
    soup = bs(html, 'html.parser')
    img_url = soup.find('img', class_="main_image")['src']
    scraped_data['featured_image_url'] = base_url + img_url
    scraped_data['featured_image_url']


    # site 3 

    tweet_url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(tweet_url)
    soup = bs(response.text, 'html.parser')
    weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text()
    print(weather)
    scraped_data['weather'] = weather
    browser.quit()


    # site 4 - 
    facts_url = 'https://space-facts.com/mars/'
    facts_df = pd.read_html(facts_url)[0]
    table = facts_df.to_html(classes=None, border=None, justify=None)
    scraped_data['table'] = table

    #site 5 
    # hemishpere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # response = requests.get(hemishpere_url)
    # soup = bs(response.text, 'html.parser')

    # hemisphere_images = []

    # browser.visit(hemishpere_url)

    # for i in range(4):
    #     hemisphere_pairs = {}
        
    #     browser.find_by_tag('h3')[i].click()
    #     html = browser.html
    #     soup = bs(html, 'html.parser')
    #     hemisphere_pairs['image'] = soup.find('div', class_='downloads').find('a')['href']
    #     time.sleep(2)
    #     hemisphere_pairs['title'] = soup.find('h2', class_='title').text
    #     hemisphere_images.append(hemisphere_pairs)
    #     time.sleep(2)
    #     browser.back()

    return scraped_data  