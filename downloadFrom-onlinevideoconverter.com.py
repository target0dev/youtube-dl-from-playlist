import requests, json, urllib, sys
from lxml import html

if len(sys.argv) < 2:
	sys.exit("[-] Error, no youtube video url. USAGE: script.py [YOUTUBE URL]")

url = 'https://www3.onlinevideoconverter.com/webservice'
#url = 'http://httpbin.org/post'
YOUTUBEURL = sys.argv[1]
YOUTUBEURL_ENCODED = urllib.quote_plus(YOUTUBEURL)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
    'Accept-Encoding': ', '.join(('gzip', 'deflate', 'br')),
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Referer': 'https://www.onlinevideoconverter.com/video-converter'
}


data={"function": "validate", "args[dummy]": "1", "args[urlEntryUser]": YOUTUBEURL_ENCODED, "args[fromConvert]": "urlconverter", "args[requestExt]": "mp4", "args[nbRetry]": "0", "args[videoResolution]": "-1", "args[audioBitrate]": "0", "args[audioFrequency]": "0", "args[channel]": "stereo", "args[volume]": "0", "args[startFrom]": "-1", "args[endTo]": "-1", "args[custom_resx]": "-1", "args[custom_resy]": "-1", "args[advSettings]": "false", "args[aspectRatio]": "-1"}

response = requests.post(url, headers=headers, data=data)

#sys.exit() #safety tag, remove before use.

res_validate_json = response.json()

SERVERID = res_validate_json['result']['serverId']
KEYHASH = res_validate_json['result']['keyHash']
YOUTUBETITLE = res_validate_json['result']['title']
PROCESSID = res_validate_json['result']['id_process']

data = {"function": "processVideo", "args[dummy]": "1", "args[urlEntryUser]": YOUTUBEURL_ENCODED, "args[fromConvert]": "urlconverter", "args[requestExt]": "mp4", "args[serverId]": SERVERID, "args[nbRetry]": "0", "args[title]": YOUTUBETITLE, "args[keyHash]": KEYHASH, "args[serverUrl]": "http%3A%2F%2Fsv98.onlinevideoconverter.com", "args[id_process]": PROCESSID, "args[videoResolution]": "-1", "args[audioBitrate]": "0", "args[audioFrequency]": "0", "args[channel]": "stereo", "args[volume]": "0", "args[startFrom]": "-1", "args[endTo]": "-1", "args[custom_resx]": "-1", "args[custom_resy]": "-1", "args[advSettings]": "false", "args[aspectRatio]": "-1"}

response = requests.post(url, headers=headers, data=data)
res_processvideo_json = response.json()
PAGEID = res_processvideo_json['result']['dPageId']
downloadURL = "https://www.onlinevideoconverter.com/success?id=" + PAGEID

response = requests.get(downloadURL, headers=headers)
t = html.fromstring(response.content)
videodownloadurl = t.xpath('//a[@class="download-button"]/@href')[1]

#print videodownloadurl

r = requests.get(videodownloadurl, headers=headers, stream=True)
with open('./result/'+YOUTUBETITLE+'.mp4', 'wb') as f:
     for chunk in r.iter_content(chunk_size=1024):
             if chunk:
                     f.write(chunk)
                     f.flush()

