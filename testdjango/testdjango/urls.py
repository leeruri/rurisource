from django.conf.urls import patterns, include, url

from django.contrib import admin
from blog import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testdjango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^category/(?P<title>\w+)', views.indexCategory),
	url(r'^category', views.index), 
    url(r'^date/(?P<year>\d{4})', views.indexYear), 
    url(r'^date/(?P<year>\d{4})/(?P<month>\d{2})', views.indexMonth),
    url(r'^date/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})', views.indexDay),    
	url(r'^date/', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^write/', views.write), 
	url(r'', views.index), 
	url(r'^(?P<what>\w+)/', views.page404), 
)
