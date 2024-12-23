# coding=utf-8
import json

# Created by Deserts
# email: i@panjunwen.com
# site: https://panjunwen.com/
# date: 2016-08-19

import requests
import time
from bs4 import BeautifulSoup
import re
import random
import datetime
import base64
# from captcha import captcha
from ocr import captcha
import DecodeAndEncode

header = {
    "accept":"application/json, text/plain, */*",
    "accept-encoding":"gzip, deflate, br, zstd",
    "accept-language":"zh-CN,zh;q=0.9,en;q=0.8",
    "authorization":"",
    "connection":"keep-alive",
    "host":"seat.ujn.edu.cn",
    "logintype":"PC",
    "referer":"https://seat.ujn.edu.cn/libseat/",
    "sec-ch-ua":'"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "sec-ch-ua-mobile":"?0",
    "sec-ch-ua-platform":'"Windows"',
    "sec-fetch-dest":"empty",
    "sec-fetch-mode":"cors",
    "sec-fetch-site":"same-origin",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "x-hmac-request-key":"",
    "x-request-date":"",
    "x-request-id":""
}
class SeatReservation(object):
    """ Seat class:
        @ param url: Leosys' URL, e.g.http://202.206.242.87/, notice the "/"
        !NOTICE: You'd better check the seat id (object.seat!=0)
                 when an object is created,
                 because if the param seat is invalid,
                 the variable seat of the object will be seted to 0.
    """
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        self.session.headers.update(header)
        self.reserveStatus = False
        self.date = self.getDate()
        self.token = ""

    def login(self, username=None, password=None):
        '''
            return a status code.
            0:  login successfully
            1:  wrong username
            2:  wrong password
            -1: network is unreachable
            !NOTICE:
            username and password MUST be provided the first time
        '''
        if username is not None:
            self.userInfo = {
                "username": username,
                "password": password,
                "captchaId": "",
                "answer": ""
            }
        captchaUrl = self.url + "auth/createCaptcha"
        loginUrl = self.url + "rest/auth"
        while True:
            try:
                captchaImg = self.session.get(captchaUrl)
                decodedImg = captchaImg.content.decode('utf-8')
                jsonImg = json.loads(decodedImg)
                self.userInfo["captchaId"] = jsonImg["captchaId"]
                base64_data = jsonImg["captchaImage"]
                image_data = base64.b64decode(base64_data.split(",")[1])
                with open("output.png", "wb") as file:
                    file.write(image_data)
                self.userInfo["answer"] = captcha(base64_data)
                decrypt = DecodeAndEncode.getKey("get")
                header["x-hmac-request-key"]=decrypt["requestKey"]
                header["x-request-date"]=str(decrypt["date"])
                header["x-request-id"]=decrypt["id"]

                print(self.session.headers)
                res = requests.get(url=loginUrl, params=self.userInfo, headers=header)

            except requests.exceptions.ConnectionError as e:
                print (e)
                return -1
            resText = json.loads(res.text)
            status = resText["status"]
            if status=="success":
                header["authorization"] = resText["data"]["token"]
                self.token = resText["data"]["token"]
                res = self.getCaptcha()
                capJson = json.loads(res.text)
                if(capJson["status"]=="OK"):
                    capToken = capJson["token"]
                    capImage = capJson["image"]
                    capWordImage = capJson["wordImage"]
                    capWordCount = capJson["wordCheckCount"]
                    capImageData = base64.b64decode(capImage.split(",")[1])
                    capWordImageData = base64.b64decode(capWordImage.split(",")[1])
                    with open("capImage.png", "wb") as file:
                        file.write(capImageData)
                    with open("capWordImage.png", "wb") as file:
                        file.write(capWordImageData)
                return 0
            # msg = re.findall('showmsg."(.*)",', res.text)
            else:
                code = resText["code"]
                if code == "31":
                    continue
        #     其他code情况

        return -1

    def loginStatusCheck(self, response=None):
        '''
            check if login successfully
        '''
        if response is None:
            response = self.session.get(self.url)
        text = json.loads(response.text)
        return text["status"] != "fail"

    def getCaptcha(self):
        url = "https://seat.ujn.edu.cn/cap/captcha/" + self.token
        params = {
            "username": self.userInfo["username"]
        }
        res = requests.post(url, params)
        return res

    # def checkCaptcha(self):


    def reserve(self, seat, start, end):
        '''
            reserve a seat.
            !NOTICE：
            @ param seat should be a string generated by getSeatID
            @ param start, end: start and end time of minutes.
                                e.g. 8:00-13:00, start = 480, end = 780
            return a status code.
            0: reserve successfully
            1: reached the limit, can't reserve
            2: the specific seat has been reserved by another user
            3: the system has not been opened up.
            4: the account is limitted
            -1: unkown error
        '''
        seatInfo = {
            "date": self.date,
            "seat": seat,
            "start": start,
            "end": end,
        }
        # post data and parse the response.
        try:
            res = self.session.post(url=(self.url + "selfRes"), data=seatInfo)
            soup = BeautifulSoup(res.text, "lxml")
            info = soup.dd.text
        except:
            info = None
        print ("post data: ", seatInfo)
        # deal with the response
        infoSlice = info[6:13]
        if info[:3] == u"凭证号" or infoSlice == u"已有1个有效预":
            self.reserveStatus = True
            return 0
        elif infoSlice == u"网上预约请求过":
            return 1
        elif infoSlice == u"预约失败，请尽":
            return 2
        elif infoSlice == u"系统可预约时间":
            return 3
        elif infoSlice == u"对不起, 您的":
            return 4
        else:
            return -1

    def getSeatID(self, room, seat):
        '''
            return a seat id(string) which is used in the system.
            if it returns 0, please make sure the room and seat
            number is right.
            @ param room: int
            @ param seat: int
        '''
        dt = self.date
        url = self.url + "mapBook/getSeatsByRoom?room=%d&date=%s" % (room, dt)
        res = self.session.get(url)
        soup = BeautifulSoup(res.text, "lxml")
        li_tags = soup.find_all("li")
        li_tags = [tag for tag in li_tags if tag.a is not None]
        for tag in li_tags:
            if int(tag.a.contents[0]) == seat:
                return tag.get("id")[5:]
        return 0

    def getDate(self):
        '''
            return a string of date of the next day,
            e.g. return "2016-08-20" when run this method on Aug 19.
        '''
        tm = time.localtime()
        date = str(tm[0]) + "-" + str(tm[1]) + "-" + str(tm[2] + 1)
        return date

    def myReservation(self):
        '''
            return a text about my reservation
        '''
        url = self.url + "history?type=SEAT"
        res = self.session.get(url)
        soup = BeautifulSoup(res.text, "lxml")
        return soup.dt.text + "\n" + soup.dd.text.strip()

    def getSeatList(self, room):
        '''
            return a list of all available seats.
            must provide a room id.
        '''
        rm = str(room)
        dt = self.date
        url = self.url + "mapBook/getSeatsByRoom?room=%s&date=%s" % (rm, dt)
        res = self.session.get(url)
        seatList = re.findall('>(\d+)</code', res.text)
        if seatList:
            return seatList
        else:
            return None

    def randomReserve(self, room, start, end):
        '''
            reserve a seat randomly.
        '''
        seats = self.getSeatList(room)
        if seats is not None:
            random.shuffle(seats)
            for seat in random:
                seat = self.getSeatID()
                status = self.reserve(seat, start, end)
                if status < 2:
                    return status
        return None

    def autoReserve(self, schedtime, room, seat, start, end, randRsv=False):
        '''
            reserve the specific seat after timeDelta seconds.
            @ param schedtime is a time, whose type is "datetime".
            If the param randRsv is True, it will randomly
             reserve a seat in the provided room.
        '''
        now = datetime.datetime.now()
        if now > schedtime:
            return None
        timeDelta = (schedtime - now).seconds
        time.sleep(timeDelta)
        # sleep timeDelta seconds then reserve
        # check account status
        if self.loginStatusCheck() is False:
            self.login()
        while True:
            status = self.reserve(seat, start, end)
            if status == 2 and randRsv:
                return self.randomReserve(room, start, end)
            if status != 3:
                break
        return status
