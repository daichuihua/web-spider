import re
import os
import sys
import requests
from urllib import request
#request库用于获取网络资源 pip install requests

# #用requests.get获取网页
# def getHtml(url): #获取网址为url的网页
#     import requests
#     import sys
#     import chardet  #编码处理库 pip install chardet
#     fakeHeaders = {'User-Agent':   #用于伪装浏览器发送请求
#                    'Mozilla/5.0 (windows NT 10.0; win64; x64) \ AppleWebKit/537.36 (KHTML, like Gecko) \ '
#                    'chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.77',
#                    'Accept': 'text/html,application/xhtml+xml,*/*'}
#     try:
#             r=requests.get(url,headers = fakeHeaders)
#             ecd = chardet.detect(r.content)['encoding']
#             if ecd.lower()!= sys.getdefaultencoding().lower():
#                 r.encoding = ecd
#             else:
#                 r.encoding = r.apparent_encoding #确保网页编码正确
#             return r.text  #返回值是个字符串，内含整个网页内容
#     except Exception as e:
#             print(e)
#             return ""



#使用pyppeteer获得网页，pip install pyppeteer
#必须下载并安装特殊版本的谷歌浏览器chromium
def getHtml(url): #获取网址为url的网页
    import asyncio
    import pyppeteer as pyp
    async def asGetHtml(url):
        # browser = await pyp.launch(headless=False,
        #                            executablePath = "c:/tmp/chrome-win32/chrome.exe",
        #                            userdataDir = "c:/tmp")
        browser = await pyp.launch(headless=False)
        page = await browser.newPage()
        await page.setUserAgent('Mozilla/5.0 (Windows NT 6.1; \ Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \ chrome/78.0.3904.70 Safari/537.36')
        await page.evaluateOnNewDocument(
            '() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } } ) }'
        )
        await page.goto(url)
        text = await page.content()
        await  browser.close()
        return text
    m = asyncio.ensure_future(asGetHtml(url))
    asyncio.get_event_loop().run_until_complete(m)
    return m.result()

def getBaiduPicture(word,number):
    file_path = 'D:\\cats-pictures\\百度'

    if not os.path.exists(file_path):
        os.mkdir(file_path)
    m = 1 + 30 * (number-1)

    #下载n个百度图片搜来的关于word的图片保存到本地
    url = "https://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl="+str(number)+"&nc=1&ie=utf-8&word="
    url += word

    html = getHtml(url)
    pt = '\"thumbURL\":.*?\"(.*?)\"'   # 正则表达式，用于寻找图片网址

    # "thumbURL":"https://img1.baidu.com/it/u=716463119,473541077&fm=26&fmt=auto&gp=0.jpg",

    for x in re.findall(pt,html): #x就是图片url(网址)
        x = x.replace("%3A",":")  #有时 ‘：’ 表示成 %3A
        x = x.replace("%2F", "/")
        if not (x.lower().endswith(".jpg") or x.lower().endswith(".jpeg") or x.lower().endswith(".png") ) :
            continue #只获得后缀名是.jpg或者.png的图片文件
        try:
            print(x) #此行非必须
            r = requests.get(x,stream=True) #获得x对应的网络资源
            pos = x.rfind(".") # 图片内容写入文件
            f = open( file_path+'\\{0}{1}{2}'.format(word,m,x[pos:]),"wb")
            f.write(r.content)
            f.close()
            m +=1

        except Exception as e :
            print(str(m) + ".jpg下载失败")
            m += 1
        # if i >=n:
        #     break

# getBaiduPicture("猫",5000)
for number in range(1,11):
    getBaiduPicture("猫",number)