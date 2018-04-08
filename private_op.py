from bs4 import BeautifulSoup
import requests
import urllib.request
import os

# url = ""
#
# max_of_pages = 30

list1 = [1, 2, 3, 4]
list2 = [5, 6, 7, 8]

for a, b in zip(list1, list2):
    data = {
        'num1': a,
        'num2': b
    }

print(data)