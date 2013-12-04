from django.db import models 
# Create your models here.

class Categories(models.Model):
	Title = models.CharField(max_length=40,null=False)  
	
	def __unicode__(self):  # Python 3: def __str__(self):
		return self.Title
  
class Entries(models.Model):  
	Title = models.CharField(max_length=100, null=False)
	Content = models.TextField(null=False)
	created = models.DateTimeField('date published')
	Category = models.ForeignKey(Categories) 

	def __unicode__(self):  # Python 3: def __str__(self):
		return self.Title  
 