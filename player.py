from urllib import request,parse
from bs4 import BeautifulSoup            #Beautiful Soup是一个可以从HTML或XML文件中提取结构化数据的Python库
import os
from xml.dom.minidom import parseString
#构造头文件，模拟浏览器访问
def dataDeal(page_info):
    result = []
    soup = BeautifulSoup(page_info,'html.parser')
    player_name_ch = soup.find('dl','team_info_dl').find('dd').find('span','tid_span').string
    player_name_en = soup.find('dl','team_info_dl').find('dd').find_all('p')[1].string
    player_record = soup.find('div','list_player_record').find_all('span')
    birthday = player_record[0].string
    age = player_record[1].string
    country = player_record[2].string
    height = player_record[3].string
    weight = player_record[4].string
    belong_team = player_record[5].string
    position = player_record[6].string
    number_in_team = player_record[7].string
    player_info = ','.join((player_name_ch,player_name_en,birthday,age,country,height,weight,belong_team,position,number_in_team))
    return player_info
    
def playerScrapy(player_id):
    # The proxy address and port:
    proxy_info = { 'host' : '106.75.9.39','port' : 8080 }
    # We create a handler for the proxy
    proxy_support = request.ProxyHandler({"http" : "http://%(host)s:%(port)d" % proxy_info})
    # We create an opener which uses this handler:
    opener = request.build_opener(proxy_support)
    # Then we install this opener as the default opener for urllib2:
    request.install_opener(opener)

    url="http://sports1.sina.cn/global/player?player_id="+player_id+"&league_type_id=4&vt=4"
    # 请求 URL: http://sports1.sina.cn/global/scoreboard?league_type_id=4&vt=4
    #Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

    page = request.Request(url,headers=headers)
    page_info = request.urlopen(page).read().decode('utf-8')#打开Url,获取HttpResponse返回对象并读取其ResposneBody
    # print(page_info)
    return dataDeal(page_info)

path = "D:\\workspace\\WebScrapy\\player_info"
if not os.path.exists(path):
    os.mkdir(path)
file_name = "player_info.csv"
with open(os.path.join(path,  file_name),"w",encoding="utf-8") as file:
    for player_id in range(37500,40000):
        print(player_id)
        try:
            playerresult = playerScrapy(str(player_id))
        except AttributeError as err:
            continue
        print(playerresult)
        file.write(playerresult+'\n')

# playerScrapy("37572")