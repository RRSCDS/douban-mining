import sys
import urllib2
import time
import re
from lxml import html

def get_user_statuses(userid):
  
  reached_end = False
  i = 1
  saying_list = []
  while not reached_end:
    page_url = "http://www.douban.com/people/%s/statuses?p=%d" % (userid, i)
    
    # TODO: User login. Results limited to the first 10 pages without login
    response = urllib2.urlopen(page_url)
    page_html = response.read()
    tree = html.fromstring(page_html)
    
    statuses_element_list = tree.xpath('//*[@class="status-item"]')
    if len(statuses_element_list) < 20:
      reached_end = True
      print len(statuses_element_list)
    
    for s in range(len(statuses_element_list)):
      author_element = statuses_element_list[s].findall('.//*[@class="hd"]/*[@class="text"]/a')[0]
      author_link = author_element.get('href')
      author_id=None
      if re.search(r".*people/(.+?)/", author_link):
        author_id=re.search(r".*people/(.+?)/", author_link).group(1)
      if author_id == userid:
        blockquote_element_list = statuses_element_list[s].findall('.//*[@class="status-saying"]/blockquote')
        if blockquote_element_list:
          content='\n'.join([p.text for p in blockquote_element_list[0].findall('p')])
          saying_list.append(content)
    i += 1
    time.sleep(1)
  return saying_list

if __name__ == "__main__":
  userid = sys.argv[1]
  result_list = get_user_statuses( userid )
  for i in result_list:
    print i
