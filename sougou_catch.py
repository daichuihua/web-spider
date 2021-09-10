"""
Tittle: sougou_catch(it is a web spider)
"""
import re
import os
from urllib import request
import requests
from bs4 import BeautifulSoup


def get_url(cate, N):
    """function to get the url"""
    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
        'cache-control': "no-cache",
        'postman-token': "fab4fce6-bc85-d134-e42e-a73628962c1f"
    }
    imgs = requests.get(
        'https://pic.sogou.com/pics?query=' + cate + '&mode='+str(N)+'&start=48&reqType=ajax&reqFrom=result&tn=0',
        headers=headers)
    html = BeautifulSoup(imgs.text)
    urls = re.findall("thumbUrl(.*?),", str(html), re.S)
    pic_urls = []
    for url in urls:
        print(url[3:-1])
        pic_urls.append(url[3:-1])
    return pic_urls


def download_pic(pic_urls, N):
    """function to download pic"""
    file_path = 'D:\\cats-pictures\\ + 圣女果 + /'
    print(file_path)
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    m = 0 + (N-1)*48
    for img_url in pic_urls:
        print('***** ' + str(m) + '.jpg *****' + '   Downloading...')
        try:
            request.urlretrieve(img_url, file_path + str(m) + '.jpg')
        except Exception as e:
            print(str(m) + ".jpg下载失败")
            print(e)
        m = m + 1
    print('Download complete!')


if __name__ == "__main__":
    Cate = '圣女果'
    for i in range(1, 10):
        Urls = get_url(Cate, i)
        download_pic(Urls, i)
