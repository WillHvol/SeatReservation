# coding=UTF-8
import requests
import json
import urllib
# import urllib2
import sys
import ssl

host = 'https://imgurlocr.market.alicloudapi.com'
path = '/urlimages'
method = 'POST'
appcode = '88044ad755834576a306e5248bf039a8'#开通服务后 买家中心-查看AppCode
querys = ''
bodys = {}
url = host + path
# 或者base64

header = {"Authorization":'APPCODE ' + appcode}
def captcha(img):
    data = {'image': img}
    try:
        res = requests.post(url,data,headers=header)
    except :
        print("URL错误")
        exit()
    httpStatusCode = res.status_code
    answer = json.loads(res.text)["result"][0]["words"]
    if(httpStatusCode == 200):
        print("正常请求计费(其他均不计费)")
        print(res.text)
    else:
        httpReason = res.headers['X-Ca-Error-Message']
        if(httpStatusCode == 400 and httpReason == 'Invalid Param Location'):
            print("参数错误")
        elif(httpStatusCode == 400 and httpReason == 'Invalid AppCode'):
            print("AppCode错误")
        elif(httpStatusCode == 400 and httpReason == 'Invalid Url'):
            print("请求的 Method、Path 或者环境错误")
        elif(httpStatusCode == 403 and httpReason == 'Unauthorized'):
            print("服务未被授权（或URL和Path不正确）")
        elif(httpStatusCode == 403 and httpReason == 'Quota Exhausted'):
            print("套餐包次数用完")
        elif(httpStatusCode == 403 and httpReason == 'Api Market Subscription quota exhausted'):
            print("套餐包次数用完，请续购套餐")
        elif(httpStatusCode == 500 ):
            print("API网关错误")
        else:
            print("参数名错误 或 其他错误")
            print(httpStatusCode)
            print(httpReason)
    return answer

def wordCaptha():
    host = 'https://fscaptcha.market.alicloudapi.com'
    path = '/'
    method = 'POST'
    appcode = '你自己的AppCode'
    querys = ''
    bodys = {}
    url = host + path

    bodys['CaptchaAppId'] = '''199685167'''
    bodys['AppSecretKey'] = '''Efs3o2dsVdw'''
    bodys['RandStr'] = '''!@v32'''
    bodys['Ticket'] = '''Efs3o2dsVdwEfs3o2dsVdwEfs3o2dsVdwEfs3o2dsVdwEfs3o2dsVdw'''
    bodys['UserIp'] = '''53.70.12.13'''
    post_data = urllib.urlencode(bodys)
    # request = urllib2.Request(url, post_data)
    # request.add_header('Authorization', 'APPCODE ' + appcode)
    # # 根据API的要求，定义相对应的Content - Type
    # request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    # ctx = ssl.create_default_context()
    # ctx.check_hostname = False
    # ctx.verify_mode = ssl.CERT_NONE
    # response = urllib2.urlopen(request, context=ctx)
    # content = response.read()
    # if (content):
    #     print(content)