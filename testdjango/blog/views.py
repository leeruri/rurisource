from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from datetime import datetime, timedelta 
from blog.models import Entries
from blog.models import Categories

page_index = 'blog/index.html'
page_404 = 'blog/page404.html'

def index(request): 
	entries = Entries.objects.order_by('-created')
	for e in entries:
		if expression: break
		if expression: continue
	else:
		
	page = page_index
	param = {'entries' : entries, 'common' : common(), }
	return render(request, page, param)


def indexCategory(request, title): 
	category = Categories.objects.filter(Title=title)
	if len(category) == 0: return render(request, page_404)
	
	entries = Entries.objects.filter(Category_id=category[0].id).order_by('-created')

	page = page_index
	param = {'entries' : entries, 'common' : common(), 'title' : category[0].Title, }
	return render(request, page, param) 

 
def indexYear(request, year): 	
	f_date =  datetime(int(year),1,1) 
	t_date =  datetime(int(year)+1,1,1)  
	entries = Entries.objects.filter(created__range=(f_date, t_date)).order_by('-created') 

	page = page_index
	param = {'entries' : entries, 'common' : common(), 'title' : year}
	return render(request, page, param) 


def indexMonth(request, year, month): 	
	yy = int(year)
	mm = int(month)
	f_date =  datetime(yy, mm, 1)
	if mm == 12:
		yy = yy + 1
		mm = 1
	else:
		mm = mm + 1
	t_date =  datetime(yy, mm, 1)  
	entries = Entries.objects.filter(created__range=(f_date, t_date)).order_by('-created')
	 
	page = page_index
	param = {'entries' : entries, 'common' : common(), 'title' : year+"/"+month}
	return render(request, page, param) 


def indexDay(request, year, month, day): 	
	f_date =  datetime(int(year), int(month), int(day)) 
	t_date =  f_date + timedelta(days = 1) 
	
	entries = Entries.objects.filter(created__range=(f_date, t_date)).order_by('-created')
	
	page = page_index
	param = {'entries' : entries, 'common' : common(), 'title' : year+"/"+month+"/"+day}
	return render(request, page, param) 

def write(request):
	if request.method == 'GET': 
		page = 'blog/write.html'
		param = {'common' : common(),}
	elif request.method == 'POST':

		e = Entries(Title = request.POST['Title'], Content = request.POST['Content'], created = datetime.now(), Category_id = request.POST['Category_id'])
		e.save()

		return index(request)
		
	return render(request, page, param) 

class common:
	def __init__(self): 		
		self.categories =  Categories.objects.order_by('-Title')
		self.history = Entries.objects.order_by('-created')
 
def page404(request, what):
	page = 'blog/page404.html'
	param = {}  
	return render(request, page, param) 
