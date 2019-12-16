from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq

browser = webdriver.Chrome()
wait=WebDriverWait(browser,10)

def search():
    try:    
        #请求网页的加载
        browser.get('http://s.weibo.com')
        #判断是否加载完成selenium.webdriver
        #提交框
        input=wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#pl_searchHead > div > div > div > div.searchInp_box > div > input'))
            )
        #提交按钮
        submit=wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'#pl_searchHead > div > div > div > div.searchBtn_box > a')) 
                )
        input.send_keys('五一出行')
        submit.click()
    except TimeoutException:
        return search()
    

def result():      
  
    html=browser.page_source
    #获取网页的HTML信息
    doc=pq(html)
    items=doc('.feed_content.wbcon').items()
    for item in items:
        product={
                'user':item.find('.W_texta.W_fb').text(),              
                'comment':item.find('.comment_txt').text()
                    }
        print(product)
   

def main():
    search()
    result()
    browser.close()  
if __name__=='__main__':
    main()
