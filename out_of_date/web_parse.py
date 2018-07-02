from bs4 import BeautifulSoup

html_path = "/Users/reed/Documents/dev/Plan-for-combating/week1/1_2/1_2code_of_video/web/new_index.html"

with open(html_path, 'r') as wb_data:
    Soup = BeautifulSoup(wb_data, "lxml")

    titles = Soup.select("body > div.main-content > ul > li > div.article-info > h3 > a")
    
    # body > div.main-content > ul > li:nth-child(1) > div.article-info > h3 > a

    images = Soup.select("body > div.main-content > ul > li > img")
    descs = Soup.select("body > div.main-content > ul > li > div.article-info > p.description")
    rates = Soup.select("body > div.main-content > ul > li > div.rate > span")
    cates = Soup.select("body > div.main-content > ul > li > div.article-info > p.meta-info")

info = []

for title, image, desc, rate, cate in list(zip(titles, images, descs, rates, cates)):
    data = {
        'title': title.get_text(),
        'rate': rate.get_text(),
        'desc': desc.get_text(),
        'cate': list(cate.stripped_strings),
        'image': image.get('src')
    }
    info.append(data)

for i in info:
    print('-----------------------------------------')
    print(i['title'])
    print(i['rate'])
    print(i['desc'])
    print(i['cate'])


# for i in info:
#     if float(i['rate']) > 3:
#         print(i['title'], " ---->>> ", i['desc'], " ---> ", i['rate'])


'''
body > div.main-content > ul > li:nth-child(1) > div.article-info > h3
body > div.main-content > ul > li:nth-child(1) > div.article-info > p.meta-info
body > div.main-content > ul > li:nth-child(1) > div.article-info > p.meta-info > span:nth-child(1)
body > div.main-content > ul > li:nth-child(1) > div.rate > span
body > div.main-content > ul > li:nth-child(1) > div.article-info > p.description
body > div.main-content > ul > li:nth-child(1) > img
'''