#!/usr/bin/python
#coding: utf-8
#@since: 2020-03-30 19:32:58

import requests
# import time
# import random
from lxml import etree
from MyDescription import SplitDescription

class SearchDoubanFilm():
    def __init__(self, word):
        self.header = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Connection': 'keep - alive'
        }
        url_start = "https://www.douban.com/search?source=suggest&q="
        send_url = url_start + str(word)
        r = requests.get(send_url, headers=self.header)
        if r.status_code != 200:
            print("豆瓣电影的搜索页面没有正常打开")
        web_data = r.text
        selector = etree.HTML(web_data)
        search_result_lists = selector.xpath('//*[@id="content"]/div/div[1]/div[3]')
        print(search_result_lists)
        # for list in search_result_lists:
            # title = list.xpath('/div[2]/div/h3/a/text()')
            # title = list.xpath('/div[2]/div[1]/div[2]/div/h3/a')
            # print(title)
            # //*[@id="content"]
            # //*[@id="content"]/div/div[1]/div[3]
            # //*[@id="content"]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/h3/a
        
if __name__ == '__main__':
    s = SearchDoubanFilm(word='行尸走肉')