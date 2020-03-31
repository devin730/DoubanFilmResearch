#!/usr/bin/python
#coding: utf-8
#@since: 2020-03-30 19:32:58

import requests
from lxml import etree

class SearchDoubanFilm():
    def __init__(self, word):
        self.header = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Connection': 'keep - alive'
        }
        url_start = "https://www.douban.com/search?source=suggest&q="
        # url_start = "https://search.douban.com/movie/subject_search?search_text="  #! 下面这个页面提取的搜索条目似乎被加密了，无法定位到条目
        send_url = url_start + str(word)
        r = requests.get(send_url, headers=self.header)
        if r.status_code != 200:
            print("豆瓣电影的搜索页面没有正常打开")
        web_data = r.text
        selector = etree.HTML(web_data)

        #! 创建七个条目的字典list
        self.item_dict0 = {'title': 'title', 'score': 'score', 'eva_num': 'eva_num', 'intro': 'intro'}
        self.item_dict1 = {'title': 'title', 'score': 'score', 'eva_num': 'eva_num', 'intro': 'intro'}
        self.item_dict2 = {'title': 'title', 'score': 'score', 'eva_num': 'eva_num', 'intro': 'intro'}
        self.item_dict3 = {'title': 'title', 'score': 'score', 'eva_num': 'eva_num', 'intro': 'intro'}
        self.item_dict4 = {'title': 'title', 'score': 'score', 'eva_num': 'eva_num', 'intro': 'intro'}
        self.item_dict5 = {'title': 'title', 'score': 'score', 'eva_num': 'eva_num', 'intro': 'intro'}
        self.item_dict6 = {'title': 'title', 'score': 'score', 'eva_num': 'eva_num', 'intro': 'intro'}
        self.item_lists = []
        self.item_lists.append(self.item_dict0)
        self.item_lists.append(self.item_dict1)
        self.item_lists.append(self.item_dict2)
        self.item_lists.append(self.item_dict3)
        self.item_lists.append(self.item_dict4)
        self.item_lists.append(self.item_dict5)
        self.item_lists.append(self.item_dict6)
        # print(self.item_lists)

        #/ 下面是搜索元素的代码
        search_result_lists = selector.xpath('//div[@class="result-list"]/div[@class="result"]')
        for index, list in enumerate(search_result_lists):
            if index >= 7:
                # print('只搜索前七条，后面的不打印')
                continue
            if not self.checkLengthLegal(list.xpath('div[2]/div[1]/h3/span/text()')):
                continue
            if list.xpath('div[2]/div[1]/h3/span/text()')[0] not in ['[电影]', '[电视剧]']:
                continue
            self.item_lists[index]['title'] = self.getValue(list.xpath('div[2]/div[1]/h3/a/text()'))
            self.item_lists[index]['score'] = self.getValue(list.xpath('div[2]/div[1]/div/span[2]/text()'))
            self.item_lists[index]['eva_num'] = self.getValue(list.xpath('div[2]/div[1]/div/span[3]/text()'))
            self.item_lists[index]['intro'] = self.getValue(list.xpath('div[2]/div[1]/div/span[4]/text()'))

        print(self.item_lists)

    def checkLengthLegal(self, xpath_selector):
        if len(xpath_selector) == 0:
            return False
        return True
    
    def getValue(self, xpath_selector):
        if len(xpath_selector) == 0:
            return 'None'
        else:
            return xpath_selector[0]
            
        
if __name__ == '__main__':
    s = SearchDoubanFilm(word='隐形人')