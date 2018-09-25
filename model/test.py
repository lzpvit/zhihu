# coding : utf-8
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import Options
from bs4 import BeautifulSoup
import time

class Spider:

  def __init__(self, id):
    self.id = id

  def get(self):
    # driver = webdriver.PhantomJS()
    # Url = "https://www.zhihu.com/people/zhipengliu/following"
    # driver.get(Url)
    # time.sleep(10)
    # soup = BeautifulSoup(driver.page_source, 'lxml')
    # print(soup)
    # 创建chrome浏览器驱动，无头模式（超爽）
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.chrome(chorme_option=chrome_options)

    # 加载百度页面
    driver.get("https://www.zhihu.com/people/zhipengliu/following")
    time.sleep(10)

    # 获取页面名为wrapper的id标签的文本内容
    data = driver.find_element_by_class_name("ContentItem-main").text
    print(data)

    # 关闭浏览器
    driver.quit()


spider = Spider('55')
spider.get()
