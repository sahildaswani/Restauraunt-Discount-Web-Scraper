from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome("/Users/sahildaswani/Downloads/chromedriver")

categories = [
  {"key": 39, "value": "Fast Food"},
  {"key": 1, "value": "Hong Kong Style"},
  {"key": 2, "value": "Chinese"},
  {"key": 3, "value": "Cantonese"},
  {"key": 4, "value": "Taiwanese"},
  {"key": 5, "value": "Japanese"},
  {"key": 7, "value": "Thai"},
  {"key": 8, "value": "Asian"},
  {"key": 9, "value": "Italian"},
  {"key": 11, "value": "Western"},
  {"key": 14, "value": "Multinational"},
  {"key": 37, "value": "Others"}
]
Category = []
Name = []
Image = []
Website = []
Offer = []
Details = []
Districts = []
for c in categories:
  url = "http://www.diningdiscount.hk/en/search/restaurant?search_wrapper%5Bsearch_cusinie_wrapper%5D%5Bsearch_cusinie%5D=" + str(c["key"]) + "&search_wrapper%5Bsearch_district_wrapper%5D%5Bsearch_district%5D=0&action_wrapper%5Bsearch_key_wrapper%5D%5Bsearch_key%5D="
  driver.get(url)
  content = driver.page_source
  soup = BeautifulSoup(content, 'html.parser')
  search_items = soup.findAll('div', attrs={'class':'search-item'})
  links = []
  for i in search_items:
    links.append(i.find("a")["href"])

  for i in links:
    driver.get(i)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    name = soup.find("div", attrs={'class':'name'}).text
    image = soup.find("div", attrs={'class':'logo'}).find("img", recursive=False)["src"]
    website = i
    details = soup.find("div", attrs={'class':'tnc_wrapper'}).findAll("p", recursive=False)
    for d in range(len(details)):
      details[d] = details[d].text
      details[d] = details[d].replace(u'\xa0', u' ')
    details = '\n'.join(details)

    offer = soup.find("div", attrs={'class':'offers_wrapper'}).findAll("p", recursive=False)
    for d in range(len(offer)):
      offer[d] = offer[d].text
    offer = '\n'.join(offer)
    
    district = soup.findAll("div", attrs={'class': 'district-item'})
    for d in range(len(district)):
      district[d] = district[d].find('div', attrs={'class': 'name'}).text
    
    Category.append(c["value"])
    Name.append(name)
    Image.append(image)
    Website.append(website)
    Offer.append(offer)
    Details.append(details)
    Districts.append(district)

df = pd.DataFrame({'Category': Category,'Name': Name,'Image':Image,'Website':Website, 'Offer':Offer, 'Details':Details, 'Districts': Districts}) 
df.to_csv('restaurants.csv', index=False, encoding='utf-8')