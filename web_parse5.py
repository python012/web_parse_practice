from bs4 import BeautifulSoup
import requests

single_url = "http://weheartit.com/inspirations/taylorswift?scrolling=true&page="
target_dir = "/Users/reed/Desktop/images"

url_list = ["http://bj.58.com/pbdn/0/pn{}/".format(str(i)) for i in range(2, 2, 1)]
url_list.insert(0, "http://bj.58.com/pbdn/0/")


def get_detail_page_url_list(list_page_url):
    wb_data = requests.get(list_page_url)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    link_list = soup.select("#infolist > div.infocon > table > tbody > tr > td.img > a")
    print(len(link_list))
    return [link.get('href').split('?')[0] for link in link_list]


def analyze_page(url):
    html_data = requests.get(url)
    page_soup = BeautifulSoup(html_data.text, 'lxml')

    cates = page_soup.select('#nav > div > span > a')
    names = page_soup.select(
        'body > div.content > div > div.box_left > div.info_lubotu.clearfix > div.box_left_top > h1')
    prices = page_soup.select('body > div.content > div > div.box_left > div.info_lubotu.clearfix ' +
                              '> div.info_massege.left > div.price_li > span > i')
    locations = page_soup.select('body > div.content > div > div.box_left > div.info_lubotu.clearfix ' +
                                 '> div.info_massege.left > div.palce_li > span > i')
    sellers = page_soup.select('p.personal_name')
    views = page_soup.select('span.look_time')

    print(url)
    print("分类：" + cates[-1].get_text().strip())
    print("物品名：" + names[0].get_text())
    print("价格：" + prices[0].get_text())
    print("区域：" + locations[0].get_text())
    print("卖家：" + sellers[0].get_text())
    print("浏览量: " + views[0].get_text())


if __name__ == '__main__':
    for url in url_list:
        for page_url in get_detail_page_url_list(url):
            if len(page_url) > 105:
                continue
            else:
                print('----------------------------------------------')
                analyze_page(page_url)
