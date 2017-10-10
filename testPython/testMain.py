# coding=UTF-8
import re
import string
import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
from lxml import etree

reload(sys)
sys.setdefaultencoding('utf-8')
user_id = 1714904297

cookie = {"Cookie": "_T_WM=1c6f3f68a97fc5fcbcebbaad001e5463"}
url = 'http://weibo.cn/u/%d?filter=1&page=1'%user_id

print "url is %s" %url

movieurl = 'https://movie.douban.com/cinema/nowplaying/beijing/'

html = requests.get(url, cookies = cookie).content
selector = etree.HTML(html)
pageNum = 50
#undata = (selector.xpath('//div[@id="pagelist"]'))

result = ""
urllist_set = set()
word_count = 1
image_count = 1

for page in range(1,pageNum+1):
    url = 'http://weibo.cn/u/%d?filter=1&page=%d'%(user_id,page)
    lxml = requests.get(url, cookies = cookie).content
    selector = etree.HTML(lxml)
    content = selector.xpath('//span[@class="ctt"]')
    for each in content:
        text = each.xpath('string(.)')
        if word_count >= 4:
            text = "%d :"%(word_count-3) +text+"\n\n"
        else :
            text = text+"\n\n"
        result = result + text
        word_count += 1
        soup = BeautifulSoup(lxml, "lxml")
        urllist = soup.find_all('a',href=re.compile(r'^http://weibo.cn/mblog/oripic',re.I))
        first = 0
        for imgurl in urllist:
            urllist_set.add(requests.get(imgurl['href'], cookies = cookie).url)
            image_count +=1

fo = open("/Volumes/mydata/%s"%user_id, "wb")
fo.write(result)
word_path=os.getcwd()+'/%d'%user_id
print "dsd"

link = ""
fo2 = open("/Volumes/mydata/%s_imageurls"%user_id, "wb")
for eachlink in urllist_set:
    link = link + eachlink +"\n"
fo2.write(link)
print 'pic'

if not urllist_set:
    print 'pic'
else:
    image_path=os.getcwd()+'/weibo_image'
if os.path.exists(image_path) is False:
        os.mkdir(image_path)
x=1
for imgurl in urllist_set:
    temp= image_path + '/%s.jpg' % x
    print u'正在下载第%s张图片' % x
    try:
        urllib.urlretrieve(urllib2.urlopen(imgurl).geturl(),temp)
    except:
        print "该图片下载失败:%s"%imgurl
x+=1

print u'原创微博爬取完毕，共%d条，保存路径%s'%(word_count-4,word_path)
print u'微博图片爬取完毕，共%d张，保存路径%s'%(image_count-1,image_path)
