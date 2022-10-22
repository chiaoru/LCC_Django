from django.db import models

# Create your models here.

class News(models.Model):
    station = models.CharField(max_length=30)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=30)
    photo_url = models.CharField(max_length=255)
    news_url = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'news'

"""
未做
class NewsCategory(models.Model):
    categoryName = models.CharField(max_length=30)
    
    class Meta:
        db_table = 'newsCategory'
    
"""