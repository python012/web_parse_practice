from bs4 import BeautifulSoup
import requests

urls = ["http://bj.xiaozhu.com/search-duanzufang-p{}-0/".format(str(i)) for i in range(2, 5, 1)]
urls.insert(0, "http://bj.xiaozhu.com/")
max_of_pages = 30


def get_detail_page_url(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    page_urls = soup.select("#page_list > ul > li > a")
    return [detail_page_url.get("href") for detail_page_url in page_urls]


def analyze_detail_page(url_str, num):
    page_data = requests.get(url_str)
    soup = BeautifulSoup(page_data.text, 'lxml')

    title = soup.select("body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > h4 > em")
    address = soup.select("body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > p")
    monthly_rental = soup.select("#pricePart > div.day_l > span")
    room_image = soup.select("#curBigImage")
    owner_image = soup.select("#floatRightBox > div.js_box.clearfix > div.member_pic > a > img")
    owner_name = soup.select("#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a")
    owner_sex_blocks = soup.select("#floatRightBox > div.js_box.clearfix > div.w_240 > h6")

    if len(owner_sex_blocks[0].find_all("span", class_="member_girl_ico")) > 0:
        sex = "female"
    else:
        sex = "male"

    print("Number: " + str(num))
    print("Title: " + title[0].get_text())
    print("Address: " + address[0].get("title"))
    print("Monthly rental: " + monthly_rental[0].get_text())
    print("Room image: " + room_image[0].get("src"))
    print("Owner image: " + owner_image[0].get("src"))
    print("Owner name: " + owner_name[0].get_text())
    print("Owner sex: " + sex)
    print("-------------------------------------------------------")


if __name__ == '__main__':
    count = 1
    for url in urls:
        for page_url in get_detail_page_url(url):
            if count < max_of_pages:
                analyze_detail_page(page_url, count)
                count += 1
            else:
                break
