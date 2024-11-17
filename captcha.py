# coding=utf-8

# Created by Deserts
# email: i@panjunwen.com
# site: https://panjunwen.com/
# date: 2016-08-20

from PIL import Image
from io import BytesIO
import math
import os
import pytesseract
import requests

class VectorCompare:
    def magnitude(self, concordance):
        total = 0
        for word, count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    def relation(self, concordance1, concordance2):
        # relevance = 0
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))






def captcha(token, username):
    url = "https://seat.ujn.edu.cn/cap/captcha/"+ token
    params ={
        "username"
    }


