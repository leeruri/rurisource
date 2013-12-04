# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = []

    operations = [
        migrations.CreateModel(
            fields = [(u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True),), ('Title', models.CharField(max_length=40),)],
            bases = (models.Model,),
            options = {},
            name = 'Categories',
        ),
        migrations.CreateModel(
            fields = [(u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True),), ('Title', models.CharField(max_length=100),), ('Content', models.TextField(),), ('created', models.DateTimeField(verbose_name='date published'),), ('Category', models.ForeignKey(to=u'blog.Categories', to_field=u'id'),)],
            bases = (models.Model,),
            options = {},
            name = 'Entries',
        ),
    ]
