import pymongo
from bs4 import BeautifulSoup
import requests

client = pymongo.MongoClient('localhost', 27017)
xiaozhu = client['xiaozhu']
rent_house_info_tab = xiaozhu['rent_house_info_tab']

urls = ["http://bj.xiaozhu.com/search-duanzufang-p{}-0/".format(str(i)) for i in range(2, 3, 1)]
urls.insert(0, "http://bj.xiaozhu.com/")
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) ' +
                  'Chrome/54.0.2840.87 Safari/537.3',
    'Cookie': 'BIDUPSID=38C621C89B4684C48321DF9EB7CB3E6E; PSTM=1433342407; BDUSS=nAxUjdxeE81bUh1aWhjcGE3aWN' +
              'pZ2xKcnBaZlNXQ3A3dlZ5YzU1ZnpBU3ZrTFZXQVFBQUFBJCQAAAAAAAAAAAEAAACFwB8ucHl0aG9uMDEyAAAAAAAAAAAA' +
              'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAK8DjlavA45WW; BAIDUID=F94FE21C72' +
              '7AF8686514E3ACB930DADD:FG=1; MCITY=-218%3A; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=7; H_PS' +
              '_PSSID=1466_21103_17001_21263_21455_21409_21554_21399'
}
max_of_pages = 10000


def get_detail_page_url(list_page_url):
    wb_data = requests.get(list_page_url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    page_urls = soup.select("#page_list > ul > li > a")
    return [detail_page_url.get("href") for detail_page_url in page_urls]


def analyze_detail_page(single_detail_page_url):
    page_data = requests.get(single_detail_page_url, headers=headers)
    soup = BeautifulSoup(page_data.text, 'lxml')

    title = soup.select("body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > h4 > em")
    address = soup.select("body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > p")
    monthly_rental = soup.select("#pricePart > div.day_l > span")
    owner_name = soup.select("#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a")
    owner_sex_blocks = soup.select("#floatRightBox > div.js_box.clearfix > div.w_240 > h6")

    if len(owner_sex_blocks[0].find_all("span", class_="member_girl_ico")) > 0:
        sex = "female"
    else:
        sex = "male"

    data = {
        'Title': title[0].get_text(),
        'Address': address[0].get("title"),
        'Monthly rental': int(monthly_rental[0].get_text()),
        'Owner name': owner_name[0].get_text(),
        'Owner sex': sex
    }

    rent_house_info_tab.insert_one(data)


if __name__ == '__main__':
    count = 1
    for url in urls:
        for page_url in get_detail_page_url(url):
            if count < max_of_pages:
                analyze_detail_page(page_url)
                print('.')
                count += 1
            else:
                break

    for item in rent_house_info_tab.find({'Monthly rental': {'$gte': 500}}):
        print(item)
