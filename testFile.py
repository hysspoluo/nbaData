from bs4 import BeautifulSoup

soup = BeautifulSoup(open("勇士.html","r",encoding='utf-8'),'html.parser')
table = soup.find("table",id="scheTab")
trs = table.find_all("tr")
trs_len = len(trs)
result_list = []
first_link = "http://nba.win007.com"

for tr_num in range(1,trs_len):
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
    elif tds[7].text =="[析]":
        result["analysis_link"] = first_link + (tds[7].a)['href']
    elif tds[7].text =="[欧]":
        result["euro_link"] = first_link + (tds[7].a.next_sibling)['href']
    result_list.append(result)
for one in result_list:
    print(one)
    print("fuck off")

