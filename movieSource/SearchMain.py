# -*- encoding:utf-8 -*-
import sys
from os import path
d = path.dirname(__file__)  # 获取当前路径
parent_path = path.dirname(d)  # 获取上一级路径
sys.path.append(parent_path)    # 如果要导入到包在上一级
from movieSource.MovieHeaven import SunshineMovie

class DownloadWeb():
    def __init__(self, name):
        self.__params = {"typeid": "1", "keyword": name.encode('gb2312')}
        self.download_url_lists = []
        sunshine = SunshineMovie()
        self.sunshine_results_lists = sunshine.get_display_content(params=self.__params)
        
    def GetLinkLists(self):
        if len(self.sunshine_results_lists) != 0:
                self.download_url_lists.extend(self.sunshine_results_lists)
        #! 在这个函数里，将多个网站的搜索信息进行汇总，最后放在一个list中，返回给GUI界面
        return self.download_url_lists

if __name__ == '__main__':
    x = DownloadWeb('西游记')
    lists = x.GetLinkLists()
    print(lists)
