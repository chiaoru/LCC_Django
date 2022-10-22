from django.db import models

# Create your models here.

class Tour(models.Model):
    title = models.CharField(max_length=100) # CharField 文字型態，最大長度到 254
    price = models.IntegerField() # IntegerField 整數型態
    discount = models.IntegerField()
    photo_url = models.CharField(max_length=254) 
    link = models.CharField(max_length=254)
    content = models.TextField() # TextField 可用來放有很多文字描述的欄位
    create_date = models.DateTimeField(auto_now_add=True)
        # DateTimeField(auto_now_add=True) 在後台建立資料時，時間不用自己填，但爬蟲抓資料時仍須自己填
    

    # 內部類別：此 class 類別需與上面對齊
    class Meta:
        db_table = 'travel'