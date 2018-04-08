from bs4 import BeautifulSoup
import requests
import time
import os
import urllib
import random


target_dir = "/Users/reed/Desktop/1"

page_list = ["http://www.roufan.cc/roufan/6983_{}.html".format(str(i)) for i in range(2, 19, 1)]
page_list.insert(0, "http://www.roufan.cc/roufan/6983.html")


def make_file_name(path, num):
    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)
    dot_ps = path.rindex('.')
    image_path = os.path.join(target_dir, str(num) + path[dot_ps:])
    print(image_path)
    return image_path


def download_image(url, num, data=None):
    print(url)
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    image = soup.select('div.content img')

    if data is None:
        print('len of images: ' + str(len(image)))
        if len(image) == 1:
            image_url = image[0].get('src')
            urllib.request.urlretrieve(image_url, make_file_name(image_url, num))


if __name__ == '__main__':
    counter = 0
    for page_url in page_list:
        download_image(page_url, counter)
        counter += 1

