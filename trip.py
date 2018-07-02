# coding=utf-8

from bs4 import BeautifulSoup
import requests

url = 'https://www.tripadvisor.cn/Attractions-g60763-Activities-New_York_City_New_York.html#ATTRACTION_SORT_WRAPPER'

wb_data = requests.get(url)
soup = BeautifulSoup(wb_data.text, 'lxml')

titles = soup.select("#ATTR_ENTRY_ > div.attraction_clarity_cell > div > div > div.listing_info > div.listing_title > a")

for t in titles:
    print(t.get_text())



