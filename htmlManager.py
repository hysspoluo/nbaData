from bs4 import BeautifulSoup
import os
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#将球队的赛程源代码保存为html文件
def teamSource2Html(teamSource,teamHtml):
    fp = open(teamHtml, "w",encoding='utf-8')
    fp.write(teamSource)
    fp.close()

#NBA30支队伍名称
teamList = {"灰熊","篮网","掘金","老鹰","开拓者","火箭",
            "湖人","骑士","凯尔特人","太阳","马刺","尼克斯",
            "雷霆","爵士","猛龙","雄鹿","鹈鹕","国王",
            "步行者","76人","快船","公牛","魔术","活塞",
            "黄蜂","森林狼","热火","独行侠","奇才","勇士"}

#分析获取的网页信息，并反馈该对的所有比赛Schedule_List,每场比赛是一条数据
def analysishtml(teamHtml):
    soup = BeautifulSoup(open(teamHtml,"r",encoding='utf-8'),'html.parser')
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


#seasonLink,每个赛季都有对应一个网页链接
def downLoadData(seasonLink):
    myDriver = webdriver.Chrome()#加载chrome内核
    # time.sleep(5)
    myDriver.get(seasonLink)#打开指定
    myDriver.maximize_window()  # 最大化屏幕
    # 等待加载成功后，开始模拟选择队伍dropHome
    element = WebDriverWait(myDriver, 10).until \
        (EC.presence_of_element_located((By.ID, "dropHomeTeam")))
    # 获得队伍选项
    teamSelect = Select(myDriver.find_element_by_name("dropHomeTeam"))

    teamOptions = teamSelect.options #获得select中的所有选项名称
    optionNum = 0# optionNum用来遍历select，值就是索引
    # 开始写入文件html
    for team in teamOptions:
        if team.text in teamList: #如果被选中的文件为NBA球队
            teamSelect.select_by_index(optionNum)#选择该球队，跳转到该球队的页面
            ##########################
            ####此处需要修改，目前只能固定等2秒钟，无法等到页面加载完自动运行后续的内容
            time.sleep(2)
            ############################
            print(team.text)  # 队伍名字
            teamSource = myDriver.page_source #获得该支队伍所对应赛季seasonLink的所有比赛（季前赛、常规赛和季后赛）
            # 开始写入文件
            # 文件名
            teamHtml = team.text + ".html" #将该队伍的页面保存成hmtl，如"勇士.html"
            teamSource2Html(teamSource, teamHtml)
            # time.sleep(3)
        optionNum += 1
    myDriver.quit()
    print("写入html完成")