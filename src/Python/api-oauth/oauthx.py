# -*- coding: utf8 -*-
import urllib, urllib2
import json

# key and secret通过创建豆瓣app获得（无审核）
# http://developers.douban.com/apikey/
APIKEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
SECRET = 'xxxxxxxxxxxxxxxx'

CALLBACK_URL = 'http://www.douban.com'
GETTOKEN_URL = 'https://www.douban.com/service/auth2/token'

def getToken(code):

    postParams = {
        'client_id': APIKEY,
        'client_secret': SECRET,
        'redirect_uri': CALLBACK_URL,
        'grant_type': 'authorization_code',
        'code': code
    }

    # hearders可能非必要
    headers = {
        'Host': 'www.douban.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive'
    }

    req = urllib2.Request(
            url = GETTOKEN_URL,
            data = urllib.urlencode(postParams),
            headers = headers
    )

    # Get the access token
    try:
        r = urllib2.urlopen(req).read()
        print r
        return json.loads(r)['access_token']
    # Get detailed error msg if 400 bad request occurs:
    except urllib2.HTTPError as e:
        print 'Error: ' + e.read()
        raise SystemExit(e)


# Authorization code can be obtained manually using browser, 
#   see http://developers.douban.com/wiki/?title=oauth2 ("获取authorization_code")
# Each code can only be used once to get an access token (?)
# Tokens are relatively long-lived - no need to get a code every time


def apiTest(user, count=1, until_id=''):
    
    # Use old token from file if there is one, otherwise get new token
    f = open('token.txt', 'a+')
    tok = f.read()
    if len(tok) == 0:
        tok = getToken(raw_input('input code here:'))   # input code manually
        f.write(tok)
    f.close()
    print 'Current token:', tok

    # Reuqest url and headers
    url = 'https://api.douban.com/shuo/v2/statuses/user_timeline/'
    url = url + user + '?count=%s&until_id=%s'%(count, until_id)
    headers = {'Authorization': 'Bearer '+tok}

    # Get data
    try:
        req2 = urllib2.Request(url=url, headers=headers)
        resp2 = urllib2.urlopen(req2)
        rj = resp2.read()   # Json格式数据
        print rj
        r = json.loads(rj)  # 转换为python列表，每条广播表示为一个词典对象
        print '%s statuses loaded' % len(r)
    except urllib2.HTTPError as e:
        print 'Error: ' + e.read()
        raise SystemExit(e)



if __name__ == "__main__":
    apiTest('homeland', 5, '1605326442')

# Note that contrary to what douban api help says, until_id is NOT inclusive, 
#   i.e. only statuses with id < until_id will be loaded.