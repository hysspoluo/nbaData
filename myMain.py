


import time

import os.path


from htmlManager import * #网页及文件分析模块
from dataBaseManager import *
#命令设置
command = 1

first_link = "http://nba.win007.com"
#result = {"type":"","time":"","home":"","result":"","guest":"","handicap":"","totle":"","analysis_link":"","euro_link":""}

#import time
seasonLink = "http://nba.win007.com/cn/Normal.aspx?matchSeason=2018-2019"
workPath = os.getcwd()
teamList = {"灰熊","篮网","掘金","老鹰","开拓者","火箭",
            "湖人","骑士","凯尔特人","太阳","马刺","尼克斯",
            "雷霆","爵士","猛龙","雄鹿","鹈鹕","国王",
            "步行者","76人","快船","公牛","魔术","活塞",
            "黄蜂","森林狼","热火","独行侠","奇才","勇士"}

if __name__=='__main__':
    #开始程序
    # 创建数据库，没有则新建数据库及文件
    createTables(teamList)
    #更新网页列表,写入html文件，如果command=0,先下载数据
    if command == 0:
        downLoadData(seasonLink)

    #写入数据库，如果command=1，开始写分析文件，写数据库
    if command == 1:
        #返回该文件的队伍的所有比赛，比赛是列表格式保存
        Schedule_List = analysishtml("勇士.html")
        #分析比赛list，每一行写入一条数据库
        writeIntoDatabase(Schedule_List, "勇士")





