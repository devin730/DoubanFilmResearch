import requests
from lxml import etree
from MyDescription import SplitDescription

search_word = '行尸走肉'
douban_file_url = 'https://www.douban.com/search?source=suggest&q='
send_url = douban_file_url + str(search_word)
header = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Connection': 'keep - alive'
        }
web_data = requests.get(send_url, headers=header).text
selector = etree.HTML(web_data)
li_lists = selector.xpath('//ol[@class="grid_view"]/li')
# print(li_lists)
for list in li_lists:
    title = list.xpath('div/div[2]/div[@class="hd"]/a/span[1]/text()')  # title
    film_url = list.xpath('div/div[2]/div[@class="hd"]/a/@href')  # url
    description = list.xpath('div/div[2]/div[@class="bd"]/p[1]/text()')  # description
    scores = list.xpath('div/div[2]/div[@class="bd"]/div[1]/span[2]/text()')  # scores
    comments_count = list.xpath('div/div[2]/div[@class="bd"]/div[1]/span[4]/text()')  # comments count
    quote = list.xpath('div/div[2]/div[@class="bd"]/p[2]/span/text()')  # quote
    
    x = SplitDescription(description)
    director = x.Director
    stars = x.Stars
    year = x.Year
    country = x.Country
    category = x.Category
    print(title)
    print(film_url)
