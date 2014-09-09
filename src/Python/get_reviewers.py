	

    import sys
    import urllib2
    import time
    from lxml import html
     
    def get_reviewers(bookid, star=1):
      allstar10_list = []
      for tag in ['collections', 'doings', 'wishes']:
        reached_end = False
        i = 0
        while not reached_end:
          print "start %d" % i
          page_url = "http://book.douban.com/subject/%s/%s?start=%d" % (bookid, tag, i)
          response = urllib2.urlopen(page_url)
          page_html = response.read()
          tree = html.fromstring(page_html)
         
          reviews_element_list = tree.xpath('//*[@id="' + tag + '_tab"]//table')
          if len(reviews_element_list) < 20:
            reached_end = True
         
          reviewer_list = tree.xpath('//*[@id="' + tag + '_tab"]//table/tr/td/div[@class="pl2"]/a')
          reviewers = [ el.attrib['href'] for el in reviewer_list ]
         
          review_list  = tree.xpath('//*[@id="' + tag + '_tab"]//table/tr/td/p[@class="pl"]/span[last()]')
          reviews = [ el.attrib['class'] for el in review_list ]
         
          review_stars = "allstar%d0" % star
          allstar10_list.extend([reviewer for (reviewer,review) in zip(reviewers, reviews) if review == review_stars])
         
          i += 20
          time.sleep(1)
       
      return allstar10_list
     
    if __name__ == "__main__":
      bookid = sys.argv[1]
      allstar10_list = get_reviewers( bookid )
      for i in allstar10_list:
        print i

