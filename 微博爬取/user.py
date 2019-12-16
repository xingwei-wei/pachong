from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq

browser = webdriver.Chrome()
wait=WebDriverWait(browser,10)
#********************************************************************************  
#                  第二步: 访问个人页面http://weibo.cn/5824697471并获取信息  
#                                VisitPersonPage()  
#        编码常见错误 UnicodeEncodeError: 'ascii' codec can't encode characters   
#********************************************************************************  
  

def VisitPersonPage(user_id):  
  
    try:  
        global infofile  
        print u'准备访问个人网站.....'  
        #原创内容 http://weibo.cn/guangxianliuyan?filter=1&page=2  
        driver.get("http://weibo.cn/" + user_id)  
  
        #**************************************************************************  
        # No.1 直接获取 用户昵称 微博数 关注数 粉丝数  
        #      str_name.text是unicode编码类型  
        #**************************************************************************  
  
        #用户id  
        print u'个人详细信息'  
        print '**********************************************'  
        print u'用户id: ' + user_id  
  
        #昵称  
        str_name = driver.find_element_by_xpath("//div[@class='ut']")  
        str_t = str_name.text.split(" ")  
        num_name = str_t[0]      #空格分隔 获取第一个值 "Eastmount 详细资料 设置 新手区"  
        print u'昵称: ' + num_name   
  
        #微博数 除个人主页 它默认直接显示微博数 无超链接  
        #Error:  'unicode' object is not callable  
        #一般是把字符串当做函数使用了 str定义成字符串 而str()函数再次使用时报错  
        str_wb = driver.find_element_by_xpath("//div[@class='tip2']")    
        pattern = r"\d+\.?\d*"   #正则提取"微博[0]" 但r"(
.∗?
.∗?
)"总含[]   
        guid = re.findall(pattern, str_wb.text, re.S|re.M)  
        print str_wb.text        #微博[294] 关注[351] 粉丝[294] 分组[1] @他的  
        for value in guid:  
            num_wb = int(value)  
            break  
        print u'微博数: ' + str(num_wb)  
  
        #关注数  
        str_gz = driver.find_element_by_xpath("//div[@class='tip2']/a[1]")  
        guid = re.findall(pattern, str_gz.text, re.M)  
        num_gz = int(guid[0])  
        print u'关注数: ' + str(num_gz)  
  
        #粉丝数  
        str_fs = driver.find_element_by_xpath("//div[@class='tip2']/a[2]")  
        guid = re.findall(pattern, str_fs.text, re.M)  
        num_fs = int(guid[0])  
        print u'粉丝数: ' + str(num_fs)  
          
  
        #***************************************************************************  
        # No.2 文件操作写入信息  
        #***************************************************************************  
  
        infofile.write('=====================================================================\r\n')  
        infofile.write(u'用户: ' + user_id + '\r\n')  
        infofile.write(u'昵称: ' + num_name + '\r\n')  
        infofile.write(u'微博数: ' + str(num_wb) + '\r\n')  
        infofile.write(u'关注数: ' + str(num_gz) + '\r\n')  
        infofile.write(u'粉丝数: ' + str(num_fs) + '\r\n')  
        infofile.write(u'微博内容: ' + '\r\n\r\n')  
          
          
        #***************************************************************************  
        # No.3 获取微博内容  
        # http://weibo.cn/guangxianliuyan?filter=0&page=1  
        # 其中filter=0表示全部 =1表示原创  
        #***************************************************************************  
  
        print '\n'  
        print u'获取微博内容信息'  
        num = 1  
        while num <= 5:  
            url_wb = "http://weibo.cn/" + user_id + "?filter=0&page=" + str(num)  
            print url_wb  
            driver.get(url_wb)  
            #info = driver.find_element_by_xpath("//div[@id='M_DiKNB0gSk']/")  
            info = driver.find_elements_by_xpath("//div[@class='c']")  
            for value in info:  
                print value.text  
                info = value.text  
  
                #跳过最后一行数据为class=c  
                #Error:  'NoneType' object has no attribute 'groups'  
                if u'设置:皮肤.图片' not in info:  
                    if info.startswith(u'转发'):  
                        print u'转发微博'  
                        infofile.write(u'转发微博\r\n')  
                    else:  
                        print u'原创微博'  
                        infofile.write(u'原创微博\r\n')  
                          
                    #获取最后一个点赞数 因为转发是后有个点赞数  
                    str1 = info.split(u" 赞")[-1]  
                    if str1:   
                        val1 = re.match(r'
(.∗?)
(.∗?)
', str1).groups()[0]  
                        print u'点赞数: ' + val1  
                        infofile.write(u'点赞数: ' + str(val1) + '\r\n')  
  
                    str2 = info.split(u" 转发")[-1]  
                    if str2:   
                        val2 = re.match(r'
(.∗?)
(.∗?)
', str2).groups()[0]  
                        print u'转发数: ' + val2  
                        infofile.write(u'转发数: ' + str(val2) + '\r\n')  
  
                    str3 = info.split(u" 评论")[-1]  
                    if str3:  
                        val3 = re.match(r'
(.∗?)
(.∗?)
', str3).groups()[0]  
                        print u'评论数: ' + val3  
                        infofile.write(u'评论数: ' + str(val3) + '\r\n')  
  
                    str4 = info.split(u" 收藏 ")[-1]  
                    flag = str4.find(u"来自")  
                    print u'时间: ' + str4[:flag]  
                    infofile.write(u'时间: ' + str4[:flag] + '\r\n')  
  
                    print u'微博内容:'  
                    print info[:info.rindex(u" 赞")]  #后去最后一个赞位置  
                    infofile.write(info[:info.rindex(u" 赞")] + '\r\n')  
                    infofile.write('\r\n')  
                    print '\n'  
                else:  
                    print u'跳过', info, '\n'  
                    break  
            else:  
                print u'next page...\n'  
                infofile.write('\r\n\r\n')  
            num += 1  
            print '\n\n'  
        print '**********************************************'  
          
          
    except Exception,e:        
        print "Error: ",e  
    finally:      
        print u'VisitPersonPage!\n\n'  
        print '**********************************************\n'  
          
  

def main():
    search()
    result()
    browser.close()  
if __name__=='__main__':
    main()
