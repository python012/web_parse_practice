from bs4 import BeautifulSoup
import requests
import time
import os
import urllib
import random

single_url = "http://weheartit.com/inspirations/taylorswift?scrolling=true&page="
target_dir = "/Users/reed/Desktop/images"


def make_file_name(path):
    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)
    dot_ps = path.rindex('.')
    image_path = os.path.join(target_dir, str(random.random())[-9:] + path[dot_ps:])
    print(image_path)
    return image_path


def get_page(url, data=None):
    print(url)
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    image_divs = soup.find_all("div", class_="entry-preview ")

    if data is None:
        print('len of images: ' + str(len(image_divs)))
        for image_div in image_divs:
            images = image_div.find_all("img", class_="entry-thumbnail")
            image_url = images[0].get('src')
            print(image_url)
            urllib.request.urlretrieve(image_url, make_file_name(image_url))
            print('.')


def walk_pages(start, end):
    for num in range(start, end):
        print('..')
        get_page(single_url + str(num))
        time.sleep(2)

walk_pages(3, 4)