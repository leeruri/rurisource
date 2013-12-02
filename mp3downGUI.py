# -*- coding: utf-8 -*- 

import re, httplib, urllib2, os, sys, datetime, time, thread
from Tkinter import *

class mp3down:
	conn = httplib.HTTPConnection("mp3.zing.vn") 
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/html"} 
	logFolder = "./logs/"

	def __init__(self, tkt):  
		if not os.path.exists(os.path.dirname(self.logFolder)):
			os.makedirs(os.path.dirname(self.logFolder)) 
		self.tkt = tkt

	def download(self, artist):  
		self.logFile = open(self.logFolder + str(datetime.date.today()) + '.log', 'ab')	
		cnt = 1 
		for page in range(1,30):
			try:  
				self.conn.request("POST", "/nghe-si/"+artist+"/bai-hat?p="+str(page), "", self.headers)   
				resonse = self.conn.getresponse()   
				result = resonse.read()   
				ff2 = re.findall('class="music-download _btnDownload" href="[^"]*"', result)  
				
				if len(ff2) == 0: break

				for ii in ff2:
					self.tkt.downloading()

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
						self.tkt.insertLog(msg)
						self.log(msg)
						continue

					f = open(file_name, 'wb')

					self.tkt.insertLog("Downloading\t%s\t%s" % (file_name, file_size))
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
							self.tkt.status(file_size_dl * 100. / file_size)
						else:
							self.tkt.status(file_size_dl * 100. / file_size)

					self.log(str(cnt)+'\t'+str(file_size)+'\t'+file_name)

					f.close()  
					cnt  = cnt + 1 
			except:
				self.tkt.insertLog("error")
				self.log("error")
				continue

		self.logFile.close()
		self.tkt.insertLog("===== END =====")
		self.tkt.stop() 
	
	def log(self, msg):
		t = time.localtime()
		self.logFile.write(self.strfill(t.tm_hour,2,'0') + ":" + self.strfill(t.tm_min,2,'0') + ":" + self.strfill(t.tm_sec,2,'0') + "\t" + msg + '\r\n') 
	
	def strfill(self, s, l, f):
		return str(f)*(l-len(str(s)))+str(s)

	def getArtist(self, artist):
		artist = artist.replace(' ','+')

		self.conn.request("GET", "/tim-kiem/bai-hat.html?q="+artist, "", self.headers)   
		result = self.conn.getresponse().read()   
		arry = re.findall('<a href="/nghe-si/[^"]*"', result) 
		if len(arry) > 0: 
			artist = (arry[0].replace('<a href="/nghe-si/','')).replace('"','')
		else:
			self.tkt.insertLog("'"+artist.replace('+',' ')+"' Does not exists")
			artist = ""

		return artist
		
class guiMp3down:
	def __init__(self):
		self.tkt = Tk()
		self.tkt.title('mp3 download')
		self.tkt.geometry('500x500+200+200')

		f = Frame(self.tkt)
		f.pack()

		lbl1 = Label(f,text='Artist name : ')
		lbl1.pack(side="left")

		self.etr1 = Entry(f)
		self.etr1.bind("<Key>",self.etr1_key)
		self.etr1.focus_force()
		self.etr1.pack(side="left")

		self.btn1 = Button(f,text='download',command=self.btn1_click)
		self.btn1.pack(side="right")

		self.txt1 = Text(self.tkt)
		self.txt1.pack()

		self.statusBar = Entry(self.tkt, width='70')
		self.statusBar.pack()

		self.tkt.mainloop()

		 
	def btn1_click(self):
		d = mp3down(self)
		artist = d.getArtist(self.etr1.get())
		
		if artist != "":
			thread.start_new_thread(d.download,(artist,))

	def etr1_key(self, event):
		if event.char != 0 and len(event.char) > 0 and ord(event.char) == 13:
			self.btn1_click()

	def insertLog(self, msg):
		self.txt1.insert(INSERT,msg + '\r\n' )

	def status(self, per):
		self.statusBar.delete(0, END)
		self.statusBar.insert(INSERT, str(int(per))+"%")
	
	def downloading(self):
		self.btn1.config(state="disabled")
		self.etr1.config(state="disabled") 
		
	def stop(self):
		self.btn1.config(state="disabled")
		self.etr1.config(state="disabled")
		self.txt1.config(state="disabled")
		self.statusBar.config(state="disabled")
		

g = guiMp3down()