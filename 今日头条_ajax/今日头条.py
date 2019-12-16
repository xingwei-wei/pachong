from urllib.parse import urlencode
from requests.exceptions import RequestException
import json
from hashlib import md5
import os
import re
import pymongo
from bs4 import BeautifulSoup
import requests
from json.decoder import JSONDecodeError
'''
#开启多进程
form multiprocessing import Pool
from config import *

client=pymongo.MongoClient(MONGO_URL,connect=False)
db=client[MONDO_DB]
'''
def get_page_index(offest,keyword):
    data={
        'offest':offest,
       
        'formate':'json',
        'keyword':keyword,
        
        'autoload':'true',
        'count':'20',
        'cur_tab':3
    }
    url='http://www.toutiao.com/search_content/?'+ urlencode(data)
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None

def parse_page_index(html):
    try:
        data=json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')
    except JSONDecodeError:
        pass
        
def get_page_detail(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        print('请求详细页出错',url)
        return None
#解析url里的内容 var gellery里是json格式的数据
def parse_page_detail(html):
    soup=BeautifulSoup(html,'lxml')
    title=soup.select('title')[0].get_text()
    print(title)
    images_pattern=re.compile('var gallery=(.*?);',re.S)
    result=re.search(images_pattern,html)
    if result:
        #得到json串，并解析
        data=json.loads(result.group(1))
        if data and 'sub_images' in data.keys():
            sub_images=data.get('sub_images')
            images=[item.get(url) for item in sub_images]
            for image in inages: download_image(image)
            return{
                'title':title,
                'url':url,
                'images':images
                }           
    
'''
def save_to_mongo(result)
    if db[MONGO_TABLE].insert(result)
        print('存储到MONDODB成功'，result)
        return True
    return False

'''

def download_image(url):
    print('正在下载',url)
    try:
        response=request.get(url)
        if response.status_code==200:
            save_image(response.content)
            return response.text
        return None
    except RequestException:
        print('请求图片出错',url)
        return None

def save_image(content):
    #用md5文件名，防止重复
    file_path='{0}/{2}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open (file_path,'wb') as f:
            f.write(content)
            f.close()
def main():
    #html=get_page_index(0, '街拍')
    html=get_page_index(offset, KEYWORD)
    for url in parse_page_index(html):
        html=get_page_detail(url)
        if html:
            result=parse_page_detail(html,url)
            print(result)
       #    if result:save_to_mongo(result)


if __name__=='__main__':
   main()
   groups=[x*20 for x in range(GROUP_START,GROUP_END+1)]
   pool=Pool()
   pool.map(main,groups)
