import requests
from lxml import etree
import time
import random

# ciligou.app的种子搜索链接

class mPage():
    def __init__(self, url):
        self.header = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Connection': 'keep - alive'
        }
        req = requests.get(url, headers=self.header, timeout=5)
        selector = etree.HTML(req.text)
        self.magnet = selector.xpath('//a[@id="down-url"]/@href')
        self.title = selector.xpath('//h1[@class="Information_title"]/text()')

class SearchCiligou():
    def __init__(self, word):
        self.header = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Connection': 'keep - alive'
        }
        self.starturl = "https://ciligou.app"
        self.url = "https://ciligou.app/search?word="
        self.search_word = word
        self.search_url = self.url + self.search_word
        self.item_lists = []
        r = None
        try:
            r = requests.get(self.search_url, headers=self.header, timeout=5)
        except Exception:
            print("connection to ciligou.app web is failed.")
        
        webtext = r.text
        selector = etree.HTML(webtext)
        ahref_lists = selector.xpath('//div[@class="SearchListTitle_list_title"]/a/@href')
        for item in ahref_lists:
            time.sleep(0.5+random.random())
            m = mPage(self.starturl+item)
            movie_info = {'title': m.title, 'url': m.magnet}
            self.item_lists.append(movie_info)
            time.sleep(0.5+random.random())
        print('搜索完成')

if __name__ == '__main__':
    x = SearchCiligou(word='战狼')
