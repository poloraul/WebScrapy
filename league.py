from urllib import request,parse
from bs4 import BeautifulSoup            #Beautiful Soup是一个可以从HTML或XML文件中提取结构化数据的Python库
import os
from xml.dom.minidom import parseString
#构造头文件，模拟浏览器访问
def dataDeal(page_info):
    result = []
    soup = BeautifulSoup(page_info,'html.parser')
    teams = soup.find('div','data_wrap').find('ul').find_all('li')
    for team in teams:
        team_info = team.find_all('p')
        if len(team_info) != 7:
            continue
        rank = team_info[0].string
        team_name = team_info[1].string
        match = team_info[2].string
        win = team_info[3].string
        duc = team_info[4].string
        loss = team_info[5].string
        points =team_info[6].string
        result.append(','.join((rank,team_name,match,win,duc,loss,points)))
    return result
    
def plDateScrapy(year_to_year,league_type_id):
    url="http://sports1.sina.cn/global/scoreboard?league_type_id="+league_type_id+"&vt=4"
    # 请求 URL: http://sports1.sina.cn/global/scoreboard?league_type_id=4&vt=4
    #Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'}
    data =  {"year_to_year" : year_to_year}
    data = parse.urlencode(data).encode('utf-8')

    page = request.Request(url,headers=headers,data=data)
    page_info = request.urlopen(page).read().decode('utf-8')#打开Url,获取HttpResponse返回对象并读取其ResposneBody
    # print(page_info)
    return dataDeal(page_info)

path = "D:\\workspace\\WebScrapy\\league_info"
if not os.path.exists(path):
    os.mkdir(path)
for league_type_id in range(101):
    for yearBegin in range(2010,2019):
        yearEnd = yearBegin + 1
        year_to_year = str(yearBegin) + "-"+ str(yearEnd)
        file_name = str(league_type_id) + "-" + year_to_year+".csv"
        plresults = plDateScrapy(year_to_year,str(league_type_id))
        if len(plresults) > 1: 
            print(file_name)
            with open(os.path.join(path,  file_name),"w",encoding="utf-8") as file:       #在磁盘以只写的方式打开/创建一个名为 articles 的txt文件
                for plresult in plresults:
                    file.write(plresult+'\n')
    

#open()是读写文件的函数,with语句会自动close()已打开文件

