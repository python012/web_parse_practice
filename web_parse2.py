from bs4 import BeautifulSoup

html_path = "/Users/reed/Documents/dev/Plan-for-combating/week1/1_2/1_2answer_of_homework/index.html"

with open(html_path, 'r') as wb_data:
    soup = BeautifulSoup(wb_data, "lxml")

    images = soup.select("body > div > div > div.col-md-9 > div > div > div > img")
    names = soup.select("body > div > div > div.col-md-9 > div > div > div > div.caption > h4 > a")
    prices = soup.select("body > div > div > div.col-md-9 > div > div > div > div.caption > h4.pull-right")
    reviews = soup.select("body > div > div > div.col-md-9 > div > div > div > div.ratings > p.pull-right")
    stars_block = soup.find_all("div", class_="ratings")

for name, image, price, review, star_block in zip(names, images, prices, reviews, stars_block):
    stars_num = len(star_block.find_all("span", class_="glyphicon glyphicon-star"))
    print(name.get_text(), "\n    ", image.get('src'), "\n    ", price.get_text(), "\n    ", review.get_text(),
          "\n    ", stars_num, " stars\n")
