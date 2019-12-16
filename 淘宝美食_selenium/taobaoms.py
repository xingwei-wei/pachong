from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pyquery import PyQuery as pq

import re
'''
from config import *
import pymogo

#连接数据库
client=pymogo.MongoClient(MONGO_URL)
db=client[MONGO_DB]
'''
#browser = webdriver.Chrome()
#不打开浏览器的情况下运行
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
wait=WebDriverWait(browser,10)


#设置窗口大小
browser.set_window_size(1400,900)

#实现网页的自动进入
def search():
    #print('正在搜索')
    try:
        #请求网页的加载
        browser.get('https://www.taobao.com')
        #判断是否加载完成selenium.webdriver
        #提交框
        input=wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'#q'))
                                                )
        #提交按钮
        submit=wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')) 
            )
        input.send_keys(KEYWORD)
        submit.click()
        #总页数total
        total=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        get_products()
        return total.text
    except TimeoutException:
        return search()
    
    
#实现对某一页的操作  翻页操作
def next_page(page_number):
    #print('正在翻页',page_number)
    try:
        #第多少页
        input=wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > input')))      
        #确定按钮
        submit=wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))) 
        input.clear()
        #传入当前页码
        input.send_keys(page_number)
        #实现翻页操作
        submit.click()
        #判断翻页是否成功    
        wait.until(EC.text_to_be_present_in_element(By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number))
        get_products()
    except TimeoutException:
        next_page(page_number)
       
#分析网页内容
def get_products():
    #判断item是否加载成功
    wait.until(
        EC.presence_of_element_located(By.CSS_SELECTOR,'#mainsrp-itemlist .items .item'))
    #获取网页源代码,用pq解析网页源代码
    html=browser.page_source
    doc=pq(html)
    items=doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product={
                'iamges':item.find('.pic .imgLink').attr('src'),
                'price':item.find('.price').text(),
                'deal':item.find('.payNum').text()[:-3],
                'title':item.find('.title').text(),
                'shop':item.find('.shop').text(),
                'location':item.find('.location').text()
                    }
        print(product)
        #save_to_mongo(product)                                        
'''
#数据库的连接
def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('保存到MONGODB成功',result)
    except Exception:
        print('保存到MONGOBD失败',result)
'''
def main():
    try:
        total=search()
        #提取页数
        total=int(re.compile('\d*').search(total).group(1))
        for i in range(2,total+1):
            next_page(i)
    except Exception:
        print('出错！')
    finally:
        browser.close()   

if __name__=='__main__':
    main()
