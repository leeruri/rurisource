import re, httplib, urllib2, os, sys, datetime, time

class mp3down:
	conn = httplib.HTTPConnection("mp3.zing.vn") 
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/html"} 
	logFolder = "./logs/"
	def __init__(self):  
		if not os.path.exists(os.path.dirname(self.logFolder)):
			os.makedirs(os.path.dirname(self.logFolder)) 

	def download(self, artist):  
		self.logFile = open(self.logFolder + str(datetime.date.today()) + '.log', 'ab')	
		cnt = 1 
		for page in range(1,100):
			try:  
				self.conn.request("POST", "/nghe-si/"+artist+"/bai-hat?p="+str(page), "", self.headers)   
				resonse = self.conn.getresponse()   
				result = resonse.read()   
				ff2 = re.findall('class="music-download _btnDownload" href="[^"]*"', result)  
				for ii in ff2:
					ii = ii.replace('class=\"music-download _btnDownload\" href=\"','')
					ii = ii.replace('"', '')  
					i2 = ii.split("/")
					file_name = "./"+artist+"/"
					u = urllib2.urlopen(ii)
					if not os.path.exists(os.path.dirname(file_name)):
						os.makedirs(os.path.dirname(file_name))
					file_name = file_name+i2[5]+".mp3"

					meta = u.info()
					file_size = int(meta.getheaders("Content-Length")[0])
								  
					if os.path.exists(file_name) and os.path.getsize(os.path.abspath(file_name)) >= file_size:
						msg = "Already exists file : %s" % (file_name) 
						print msg
						self.log(msg)
						continue

					f = open(file_name, 'wb')

					print "Downloading\t%s\t%s" % (file_name, file_size)
					file_size_dl = 0
					block_sz = 81920
					while True:
						buffer = u.read(block_sz)
						if not buffer:
							break

						file_size_dl += len(buffer)
						f.write(buffer)
						status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
						status = status + chr(8)*(len(status)+1)

						# To distinguish displaying difference between dos and linux
						if sys.platform == 'win32':
							print status,
						else:
							print status

					self.log(str(cnt)+'\t'+str(file_size)+'\t'+file_name)

					f.close()  
					cnt  = cnt + 1 
			except:
				print "error"
				self.log("error")
				f.close()  
				continue

		self.logFile.close()
	
	def getArtist(self):
		artist = "" 
		while artist == "":
			artist = raw_input('Artist : ').replace(' ','+')

			self.conn.request("GET", "/tim-kiem/bai-hat.html?q="+artist, "", self.headers)   
			result = self.conn.getresponse().read()   
			arry = re.findall('<a href="/nghe-si/[^"]*"', result) 
			if len(arry) > 0: 
				artist = (arry[0].replace('<a href="/nghe-si/','')).replace('"','')
			else:
				print "'",artist,"' Does not exists"
				artist = ""

		return artist
	
	def log(self, msg):
		t = time.localtime()
		self.logFile.write(self.strfill(t.tm_hour,2,'0') + ":" + self.strfill(t.tm_min,2,'0') + ":" + self.strfill(t.tm_sec,2,'0') + "\t" + msg + '\r\n') 
	
	def strfill(self, s, l, f):
		return str(f)*(l-len(str(s)))+str(s)
		

d = mp3down()
d.download(d.getArtist())