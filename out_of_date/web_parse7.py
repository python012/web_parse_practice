# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import pymongo
from string import whitespace

client = pymongo.MongoClient('localhost', 27017)
phone_number_sale = client['phone_number_sale']
page_url_tab = phone_number_sale['page_url_tab']

urls = ["http://bj.58.com/shoujihao/pn{}/".format(str(i)) for i in range(2, 200, 1)]
urls.insert(0, "http://bj.58.com/shoujihao/")

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) ' +
                  'Chrome/54.0.2840.87 Safari/537.3',
}


def get_title_and_links(page_url):
    page_data = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(page_data.text, 'lxml')

    amount = soup.select("#infocont > span > b")[0].get_text()
    if '0' == amount:
        return False
    else:
        titles = soup.select('#infolist div.boxlist div.boxlist ul li a.t strong.number')
        grid_urls = soup.select('#infolist div.boxlist div.boxlist ul li a.t')
        for title, gird_url in zip(titles, grid_urls):
            if gird_url.get("href").startswith('http://jump.zhineng.'):
                continue
            data = {
                'Title': title.get_text(),
                'Grid URL': gird_url.get("href"),
            }
            page_url_tab.insert_one(data)
        return True


def check_each_grid(grid_url):
    page_data = requests.get(grid_url, headers=headers)
    soup = BeautifulSoup(page_data.text, 'lxml')

    page_title = soup.select('div.col_sub.mainTitle > h1')[0].get_text()
    price = soup.select('ul.suUl span.price.c_f50')[0].get_text()
    seller = soup.select('ul.vcard > li > a')[0].get_text()

    data = {
        'Page title': page_title.translate(dict.fromkeys(map(ord, whitespace))),
        'Price': price.translate(dict.fromkeys(map(ord, whitespace))),
        'Seller': seller.translate(dict.fromkeys(map(ord, whitespace)))
    }
    return data


def feed_the_database():
    for page in page_url_tab.find():
        data = check_each_grid(page['Grid URL'])
        for field in data:
            page_url_tab.update_one({'_id': page['_id']}, {'$set': {field: data[field]}})


if __name__ == '__main__':
    counter = 1
    for url in urls:
        if not get_title_and_links(url):
            break
        else:
            print(counter)
            counter += 1

    feed_the_database()
