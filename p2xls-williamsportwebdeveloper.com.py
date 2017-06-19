import requests, json, urllib, sys
from lxml import html

if len(sys.argv) < 2:
	sys.exit("[-] Error, no playlist ID. USAGE: script.py [YOUTUBE PLAYLIST ID]")

url = 'http://www.williamsportwebdeveloper.com/FavBackUp.aspx'
#url = 'http://httpbin.org/post'
YTPLID = sys.argv[1]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
    'Accept-Encoding': ', '.join(('gzip', 'deflate')),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Referer': 'http://www.williamsportwebdeveloper.com/FavBackUp.aspx',
    'Upgrade-Insecure-Requests': '1'
}

frontpage_res = requests.get(url, headers=headers)
frontpage_t = html.fromstring(frontpage_res.content)
EVENTARGET = frontpage_t.xpath('//input[@type="hidden" and @name="__EVENTTARGET"]/@value')[0]
EVENTARGUMENT = frontpage_t.xpath('//input[@type="hidden" and @name="__EVENTARGUMENT"]/@value')[0]
VIEWSTATE = frontpage_t.xpath('//input[@type="hidden" and @name="__VIEWSTATE"]/@value')[0]
VIEWSTATEGENERATOR = frontpage_t.xpath('//input[@type="hidden" and @name="__VIEWSTATEGENERATOR"]/@value')[0]

data={"__EVENTTARGET": EVENTARGET, "__EVENTARGUMENT": EVENTARGUMENT, "__VIEWSTATE": VIEWSTATE, "__VIEWSTATEGENERATOR": VIEWSTATEGENERATOR, "ctl00$ContentPlaceHolder1$txtPlaylist": YTPLID, "ctl00$ContentPlaceHolder1$btnSubmit": "Submit"}

print EVENTARGET, EVENTARGUMENT, VIEWSTATE, VIEWSTATEGENERATOR, YTPLID
reply_res = requests.post(url, headers=headers, data=data)
print reply_res.headers
reply_t = html.fromstring(reply_res.content)
filename = "./working/" + YTPLID + "-urllist"

try:
	tr_s = reply_t.xpath('//tr')
	for n in range(2, len(tr_s)):
		td_s = tr_s[n].xpath('.//td')
		if len(td_s[3].xpath('./text()')) == 0 or td_s[3].xpath('./text()')[0] != 'This video is unavailable.':
			with open(filename, 'a') as fnw:
				fnw.write(td_s[1].xpath('./text()')[0]+'\r\n')
			fnw.close()
	print "good"
	print filename
except:
	with open('debug'+YTPLID, 'a') as dw:
		dw.write(reply_res.content)
	dw.close()
	print "debug pls"
	print 'debug'+YTPLID
		


