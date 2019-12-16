
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq

from tkinter import *
import pandas as pd
import numpy as np
import re
'''
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
        #alist=np.arange(0,len(product),1)
        #data=pd.DataFrame(product,index=alist,columns=['user','comment'])
        #print(data)
        #return product 
'''
#用户界面设置
#初始化
root=Tk()
root.title("微博信息采集")
Label(root,text="关注话题：").grid(row=1,column=1)
#text组件
text=Text(root,width=40,height=30)
text.grid(row=4,column=1,columnspan=2,rowspan=4,sticky=W+E+S+N)

#绑定变量
v1=StringVar()
e=Entry(root,textvariable=v1)
e.insert(0,"五一出行")
e.grid(row=1,column=2,padx=10,pady=5)

def show( ): 

    dt=result()
    #print(dt)
    #text.insert(END,dt)
    #text.see(END)
    #text.updata()



def close():
    browser.close()


#Message组件
#w=Message(root,text="hhh",width=30)
#w.grid(row=4,column=1)
'''
def main():
    search()
    result()
    #dt=result()
'''    
    #按键实现功能
Button(root,text="采集结果",width=10,command=show)\
        .grid(row=3,column=1,sticky=W,padx=10,pady=5)

Button(root,text="停止采集",width=10,command=close)\
        .grid(row=3,column=2,sticky=E,padx=10,pady=5)
'''
if __name__=='__main__':
    main()
'''







 
