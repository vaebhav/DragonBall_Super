#!/usr/local/bin/python3

import requests
from bs4 import BeautifulSoup
#import re
import time
import datetime
#import unicode
#import pprint
#from selenium import webdriver
#from selenium.common.exceptions import TimeoutException

import sys, os, tempfile, logging

import urllib.request as urllib2
import urllib.parse as urlparse
'''
URL of the archive web-page which provides link to
all video lectures. It would have been tiring to
download each video manually.
In this example, we first crawl the webpage to extract
all the links and then download videos.
'''

logger = logging.getLogger('DragonBallSuper')
hdlr = logging.FileHandler('/var/tmp/DragonBallSuper.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

# specify the URL of the archive here
#archive_url = "https://watch-dbz39.funonline.co.in/dragon-ball-super-episode-55-english-dubbed/"
db_url = "https://watch-dbz40.funonline.co.in/dragon-ball-super-dubbed-episodes/"

#pp = pprint.PrettyPrinter()


def get_video_links():

    # create response object
	r = requests.get(db_url)
	file = "/Users/vaebhav/Downloads/DragonBallSuper/episodeCounter"
	eps_counterFile = open(file,'r+')
	if os.stat(file).st_size == 0:
		logger.error("Counter File is Zero Bytes")
		sys.exit()
	else:
		eps_Num = eps_counterFile.readline().strip()
		#sys.exit()

	# Chrome Driver Method
	#driver = webdriver.Chrome("/usr/local/lib/python3.6/site-packages/chromedriver_binary/chromedriver")
	#driver.set_page_load_timeout(5)
	#try:
	# 	driver.get(archive_url)
	# except TimeoutException:
    # never ignore exceptions silently in real world code
		# pass
	#driver.close()

	#Create Soup object to parse site
	soup = BeautifulSoup(r.content,'lxml-xml')

	for epsiodes in soup.findAll("div",class_="episode-list dbs"):
		#Getting the latest episode Number
		latest_epsiode_num = epsiodes.li.a['href'].split("/")[3].split("-")[4]
		latest_epsiode_link = "https://watch-dbz.funonline.co.in/vid/new/play.html?s=dragon-ball-super-dub&eno=" + latest_epsiode_num
		fileName = epsiodes.li.a['href'].split("/")[3].split("-")[0] + epsiodes.li.a['href'].split("/")[3].split("-")[1] + epsiodes.li.a['href'].split("/")[3].split("-")[2]
		fileName = fileName + "_" + latest_epsiode_num
		if latest_epsiode_num > eps_Num:
			eps_counterFile.seek(0)
			eps_counterFile.truncate()
			eps_counterFile.write(latest_epsiode_num)
			response = requests.get(latest_epsiode_link)
			iframe_soup = BeautifulSoup(response.content,'lxml-xml')
			#print(iframe_soup.findAll('div',class_="vw"))
			video_link = iframe_soup.source['src']
			#print(iframe_soup.source['src'])
			return video_link,fileName,latest_epsiode_num
			#print(epsiodes.li.a['href'].split("/")[3].split("-")[4])
		else:
			video_link = None
			fileName = None
			latest_epsiode_num = ""
			return video_link,fileName,latest_epsiode_num
			#print("Check Logic")
	#links = u''.join((str(item.contents) for item in soup.findAll("div",class_="episode-list dbs")))

	'''
	Method to Fetch Src using Chrome Driver Method
		##Fetching Video Wrapper class tags
		#links = u''.join((str(item) for item in soup.findAll("div",class_="videoWrapper")))

		# regex = r'src=.*'
		# match = re.search(regex,links)
		# src_link = match.group().split(" ")[0].replace("amp;","").split("\"")[1]
		# print(src_link)
		#response = requests.get(src_link)
		# iframe_soup = BeautifulSoup(response.content,'lxml-xml')
		# print(type(iframe_soup.findAll('div')))
		# video_link = iframe_soup.source['src']
		# print(iframe_soup.source['src'])#,class_="vw"))
	'''

def download_file(url,file,dest="/Users/vaebhav/Downloads/DragonBallSuper"):
	"""
	Download and save a file specified by url to dest directory,
	"""
	if file is None:
		logger.error("No File Returned")
		sys.exit()
	else:
		filename = file + ".mp4"

	if url is None:
		logger.error("No Url Found")
		sys.exit()

	if os.path.exists(filename):
		logger.error("Same File Already Present")
		sys.exit()


	u = urllib2.urlopen(url)

	scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
	#os.path.basename(path)
    #if not filename:
    #    filename = 'downloaded.file'

	if dest:
		filename = os.path.join(dest, filename)

	#print(filename)

	with open(filename, 'wb') as f:
		meta = u.info()
		meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
		meta_length = meta_func("Content-Length")
		file_size = None
		if meta_length:
			file_size = int(meta_length[0])/(1024*1024)
		logger.info("Downloading: {0} MegaBytes: {1}".format(url, file_size))

		file_size_dl = 0
		block_sz = 8192
		while True:
			buffer = u.read(block_sz)
			if not buffer:
				break

			file_size_dl += len(buffer)
			f.write(buffer)

			#status = "{0:16}".format(file_size_dl)
            #if file_size:
            #    status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
            #status += chr(13)
            #print(status, end="")
		print("Download Complete-->",filename)
		logger.info("Download Complete-->",filename)
		f.close()
	#return filename

def notify():
	title = "DragonBallSuper"
	episodeNum = open("/Users/vaebhav/Downloads/DragonBallSuper/episodeCounter",'r').readline()
	text = "New epidose - {0} downloaded".format(episodeNum)
	filename = "/Users/vaebhav/Downloads/DragonBallSuper/dragonballsuper_"+episodeNum+".mp4"
	if os.path.exists(filename):
		ft = os.path.getctime(filename)
		filedate =time.strftime("%Y-%m-%d", time.gmtime(ft))
		currentDate = datetime.datetime.now().strftime ("%Y-%m-%d")
		if filedate == currentDate:
		    os.system("""
		            	osascript -e 'display notification "{0}" with title "{1}"'
		             """.format(text, title))



if __name__ == "__main__":

    # getting video link
	(video_link,file,eNum) = get_video_links()
	# download video
	download_file(video_link,file)
	#notify when new episode downloaded
	notify()
