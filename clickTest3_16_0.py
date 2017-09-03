# encoding:UTF-8
# 迷之Header！！
# Author: 于霁
import urllib.request
import re
import urllib
from collections import deque
import xlrd

# 遍历基因数字
a = set(['28989', '84793', '84983'])

queue = deque()
for website in a:
    url = "http://www.genecards.org/Search/Keyword?queryString="+website
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'}
    try:
        req = urllib.request.Request(url=url, headers=headers)
        data = urllib.request.urlopen(req).read().decode('UTF-8')
        #print(data)
        linkre = re.compile('/cgi-bin/carddisp\.pl\?gene=.+keywords=[0-9]+')    # 匹配网页正则表达式
        for x in linkre.findall(data):
            queue.append(x)
            # print('加入队列 --->  ' + x)
            try:
                urlbase = "http://www.genecards.org"                       # base网址
                url2 = urlbase + x
                url3 = url2.replace("&amp;", "&")
                print(url3)                                                # 真实基因网址
                req2 = urllib.request.Request(url=url3, headers=headers)   # 访问基因名网页
                data2 = urllib.request.urlopen(req2).read().decode('UTF-8')
                # print(data2)

                genere = re.compile('keywords=[0-9]*')                     # 基因名正则表达式
                geneNumber = genere.findall(url3)
                # print(geneNumber[0])
                geneRealNumber = geneNumber[0].replace('keywords=', '')    # 真实数字
                # print(geneRealNumber)

                genere2 = re.compile('Entrez Gene: <a.*>[0-9]*</a>')
                geneNumber2 = genere2.findall(data2)
                # print(geneNumber2[0])
                genere3 = re.compile("[0-9]*</a")
                geneNumber3 = genere3.findall(geneNumber2[0])
                # print(geneNumber3[0])
                geneNumber4 = geneNumber3[0].replace('</a', '')
                # print(geneNumber4)   #
                if geneRealNumber == geneNumber4:
                    print(geneNumber4)
                genere4 = re.compile('gene=.*&')
                geneID = genere4.findall(url3)
                geneRealID = geneID[0].replace('gene=', '').replace('&', '')
                print(geneRealID)
            except:
                continue
    except:
        continue
