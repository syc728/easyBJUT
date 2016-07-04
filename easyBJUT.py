# -*- coding: cp936 -*-
import sys
from bs4 import BeautifulSoup
import xlwt
import urllib2
import urllib
import cookielib
import time
import re
import os

reload(sys)
sys.setdefaultencoding( "utf-8" )
baseUrl = "http://gdjwgl.bjut.edu.cn/default2.aspx"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586"
cookie = cookielib.CookieJar()
headers = {'user-Agent': user_agent}
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))


def getC():
        try:
                CaptchaUrl = "http://gdjwgl.bjut.edu.cn/CheckCode.aspx"
                picture = opener.open(CaptchaUrl).read()

                local = open('image.jpg', 'wb')
                local.write(picture)
                local.close()
                return "success"
        except urllib2.URLError, e:
                if hasattr(e,"result"):
                        return e.result
                return "Error"


def login():
        try:
                page = urllib2.urlopen(baseUrl).read()
                soup = BeautifulSoup(page,"html.parser")
                tmp = soup.find('input',attrs={'name':'__VIEWSTATE'})
                viewstate = tmp['value']
                studentNo = raw_input("studentNo:")
                studentPass = raw_input("studentPass:")
                secretCode = raw_input("secretCode:")
                postData = urllib.urlencode({
                        '__VIEWSTATE': viewstate,
                        'txtUserName': studentNo,
                        'TextBox2': studentPass,
                        'txtSecretCode': secretCode,
                        'RadioButtonList1': '学生',
                        'Button1': '',
                        'lbLanguage': '',
                        'hidPdrs': '',
                        'hidsc': ''
                })
                request = urllib2.Request(baseUrl, postData, headers)
                result = opener.open(request)
                soup = BeautifulSoup(result.read(),"html.parser")
                error = soup.find_all('script')
                source = error[1].get_text().encode("gbk")
                
                secret_error = "验证码不正确"
                secret_res = source.find(secret_error)

                if secret_res != -1:
                        f = file("error.txt","w+")
                        f.writelines(secret_error)
                        f.close()
                        os._exit(0)

                print source
                pass_error = "密码错误"
                pass_res = source.find(pass_error)

                if pass_res != -1:
                        f = file("error.txt","w+")
                        f.writelines(pass_error)
                        f.close()
                        os._exit(0)

                user_error = "用户名不存在"
                user_res = source.find(user_error)

                if user_res != -1:
                        f = file("error.txt","w+")
                        f.writelines(user_error)
                        f.close()
                        os._exit(0)
                
                tmp = soup.find(id="xhxm")                
                studentName = str(tmp.string.decode('utf-8')[:-2])
                graduURL1 = "http://gdjwgl.bjut.edu.cn/xscjcx.aspx?xh=" + studentNo + "&xm=" + studentName + "&gnmkdm=N121605"
                referer = "http://gdjwgl.bjut.edu.cn/xs_main.aspx?xh=" + studentNo
                graduURL1 = urllib.quote(graduURL1,"?&/=:")

                headers_gra1 = {'Referer':referer,'user-Agent': user_agent,'Host':'gdjwgl.bjut.edu.cn',
                                    'Accept-Encoding': 'gzip, deflate','Connection': 'Keep-Alive'}
                headers_gra2 = {'Referer': graduURL1,'user-Agent': user_agent}
                
                request_gra1 = urllib2.Request(graduURL1, headers=headers_gra1)
                result = opener.open(request_gra1)
                soup = BeautifulSoup(result.read(),"html.parser")
                tmp = soup.find('input',attrs={'name':'__VIEWSTATE'})
                viewstate = tmp['value']
                postData_Gra = urllib.urlencode({
                        '__EVENTTARGET':'',
                        '__EVENTARGUMENT':'',
                        'btn_zcj':'历年成绩',
                        '__VIEWSTATE':viewstate,
                        'hidLanguage': '',
                        'ddLXN':'',
                        'ddLXQ':'',
                        'ddl_kcxz':''
                })
                request_gra2 = urllib2.Request(graduURL1, postData_Gra, headers_gra2)
                result = opener.open(request_gra2)
                return result.read()
        except urllib2.URLError, e:
                if hasattr(e,"code"):
                        return e.code

def writeIntoExcel():
        pageCode = login()
        # print pageCode
        
        soup = BeautifulSoup(pageCode, 'html.parser')

        table = soup.find("table", class_="datelist")
       
        book = xlwt.Workbook(encoding="utf-8", style_compression=0)
        sheet = book.add_sheet("score", cell_overwrite_ok=True)

        trs = table.find("tr")
        tds = trs.find_all("td")
        #print tds
        col = 0
        
        for i in range(len(tds)):
            if i == 0 or i == 1 or i == 3:
                sheet.write(0, col, tds[i].find('a').string.decode("utf-8"))
                col += 1
            if i == 4 or i == 6 or i == 7 or i == 8 or i == 9:
                sheet.write(0, col, tds[i].string.decode("utf-8"))
                col += 1

        row = 0
        trs = table.find_all("tr")
        for i in range(len(trs)):
            if i > 0:
                tds = trs[i].find_all("td")
                row += 1
                col = 0
                for j in range(len(tds)):
                    if j == 0 or j == 1 or j == 3 or j == 4 or j == 6 or j == 7 or j == 8 or j == 9:
                        sheet.write(row, col, tds[j].string.decode("utf-8"))
                        col += 1

        book.save("score.xls")
        print "EXCEL done!"
 
def getV():
        try:
                output = open("viewstate.txt","w")
                
                output.write(viewstate)
                output.close()
        except urllib2.URLError, e:
                if hasattr(e,"result"):
                        return e.result
                return "Error"

while True:
        order = raw_input("option: ")
        if order=='1':
                getC()
        else:
                writeIntoExcel()
                break
