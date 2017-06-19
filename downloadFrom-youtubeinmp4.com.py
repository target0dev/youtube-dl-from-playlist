import requests, json, urllib, sys
from lxml import html

if len(sys.argv) < 2:
	sys.exit("[-] Error, no youtube video url. USAGE: script.py [YOUTUBE URL]")

#https://www.youtubeinmp4.com/youtube.php?video=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DsKofqwyuCaI

url = 'https://www.youtubeinmp4.com/youtube.php'
#url = 'http://httpbin.org/post'
#url = 'http://httpbin.org/get'
YOUTUBEURL = sys.argv[1]
#YOUTUBEURL_ENCODED = urllib.quote_plus(YOUTUBEURL)

url = 'https://www.youtubeinmp4.com/youtube.php'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Referer': 'https://www.youtubeinmp4.com/'
}


params={"video":YOUTUBEURL}

response = requests.get(url, params=params, headers=headers)
t = html.fromstring(response.content)
videodownloadurl = "https://www.youtubeinmp4.com/" + t.xpath('//a[contains(@class, "downloadButtons") and ./text()="Download MP4"]/@href')[0]
print "[i] Downloading video url: %s" % videodownloadurl

video_res = requests.get(videodownloadurl, headers=headers, stream=True)

#check response is it relavant
#status_code == 200, content-disposition exist, content-type == 'application/octet-stream'

video_res_STATUS_CODE = video_res.status_code
if video_res.status_code != 200:
	print "[-] Error: status code returns %s" % str(video_res.status_code)
	sys.exit()

if "Content-Disposition" not in video_res.headers.keys():
	print "[-] Error: response does not seems like file"
	print video_res.headers
	sys.exit()

if "Content-Disposition" not in video_res.headers.keys() or video_res.headers['Content-Type'] != 'application/octet-stream':
	print "[-] Error: response does not seems like file"
	print video_res.headers
	sys.exit()


#donwload the video
donesize = 0
filesize = int(video_res.headers['Content-length'])
noisytracker_counter = 0
noisytracker_trigger = 5000
video_filename = video_res.headers['Content-Disposition'].split(";")[1].split("=")[1].strip("\"")
print "[i] Video filename is %s" % video_filename
with open('./result/'+video_filename+'.mp4', 'wb') as f:
	for chunk in video_res.iter_content(chunk_size=1024):
		donesize = donesize + 1024
		noisytracker_counter = noisytracker_counter + 1
		if noisytracker_counter > noisytracker_trigger:
			noisytracker_counter = 0
			print "[i] ProgresS: %s ...... %s , %s" % (video_filename, str(donesize), str(filesize))
		if chunk:
			f.write(chunk)
			f.flush()
f.close()
video_res.close()
sys.exit()
