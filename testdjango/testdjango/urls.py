from django.conf.urls import patterns, include, url

from django.contrib import admin
from blog import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testdjango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^category/(?P<title>\w+)/$', views.indexCategory),
	url(r'^date/(?P<year>\d{4})/$', views.indexYear), 
    url(r'^date/(?P<year>\d{4})/(?P<month>\d+)/$', views.indexMonth),
    url(r'^date/(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d+)/$', views.indexDay),    
	url(r'^admin/', include(admin.site.urls)),
    url(r'^write/', views.write), 
	url(r'^$', views.index), 
)
