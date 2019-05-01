from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os
import os.path
import sqlite3

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


def htmlwriteinTxt(pageSource,txtName):
    fp = open(txtName, "w",encoding='utf-8')
    fp.write(pageSource)
    fp.close()
#分析获取的网页信息
def analysishtml(txtName):
    soup = BeautifulSoup(open(txtName,"r",encoding='utf-8'),'html.parser')
    table = soup.find("table",id="scheTab")
    trs = table.find_all("tr")
    trs_len = len(trs)
    Schedule_List = []
    first_link = "http://nba.win007.com"
    for tr_num in range(1, trs_len):
        tds = trs[tr_num].find_all("td")
        trs_len = len(tds)
        result = {"type": "", "time": "", "home": "", "result": "", "guest": "", "handicap": "", "totle": "",
                  "analysis_link": "", "euro_link": ""}
        result['type'] = tds[0].text
        result["time"] = tds[1].text
        result["home"] = tds[2].text
        result["result"] = tds[3].text
        result["guest"] = tds[4].text
        result['handicap'] = tds[5].text
        result["totle"] = tds[6].text
        if tds[7].text == "[析][欧]":
            result["analysis_link"] = first_link + (tds[7].a)['href']
            result["euro_link"] = first_link + (tds[7].a.next_sibling)['href']
        elif tds[7].text == "[析]":
            result["analysis_link"] = first_link + (tds[7].a)['href']
        elif tds[7].text == "[欧]":
            result["euro_link"] = first_link + (tds[7].a.next_sibling)['href']
        Schedule_List.append(result)

    return Schedule_List


#创建球队的表，每个表有球队这个赛季的所有赛程
def createTables(teamlist):
    conn = sqlite3.connect('nba.db')
    print("连接数据库，没有则新建")
    cursor = conn.cursor()
    for team in teamlist:
        createtableString = 'create table if not exists "%s" (season text,type text,' \
                            'time text,home text,result text,guest text,handicap text,' \
                            'totle text,analysis_Link text,euro_Link text)'%(team)
        cursor.execute(createtableString)
    cursor.close()
    conn.commit()
    conn.close()

def writeIntoDatabase(Schedule_List,teamName):
    conn = sqlite3.connect('nba.db')
    print("打开数据库，对表进行读写")
    cursor = conn.cursor()

    for game in Schedule_List:
        season = "2018-2019"

        insetString = 'insert into %s (season,type,time,home,result,guest,handicap,totle,analysis_link,euro_link)' \
                     'values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'\
        %(teamName,season,game['type'],game['time'],game['home'],game['result'],game['guest'],game['handicap'],game['totle'],game['analysis_link'],game['euro_link'])
        print(insetString)
        '''
        insertString = 'insert into %s (id,season,type,time,home,result,guest,handicap,totle,analysis_Link,euro_Link)' \
                       'values (%d,"2009-2010","常规赛","十点","","","","","","","")'%(teamName,id)
        game['type'],game['time'],game['home'],game['result'],game['guest'],game['handicap'],game['totle'],game['analysis_link'],game['euro_link']
        '''
        cursor.execute(insetString)
        conn.commit()


    #conn.commit()
    conn.close()



if __name__=='__main__':
    #开始程序

    createTables(teamList)
    '''
    myDriver = webdriver.Chrome()
    #time.sleep(5)
    myDriver.get(seasonLink)
    myDriver.maximize_window()#最大化屏幕
    #等待加载成功后，开始选择
    element = WebDriverWait(myDriver, 10).until\
        (EC.presence_of_element_located((By.ID, "dropHomeTeam")))
    #获得队伍选项
    teamSelect = Select(myDriver.find_element_by_name("dropHomeTeam"))

    teamOptions = teamSelect.options
    optionNum = 0
    #开始写入文件html
    for team in teamOptions:
        if team.text in teamList:
            teamSelect.select_by_index(optionNum)
            ##########################
            ####此处需要修改
            time.sleep(2)
            ############################
            print(team.text) #队伍名字
            teamHtml = myDriver.page_source
            #开始写入文件
            #文件名
            txtName = team.text +".html"
            htmlwriteinTxt(teamHtml,txtName)
            #time.sleep(3)
        optionNum += 1
    #分析文件,写入数据库
    analysishtml("灰熊.html")
    '''

#######################################
######老子敲了几个注释####

    #for team in teamList:
     #   teamNameFile = team+".html"
     #   Schedule_List = analysishtml(teamNameFile)
    #    writeIntoDatabase(Schedule_List,team)
    #myDriver.quit()
    Schedule_List = analysishtml("灰熊.html")
    writeIntoDatabase(Schedule_List, "灰熊")

