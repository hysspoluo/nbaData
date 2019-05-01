import sqlite3

#初始化数据库表
#创建球队的表，每个表有球队这个赛季的所有赛程，这个是静态创建，不是动态创建，所以可以每次都运行
def createTables(teamlist):
    conn = sqlite3.connect('nba.db')
    print("连接数据库，没有则构建新的数据库表")
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
    cursor = conn.cursor()
    print("打开数据库，对表进行读写")
    #读取该表的数据条数SELECT COUNT(*) FROM table_name
    countString = 'select count(*) from %s'%(teamName)
    for game in Schedule_List:
        season = "2018-2019"
        insetString = 'insert into %s (season,type,time,home,result,guest,handicap,totle,analysis_link,euro_link)' \
                     'values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'\
        %(teamName,season,game['type'],game['time'],game['home'],game['result'],game['guest'],game['handicap'],game['totle'],game['analysis_link'],game['euro_link'])
        print(insetString)
        cursor.execute(insetString)
        conn.commit()
    conn.close()