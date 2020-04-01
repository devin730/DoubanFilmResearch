#!/usr/bin/python
#coding: utf-8

import requests
from lxml import etree
import os

class DoubanMovieInfo():
    def __init__(self, url):
        self.header = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Connection': 'keep - alive'
        }
        douban_url = url
        r = requests.get(douban_url, headers=self.header)
        if r.status_code != 200:
            print("这个电影的豆瓣页面没有正常打开!")
            self.Info_status = 0
            return
        web_data = r.text
        selector = etree.HTML(web_data)

        # *开始搜索信息
        self.info_dict = {'title': 'title', 'year': 'year', 'director': 'director', 'actors': 'actors',
                          'types': 'types', 'language': 'language', 'show_date': 'show_date',
                          'country': 'country', 'imdb_url': 'imdb_url', 'image': 'image'}

        self.info_dict['title'] = selector.xpath('//*[@id="content"]/h1/span[1]/text()')[0]
        self.info_dict['year'] = selector.xpath('//*[@id="content"]/h1/span[2]/text()')[0]
        self.info_dict['director'] = selector.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')[0]
        self.info_dict['show_date'] = selector.xpath('//span[@property="v:initialReleaseDate"]/text()')[0]
        
        if len(selector.xpath('//*[@id="info"]/span[3]/span[2]/a/text()')) >= 1:
            self.info_dict['actors'] = ''
            for i in selector.xpath('//*[@id="info"]/span[3]/span[2]/a/text()'):
                self.info_dict['actors'] += (str(i)+"/")
        else:
            self.info_dict['actors'] = '...'

        if len(selector.xpath('//span[@property="v:genre"]/text()')) >= 1:
            self.info_dict['types'] = ''
            for i in selector.xpath('//span[@property="v:genre"]/text()'):
                self.info_dict['types'] += (str(i)+"/")
        else:
            self.info_dict['types'] = '...'
        
        # if len(selector.xpath('//*[@id="info"]/a')) == 1:
        #     self.info_dict['imdb_url'] = selector.xpath('//*[@id="info"]/a/@href')[0]
        # elif len(selector.xpath('//*[@id="info"]/a')) >= 1:
        #     self.info_dict['imdb_url'] = selector.xpath('//*[@id="info"]/a' + str(len(selector.xpath('//*[@id="info"]/a'))-1)+'/@href')
        # else:
        #     self.info_dict['imdb_url'] = 'None'
        # self.info_dict['country'] = selector.xpath('//*[@id="info"]/text()')  #! 先不提取
        # self.info_dict['language'] = selector.xpath()  #! 先不提取
        # print(self.info_dict['title'])
        # print(self.info_dict['year'])
        # print(self.info_dict['show_date'])
        # print(self.info_dict['imdb_url'])
        image_url_list = selector.xpath('//img[@rel="v:image"]/@src')
        if len(image_url_list) >= 0:
            self.DownloadImage(image_url_list[0])
        
        if len(selector.xpath('//span[@property="v:summary"]/text()')) >= 1:
            self.intro = ''
            for i in selector.xpath('//span[@property="v:summary"]/text()'):
                x = str(i).replace(' ', '')
                x = x.replace('\n', '')
                self.intro += x
        else:
            self.intro = '...'

        # print(self.intro)
        self.Info_status = 200
    
    def DownloadImage(self, url):
        os.makedirs('./image/', exist_ok=True)
        x = requests.get(url)
        file_name = str(self.info_dict['title']) + '.jpg'
        path = './image/'+file_name
        with open(path, 'wb') as f:
            f.write(x.content)
            self.info_dict['image'] = path
            # print('图片保存成功在'+path)


if __name__ == '__main__':
    x = DoubanMovieInfo('https://movie.douban.com/subject/3074460/')
    x = DoubanMovieInfo('https://movie.douban.com/subject/2364086/')
