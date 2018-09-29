# coding : utf-8
import re
import time
import urllib
from selenium import webdriver
from urllib import request


class Spider:

  def __init__(self, id):
    self.id = id

  def httpData(self, data):
    response = request.urlopen(url='http://127.0.0.1:8000/setData', data=data, timeout=200)
    print(response.read().decode('utf-8'))
  def httpSave(self,data):
    response = request.urlopen(url='http://127.0.0.1:8000/giveKey', data=b"data="+data+b"", timeout=200)
    print(response.read().decode('utf-8'))
  def httpGet(self):
    response = request.urlopen(url='http://127.0.0.1:8000/getKey',data=b"data=" , timeout=200)
    # print(response.read().decode('utf-8'))
    return response.read().decode('utf-8')
  def get(self, url):
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.add_argument('--headless')
    driver = webdriver.Firefox(firefox_options=fireFoxOptions)
    driver.get(url)
    time.sleep(5)
    try:
      driver.find_element_by_class_name("NumberBoard-itemValue")
    except :
      return False
    next = driver.find_element_by_class_name("NumberBoard-itemValue").text
    data = driver.find_elements_by_class_name("List-item")
    result = b"data=["
    while (len(data)>0):
      contentItem = data.pop().find_element_by_class_name("ContentItem-main")
      contentItemImage = contentItem.find_element_by_class_name("ContentItem-image")
      img = contentItemImage.find_element_by_tag_name('img')
      imglink = img.get_property('src')
      contentItemHead = contentItem.find_element_by_class_name("ContentItem-head")
      userItemName = contentItemHead.find_element_by_class_name("UserItem-name")
      a = userItemName.find_element_by_class_name("Popover").find_element_by_tag_name('a')
      userIdLink = a.get_property('href')
      userId = re.search(r'((?<=people/)|(?<=/org/)).*', userIdLink).group()
      userName = a.text
      contentItemMeta = contentItemHead.find_element_by_class_name("ContentItem-meta")
      contentItemStatus = contentItemMeta.find_element_by_class_name("ContentItem-status")
      spans = contentItemStatus.find_elements_by_tag_name("span")
      sign = contentItemMeta.find_element_by_tag_name("div").find_element_by_tag_name("div").text
      sign = "tmp..."
      answerNum = 0
      articles = 0
      follower = 0
      # reg = '/[\u4e00 -\u9fa5]/g'
      if (len(spans) == 3):
          follower = spans.pop().text
          articles = spans.pop().text
          answerNum = spans.pop().text
      this = "{" + "'userName':'" + userName.replace(' ', '') + "','zhihuKey':'" + userId.replace(' ', '') + "','articles':'" + str(
          articles).replace(' ', '')+ "','followNum':'" + str(follower).replace(' ', '') + "','answerNum':'" + str(
          answerNum).replace(' ', '') + "','ownerSign':'" + sign.replace(' ', '') + "','imgLink':'" + imglink.replace(' ', '') + "'}"
      result = result + this.encode('utf8') + b","
    result = result + b"]"
    self.httpData(result)
    driver.quit()
    return next
  def get_by_zhihu_key(self,zhihu_key):
    base_url = "https://www.zhihu.com/people/" + zhihu_key+"/following?page="
    print(base_url)
    a = 1
    while True:
      result = spider.get(base_url + str(a))
      while result == False:
        print("失败获取")
        time.sleep(20)
        result = spider.get(base_url + str(a))
      a += 1
      if 20 * (a - 1) > int(result):
        break
  def spi(self, zhih_key):
    self.httpSave(zhih_key.encode('utf8'))
    self.get_by_zhihu_key(zhih_key)
    i= 0
    while i<10:
      new_key = self.httpGet()
      print(new_key)
      self.get_by_zhihu_key(new_key)
      i+=1
spider = Spider('55')
spider.spi("zhipengliu")
# spider.get_by_zhihu_key("lin-wei-pei")
