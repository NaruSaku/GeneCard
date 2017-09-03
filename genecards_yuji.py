# encoding:UTF-8
# Author:yuji
# Date:2017/3/16
import xlrd
import urllib.request
import re
import urllib
import xlwt

# 打开一个Excel文档
book = xlwt.Workbook(encoding="utf-8", style_compression=0)
sheet = book.add_sheet('1a', cell_overwrite_ok=True)                           # 为sheet取名

# 读取数据输入文件的Excel文档
data = xlrd.open_workbook('b.xlsx')
table = data.sheets()[0]
c = table.col_values(0)                                  # 将某一列中所有数字转化为一个list
count = 0                                                # 为循环计数
for i in c:                                             # 循环一个个数字
    j = str(i)
    k = j.replace('.0', '')                              # 将数字转化为字符
    url = "http://www.genecards.org/Search/Keyword?queryString="+k           # 搜索网址
    # 迷之header！！！！
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'}

    req = urllib.request.Request(url=url, headers=headers)
    data = urllib.request.urlopen(req).read().decode('UTF-8')
                                                                             # print(data)
    linkre = re.compile('/cgi-bin/carddisp\.pl\?gene=.+keywords=[0-9]+')    # 匹配网页正则表达式
    for x in linkre.findall(data):
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
        if int(geneRealNumber) < 100:
            sheet.write(count, 0, geneRealNumber)
            sheet.write(count, 1, 'bullshit')
            print(geneRealNumber)
            print('bullshit')

            break
        genere2 = re.compile('Entrez Gene: <a.*>[0-9]*</a>')
        geneNumber2 = genere2.findall(data2)
        # print(geneNumber2[0])
        genere3 = re.compile("[0-9]*</a")
        geneNumber3 = genere3.findall(geneNumber2[0])
        # print(geneNumber3[0])
        geneNumber4 = geneNumber3[0].replace('</a', '')
        # print(geneNumber4)   #
        genere4 = re.compile('gene=.*&')
        geneID = genere4.findall(url3)
        geneRealID = geneID[0].replace('gene=', '').replace('&', '')

        if geneRealNumber != geneNumber4:
            # print(geneNumber4)
             # print(geneRealID)
            sheet.write(count, 0, geneNumber4)
            sheet.write(count, 1, 'bullshit')
        else:
            print(geneNumber4)
            print(geneRealID)
            sheet.write(count, 0, geneNumber4)
            sheet.write(count, 1, geneRealID)
            break                                     # 跳出循环某个数字的网址循环
    count += 1
book.save("e:/gene2.xls")                              # 保存文件
