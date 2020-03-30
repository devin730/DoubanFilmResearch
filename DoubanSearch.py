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
        # print(web_data)
        selector = etree.HTML(web_data)
        search_result_lists = selector.xpath('//div[@class="result-list"]/div[@class="result"]')
        # print(search_result_lists)
        for list in search_result_lists:
            if len(list.xpath('div[2]/div[1]/h3/span/text()')) == 0:
                continue
            if list.xpath('div[2]/div[1]/h3/span/text()')[0] not in ['[电影]', '[电视剧]']:
                continue
            print("___________________________________")
            print(list.xpath('div[2]/div[1]/h3/span/text()'))
            print(list.xpath('div[2]/div[1]/h3/a/text()'))
            print(list.xpath('div[2]/div[1]/h3/a/text()'))
            print(list.xpath('div[2]/div[1]/div/span[2]/text()')[0]+' 分')
            print(list.xpath('div[2]/div[1]/div/span[3]/text()')[0])
            # print(list.xpath('div[2]/div[1]/div/span[4]/text()')[0])
            # !要验证是不是有这个项，然后再输出。
            # !搜索的时候是不是可以先跳到专页？
            
        
if __name__ == '__main__':
    s = SearchDoubanFilm(word='行尸走肉')