# coding : utf-8
import re
import time
import urllib
from selenium import webdriver


class Spider:

  def __init__(self, id):
    self.id = id

  def get(self):
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.add_argument('--headless')
    driver = webdriver.Firefox(firefox_options=fireFoxOptions)
    driver.get("https://www.zhihu.com/people/zhipengliu/following")
    time.sleep(10)
    data = driver.find_elements_by_class_name("List-item")
    for x in data:
      contentItem = x.find_element_by_class_name("ContentItem-main")
      contentItemImage = contentItem.find_element_by_class_name("ContentItem-image")
      img = contentItemImage.find_element_by_tag_name('img')
      imglink = img.get_property('src')
      contentItemHead = contentItem.find_element_by_class_name("ContentItem-head")
      userItemName = contentItemHead.find_element_by_class_name("UserItem-name")
      a = userItemName.find_element_by_class_name("Popover").find_element_by_tag_name('a')
      userIdLink = a.get_property('href')
      userId = re.match('people/.*', userIdLink)
      userName = a.text
      contentItemMeta = contentItemHead.find_element_by_class_name("ContentItem-meta")
      contentItemStatus = contentItemMeta.find_element_by_class_name("ContentItem-status")
      spans = contentItemStatus.find_elements_by_tag_name("span")
      sign = contentItemMeta.find_element_by_tag_name("div").find_element_by_tag_name("div").text
      if (len(spans)==3):
        follower = spans.pop().text
        articles = spans.pop().text
        answerNum = spans.pop().text
        print(answerNum)
        print(articles)
        print(follower)
      print(userId)
      print(userName)
      print(sign)
      print(userIdLink)
      print(imglink)
      print('')
    driver.quit()

    url = "127.0.0.1:8000/setData"
    data = userIdLink
    data = urllib.parse.urlencode(data)
    data = data.encode('utf-8')
    new_url = urllib.request.Request(url, data)
    response = urllib.request.urlopen(new_url)
    response = response.read()
    print(response.decode("utf8"))

spider = Spider('55')
spider.get()
