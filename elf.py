#!/usr/local/env python3
# -*- coding : utf-8 -*-
import requests
from bs4 import BeautifulSoup
import random
import shutil

class elf:
    def __init__(self):
        self.session = requests.Session()
        s = self.session

        url = "https://www.airelf.com.tw/login.aspx"
        r = s.get(url)

        soup = BeautifulSoup(r.text, 'html.parser')
        self.__VIEWSTATE = soup.find(id="__VIEWSTATE").get("value")
        self.__VIEWSTATEGENERATOR = soup.find(id="__VIEWSTATEGENERATOR").get("value")
        self.__EVENTVALIDATION = soup.find(id="__EVENTVALIDATION").get("value")

    def getCode(self, fileName):
        s = self.session
        url = "https://www.airelf.com.tw/ValidateImage.ashx?m=" + str(random.random)
        code = s.get(url, stream = True)
        with open(fileName + ".gif", 'wb') as out_file:
            shutil.copyfileobj(code.raw, out_file)
        del code

    def login(self, email, passwd, code):
        Json = {
            "__VIEWSTATE":self.__VIEWSTATE,
            "__VIEWSTATEGENERATOR":self.__VIEWSTATEGENERATOR,
            "__EVENTVALIDATION":self.__EVENTVALIDATION,
            "email":email,
            "txtPassword":passwd,
            "txtiden":code,
            "ctl00$MainContent$ButLogin":"會員登入"
        }
        s = self.session
        url = "https://www.airelf.com.tw/login.aspx"
        r = s.post(url,data=Json)

    def setPlace(self, num):
        num = int(num)
        s = self.session
        url = "https://www.airelf.com.tw/CN/index.aspx"
        if num <= 3 or num >= 0:
            r = s.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            thePlace = soup.find(id=num).a.string
            print(thePlace)

            theID = soup.find(id=str(num)+"_0").a["href"]
            self.palceID = theID.split("=")[1]

    def removeTab(self, string):
        string = string.replace("\t", "" )
        string = string.replace("\n", "" )
        string = string.replace("\r", "" )
        return string

    def getAddress(self):
        s = self.session
        url = "https://www.airelf.com.tw/CN/stationaddress.aspx?IDCompany=" + self.palceID
        r = s.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        theAddress = soup.findAll("td")[1].string
        theAddress = self.removeTab(theAddress)

        theZIP = soup.findAll("td")[3].string
        theZIP = self.removeTab(theZIP)

        theUser = soup.findAll("td")[5].string
        theUser = self.removeTab(theUser)

        theNumber = soup.findAll("td")[7].string
        theNumber = self.removeTab(theNumber)

        thePhone = soup.findAll("td")[9].string
        thePhone = self.removeTab(thePhone)

        theData = {
            "address":theAddress,
            "zip":theZIP,
            "user":theUser,
            "number":theNumber,
            "phone":thePhone
        }
        return theData
