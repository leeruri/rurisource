import re, httplib, urllib2, os, sys

class down:
	conn = httplib.HTTPConnection("mp3.zing.vn") 
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/html"} 

	def __init__(self): 
		pass

	def download(self, artist):  
		cnt = 1 
		for t in range(1,100):
			try:  
				self.conn.request("POST", "/nghe-si/"+artist+"/bai-hat?p="+str(t), "", self.headers)   
				r = self.conn.getresponse()   
				result = r.read()   
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
						print "Already exists file : %s" % (file_name)
						continue

					f = open(file_name, 'wb')

					print "Downloading: %s Bytes: %s" % (file_name, file_size)
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

					f.close()  
					cnt  = cnt + 1 
			except:
				print "Error"
				continue
	
	def getArtist(self):
		artist = ""
		while artist == "":
			artist = raw_input('Artist : ').replace(' ','+')

		self.conn.request("GET", "/tim-kiem/bai-hat.html?q="+artist, "", self.headers)   
		r = self.conn.getresponse()   
		result = r.read()    
		ff = re.findall('<a href="/nghe-si/[^"]*"', result) 
		if len(ff) > 0: 
			artist = ff[0].replace('<a href="/nghe-si/','')
			artist = artist.replace('"','')
		
		return artist

	
		
	



d = down()
d.download(d.getArtist())