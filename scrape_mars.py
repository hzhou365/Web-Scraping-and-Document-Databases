
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup
import pymongo
import requests
import pandas as pd
import time
from datetime import datetime


# In[2]:


def init_browser():
    chrome_location = "C:\\Users\\HZhou\\Documents\\BOOTCAMP2018\\HW12-Web-Scraping-and-Document-Databases\\chromedriver.exe"
    chrome_location = chrome_location.replace("\\","/")
    executable_path = {"executable_path":chrome_location}
    
    return Browser("chrome", **executable_path, headless=False)


# In[3]:


def get_soup_object(url):
    browser = init_browser()
    browser.visit(url)
    soup = BeautifulSoup(browser.html,"html.parser")
    return soup


# In[4]:


def get_latest_NASA_news():
    NASA_MARS_url = "https://mars.nasa.gov/news/"
    news_soup = get_soup_object(NASA_MARS_url)
    latest_news = news_soup.find_all("div",{"class":"list_text"})[0]
    return {
        "title":latest_news.find("div",{"class":"content_title"}).text,
        "content":latest_news.find("div",{"class":"article_teaser_body"}).text
    }


# In[5]:


def get_MARS_img():
    JPL_home_url = "https://www.jpl.nasa.gov"
    JPL_img_url = JPL_home_url+"/spaceimages/?search=&category=Mars"
    jpl_soup = get_soup_object(JPL_img_url)
    items = jpl_soup.find("div",{"class":"carousel_items"})
    img_title = items.find("h1",{"class":"media_feature_title"}).text
    featured_img = items.find("article")
    img_url = JPL_home_url+featured_img['style'].split(':')[1].split('\'')[1]
    return {
            "title":img_title,
            "img_url":img_url
           }


# In[6]:


def get_MARS_temperature():
    twitter_report_url = "https://twitter.com/marswxreport?lang=en"
    temp_soup = get_soup_object(twitter_report_url)
    return temp_soup.find("ol",{"id":"stream-items-id"}).find("li").find("p").text


# In[7]:


def get_MARS_facts():
    df = pd.read_html("https://space-facts.com/mars/")[0]
    df = df.rename(columns={0:"Description",1:"Value"})
    df = df.set_index("Description")
    return df.to_dict()['Value']


# In[8]:


def scrape():
    mars_news = get_latest_NASA_news()
    mars_img = get_MARS_img()
    mars_facts = get_MARS_facts()
    mars_temp = get_MARS_temperature()
    return {
        "date":datetime.now(),
        "news":mars_news,
        "featured_img":mars_img,
        "facts":mars_facts,
        "temperature":mars_temp,
    }



