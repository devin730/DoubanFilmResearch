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
        self.item_dict_standard = {'title': 'title', 'score': 'score', 'eva_num': 'eva_num', 'intro': 'intro', 'url': 'url'}
        self.item_lists = []
        index = 0

        #/ 下面是搜索元素的代码
        search_result_lists = selector.xpath('//div[@class="result-list"]/div[@class="result"]')
        for list in search_result_lists:
            
            if not self.checkLengthLegal(list.xpath('div[2]/div[1]/h3/span/text()')):
                continue
            if list.xpath('div[2]/div[1]/h3/span/text()')[0] not in ['[电影]', '[电视剧]']:
                continue

            temp_item_dict = self.item_dict_standard.copy()
            self.item_lists.append(temp_item_dict)

            self.item_lists[index]['title'] = self.getValue(list.xpath('div[2]/div[1]/h3/a/text()'))
            self.item_lists[index]['score'] = self.getValue(list.xpath('div[2]/div[1]/div/span[2]/text()'))
            self.item_lists[index]['eva_num'] = self.getValue(list.xpath('div[2]/div[1]/div/span[3]/text()'))
            self.item_lists[index]['intro'] = self.getValue(list.xpath('div[2]/div[1]/div/span[4]/text()'))
            self.item_lists[index]['url'] = self.GetRightURL(list.xpath('div[2]/div[1]/h3/a/@href'))

            # !处理一个异常：
            if self.item_lists[index]['score'] == '(暂无评分)':
                self.item_lists[index]['intro'] = self.item_lists[index]['eva_num']
                self.item_lists[index]['eva_num'] = '0人评价'
                self.item_lists[index]['score'] = '-'

            # print(list.xpath('div[2]/div[1]/h3/a/@href'))
            index = index + 1
        self.items_count = len(self.item_lists)

        # *测试一下搜索条目的信息存储
        for index, itemlist in enumerate(self.item_lists):
            print(index+1, '/', self.items_count)
            print(itemlist)

    def GetRightURL(self, list):
        if len(list) == 0:
            return None
        target = str(list[0])
        index1 = target.find('subject')
        index2 = target.find('query')
        take_url = target[index1+10:index2-4]
        right_url = 'https://movie.douban.com/subject/' + take_url + '/'
        print(right_url)
        return right_url

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
