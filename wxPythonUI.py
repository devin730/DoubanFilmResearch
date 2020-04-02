#!/usr/bin/python
#coding: utf-8
import wx
# import time
from DoubanSearch import SearchDoubanFilm
from DoubanMovie import DoubanMovieInfo
from PIL import Image
import webbrowser


class Example(wx.Frame):
    
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title)
        self.InitUI()
        self.Centre()

    def InitUI(self):
        self.panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer = wx.GridBagSizer(5, 5)
        # self.sizer.SetMinSize(300, 100)
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
        
        self.tc_search = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.tc_search.Bind(wx.EVT_TEXT_ENTER, self.ClickToSearch)
        self.sizer.Add(self.tc_search, pos=(3, 0), span=(1, 3), flag=wx.TOP | wx.EXPAND | wx.LEFT, border=10)
        
        button1 = wx.Button(self.panel, label="搜索", size=(70, 30))
        button1.Bind(wx.EVT_BUTTON, self.ClickToSearch)
        self.sizer.Add(button1, pos=(3, 3), flag=wx.TOP | wx.RIGHT, border=5)

        # 做一个状态栏
        self.text_status = wx.StaticText(self.panel, label="搜索结果框")
        self.sizer.Add(self.text_status, pos=(4, 0), flag=wx.LEFT, border=10)
        
        # *搜索结果以条目的形式显示在下面
        self.listct = wx.ListCtrl(self.panel, -1, style=wx.LC_REPORT, size=(-1, 475))
        self.listct.InsertColumn(0, '电影名称', wx.LIST_FORMAT_CENTER, width=120)
        self.listct.InsertColumn(1, '评分', wx.LIST_FORMAT_RIGHT, width=50)
        self.listct.InsertColumn(2, '评分人数', wx.LIST_FORMAT_RIGHT, width=100)
        self.listct.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDouClick)
        self.sizer.Add(self.listct, pos=(5, 0), span=(0, 5), flag=wx.TOP | wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        hbox.Add(self.sizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        
        # *做一个电影详情的介绍box
        static_box = wx.StaticBox(self.panel, label="影片详细信息", size=(300, 600))
        static_box.SetFont(font2)
        self.film_icon = wx.StaticBitmap(self.panel, bitmap=wx.Bitmap('./assets/title.png'), style=wx.ALIGN_CENTER_HORIZONTAL)
        self.box_film_title = wx.StaticText(self.panel, label="电影名称:")
        self.box_film_score = wx.StaticText(self.panel, label="电影评分:")
        self.box_film_scorecnt = wx.StaticText(self.panel, label="评分人数:")
        self.box_film_url = wx.StaticText(self.panel, label="豆瓣网页链接:")
        self.box_film_year = wx.StaticText(self.panel, label="电影年代: ")
        self.box_film_director = wx.StaticText(self.panel, label="导演: ")
        self.box_film_actors = wx.StaticText(self.panel, label="演员: ")
        self.box_film_types = wx.StaticText(self.panel, label="类型: ")
        self.box_film_date = wx.StaticText(self.panel, label="上映时间: ")
        self.box_film_intro = wx.TextCtrl(self.panel, value="电影简介:", size=(300, 100), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.box_film_urltxt = wx.TextCtrl(self.panel, value="", style=wx.TE_READONLY | wx.TE_AUTO_URL, size=(300, -1))

        boxsizer = wx.StaticBoxSizer(static_box, wx.VERTICAL)
        boxsizer.Add(self.film_icon, flag=wx.TOP | wx.RIGHT | wx.ALIGN_CENTER_HORIZONTAL, border=5)
        boxsizer.Add(self.box_film_title, flag=wx.TOP | wx.LEFT, border=5)
        boxsizer.Add(self.box_film_score, flag=wx.TOP | wx.LEFT, border=5)
        boxsizer.Add(self.box_film_scorecnt, flag=wx.TOP | wx.LEFT, border=5)
        boxsizer.Add(self.box_film_year, flag=wx.TOP | wx.LEFT, border=5)
        boxsizer.Add(self.box_film_director, flag=wx.TOP | wx.LEFT, border=5)
        boxsizer.Add(self.box_film_actors, flag=wx.TOP | wx.LEFT, border=5)
        boxsizer.Add(self.box_film_types, flag=wx.TOP | wx.LEFT, border=5)
        boxsizer.Add(self.box_film_date, flag=wx.TOP | wx.LEFT, border=5)
        boxsizer.Add(self.box_film_url, flag=wx.TOP | wx.LEFT, border=5)
        boxsizer.Add(self.box_film_urltxt, flag=wx.TOP | wx.LEFT, border=5)
        boxsizer.Add(self.box_film_intro, flag=wx.TOP | wx.LEFT, border=5)

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
        self.SetSize(800, 720)

    def GotoDouban(self, e):
        pass

    def SearchDown(self, e):
        pass

    def SearchOnline(self, e):
        pass

    def OnDouClick(self, e):
        itemID = e.GetEventObject().GetFirstSelected()
        # print("Current selection:" + str(itemID)+"\n")

        SubjectURL = self.re.item_lists[itemID]['url']
        
        self.movie_re = DoubanMovieInfo(SubjectURL)
        
        path = self.movie_re.info_dict['image']
        self.Image_PreProcessing(tsize=(135, 186), path=path)
        Film_image = wx.Bitmap(path, wx.BITMAP_TYPE_JPEG)
        self.film_icon.SetBitmap(Film_image)

        self.box_film_title.SetLabel("电影名称: "+self.movie_re.info_dict['title'])
        self.box_film_year.SetLabel("电影年代: "+self.movie_re.info_dict['year'])
        self.box_film_score.SetLabel("电影评分: "+self.re.item_lists[itemID]['score'])
        self.box_film_scorecnt.SetLabel("评分人数: "+self.re.item_lists[itemID]['eva_num'])
        self.box_film_director.SetLabel("导演: "+self.movie_re.info_dict['director'])
        self.box_film_actors.SetLabel("演员: "+self.movie_re.info_dict['actors'])
        self.box_film_types.SetLabel("类型: "+self.movie_re.info_dict['types'])
        self.box_film_date.SetLabel("上映时间: "+self.movie_re.info_dict['show_date'])
        self.box_film_intro.SetValue("电影简介: "+self.movie_re.intro)

        self.url_to_open = self.re.item_lists[itemID]['url']
        self.box_film_urltxt.SetValue(self.url_to_open)
        self.box_film_urltxt.Bind(wx.EVT_LEFT_DCLICK, self.OpenURL)

    def OpenURL(self, e):
        print('OpenURL')
        webbrowser.open(url=self.url_to_open, new=0, autoraise=True)
        print('222')
        
        return

    def Image_PreProcessing(self, tsize, path):
        # 待处理图片存储路径
        im = Image.open(path)
        # Resize图片大小，入口参数为一个tuple，新的图片大小
        if im.size == tsize:
            return
        else:
            imBackground = im.resize(tsize)
            # 处理后的图片的存储路径，以及存储格式
            imBackground.save(path, 'JPEG')
        return
            
    def ClickToSearch(self, e):
        self.text_status.SetLabel('开始搜索...')
        # self.tc_search 里存放了需要搜索的电影名称
        txt = self.tc_search.GetValue()
        print(txt)
        self.re = SearchDoubanFilm(word=txt)

        result_item_count = self.re.items_count
        players = []

        if result_item_count <= 0:
            #! 没有搜索到，需要设置一个响应机制
            pass

        # elif result_item_count <= 10:  # 搜索返回的条目比较少
        for item in self.re.item_lists:
            (title, score, cnt) = (item['title'], item['score'], item['eva_num'])
            players.append((title, score, cnt))

        # 先清空之前的条目
        self.listct.DeleteAllItems()
        rows = 0
        for i in players:
            index = self.listct.InsertItem(rows, i[0])
            self.listct.SetItem(index, 1, i[1])
            self.listct.SetItem(index, 2, i[2])
            rows = rows + 1
        self.text_status.SetLabel('搜索完成!双击显示详情!')

if __name__ == '__main__':
    app = wx.App()
    ex = Example(None, title="戴文搜电影")
    ex.Show()
    app.MainLoop()
