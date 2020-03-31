#!/usr/bin/python
#coding: utf-8
import wx
import time
from DoubanSearch import SearchDoubanFilm

class Example(wx.Frame):
    
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title)
        self.InitUI()
        self.Centre()

    def InitUI(self):
        self.panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer = wx.GridBagSizer(5, 5)
        self.font = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        # 标题栏
        text_title = wx.StaticText(self.panel, label="电影搜索小工具")
        text_title.SetFont(self.font)
        self.sizer.Add(text_title, pos=(0, 0), span=(1, 3), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=15)
        # icon = wx.StaticBitmap(self.panel, bitmap=wx.Bitmap('./assets/title.jpg'))
        # self.sizer.Add(icon, pos=(0, 4), flag=wx.TOP | wx.RIGHT | wx.ALIGN_RIGHT, border=5)
        # 画一条线
        line = wx.StaticLine(self.panel)
        self.sizer.Add(line, pos=(1, 0), span=(1, 5), flag=wx.EXPAND | wx.BOTTOM, border=10)
        # 搜索框这一栏
        text2 = wx.StaticText(self.panel, label="输入电影名")
        font2 = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        text2.SetFont(font2)
        self.sizer.Add(text2, pos=(2, 0), flag=wx.LEFT, border=10)
        
        self.tc_search = wx.TextCtrl(self.panel)
        self.sizer.Add(self.tc_search, pos=(3, 0), span=(1, 3), flag=wx.TOP | wx.EXPAND | wx.LEFT, border=10)
        
        button1 = wx.Button(self.panel, label="搜索", size=(70, 30))
        button1.Bind(wx.EVT_BUTTON, self.ClickToSearch)
        self.sizer.Add(button1, pos=(3, 3), flag=wx.TOP | wx.RIGHT, border=5)

        # 做一个状态栏
        self.text_status = wx.StaticText(self.panel, label="搜索结果框")
        self.sizer.Add(self.text_status, pos=(4, 0), flag=wx.LEFT, border=10)
        
        # *搜索结果以条目的形式显示在下面
        self.listct = wx.ListCtrl(self.panel, -1, style=wx.LC_REPORT)
        self.listct.InsertColumn(0, '电影名称', wx.LIST_FORMAT_CENTER, width=150)
        self.listct.InsertColumn(1, '评分', wx.LIST_FORMAT_RIGHT, width=50)
        self.listct.InsertColumn(2, '评分人数', wx.LIST_FORMAT_RIGHT, width=100)
        self.listct.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDouClick)
        self.sizer.Add(self.listct, pos=(5, 0), span=(0, 5), flag=wx.TOP | wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        hbox.Add(self.sizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        
        # *做一个电影详情的介绍box
        static_box = wx.StaticBox(self.panel, label="影片详细信息", size=(300, 600))
        static_box.SetFont(font2)
        boxsizer = wx.StaticBoxSizer(static_box, wx.VERTICAL)
        film_icon = wx.StaticBitmap(self.panel, bitmap=wx.Bitmap('./assets/title.jpg'))
        boxsizer.Add(film_icon, flag=wx.TOP | wx.RIGHT | wx.ALIGN_RIGHT, border=5)
        
        text3 = wx.StaticText(self.panel, label="电影名称")
        boxsizer.Add(text3, flag=wx.TOP | wx.LEFT, border=5)
        self.tc_film_name = wx.TextCtrl(self.panel, style=wx.TE_READONLY)
        boxsizer.Add(self.tc_film_name, flag=wx.TOP | wx.EXPAND | wx.LEFT, border=5)

        text4 = wx.StaticText(self.panel, label="电影评分")
        boxsizer.Add(text4, flag=wx.TOP | wx.LEFT, border=5)
        self.tc_film_score = wx.TextCtrl(self.panel, style=wx.TE_READONLY)
        boxsizer.Add(self.tc_film_score, flag=wx.TOP | wx.EXPAND | wx.LEFT, border=5)

        text5 = wx.StaticText(self.panel, label="评分人数")
        boxsizer.Add(text5, flag=wx.TOP | wx.LEFT, border=5)
        self.tc_film_scorenum = wx.TextCtrl(self.panel, style=wx.TE_READONLY)
        boxsizer.Add(self.tc_film_scorenum, flag=wx.TOP | wx.EXPAND | wx.LEFT, border=5)

        text6 = wx.StaticText(self.panel, label="电影简介")
        boxsizer.Add(text6, flag=wx.TOP | wx.LEFT, border=5)
        self.tc_film_intro = wx.TextCtrl(self.panel, style=wx.TE_READONLY)
        boxsizer.Add(self.tc_film_intro, flag=wx.TOP | wx.EXPAND | wx.LEFT, border=5)

        text7 = wx.StaticText(self.panel, label="豆瓣网页链接")
        boxsizer.Add(text7, flag=wx.TOP | wx.LEFT, border=5)
        self.tc_film_url = wx.TextCtrl(self.panel, style=wx.TE_READONLY)
        boxsizer.Add(self.tc_film_url, flag=wx.TOP | wx.EXPAND | wx.LEFT, border=5)

        btn_douban = wx.Button(self.panel, label="前往豆瓣页", size=(70, 30))
        btn_download = wx.Button(self.panel, label="搜索下载资源", size=(70, 30))
        btn_online = wx.Button(self.panel, label="搜索在线播放", size=(70, 30))
        btn_douban.Bind(wx.EVT_BUTTON, self.GotoDouban)
        btn_download.Bind(wx.EVT_BUTTON, self.SearchDown)
        btn_online.Bind(wx.EVT_BUTTON, self.SearchOnline)

        boxsizer.Add(btn_douban, flag=wx.TOP | wx.EXPAND | wx.LEFT, border=5)
        boxsizer.Add(btn_download, flag=wx.TOP | wx.EXPAND | wx.LEFT, border=5)
        boxsizer.Add(btn_online, flag=wx.TOP | wx.EXPAND | wx.LEFT, border=5)

        hbox.Add(boxsizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.panel.SetSizer(hbox)
        # self.sizer.Fit(self)
        self.SetSize(800, 600)

    def GotoDouban(self, e):
        pass

    def SearchDown(self, e):
        pass

    def SearchOnline(self, e):
        pass

    def OnDouClick(self, e):
        print("Current selection:" + str(e.GetEventObject().GetFirstSelected())+"\n")

    def ClickToSearch(self, e):
        self.text_status.SetLabel('开始搜索...')
        # self.tc_search 里存放了需要搜索的电影名称
        txt = self.tc_search.GetValue()
        print(txt)
        re = SearchDoubanFilm(word=txt)

        players = [(re.item_dict0['title'], re.item_dict0['score'], re.item_dict0['eva_num']),
                   (re.item_dict1['title'], re.item_dict1['score'], re.item_dict1['eva_num']),
                   (re.item_dict2['title'], re.item_dict2['score'], re.item_dict2['eva_num']),
                   (re.item_dict3['title'], re.item_dict3['score'], re.item_dict3['eva_num']),
                   (re.item_dict4['title'], re.item_dict4['score'], re.item_dict4['eva_num']),
                   (re.item_dict5['title'], re.item_dict5['score'], re.item_dict5['eva_num']),
                   (re.item_dict6['title'], re.item_dict6['score'], re.item_dict6['eva_num'])]

        for i in players:
            index = self.listct.InsertItem(0, i[0])
            self.listct.SetItem(index, 1, i[1])
            self.listct.SetItem(index, 2, i[2])
        self.text_status.SetLabel('搜索完成!双击显示详情!')

if __name__ == '__main__':
    app = wx.App()
    ex = Example(None, title="搜索电影小工具")
    ex.Show()
    app.MainLoop()
