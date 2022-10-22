from django.db import models

# Create your models here.

from django.utils import timezone # 可抓現在的時間

# 當 django 要使用圖片上傳的功能時，要先安裝 pip install pillow


class Photo(models.Model):
    # upload_to 圖片上傳後存放的位置
    # blank、null 這兩個是表示圖片欄位是否可以是空值 False(一定要填) -> 不能是空值 -> 一定要有值
    image = models.ImageField(upload_to='images/',blank=False,null=False)
    upload_date = models.DateField(default=timezone.now)
    