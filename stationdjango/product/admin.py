from django.contrib import admin

# Register your models here.

# 客製化後台的顯示欄位

from .models import Goods,GoodsItems

class GoodsAdmin(admin.ModelAdmin): # 如不做客製化，可只寫第16行
    list_display = ('platform','title','price') # 顯示資料表中的欄位
    

class ItemsAdmin(admin.ModelAdmin):
    list_display = ('id','itemName')
    
admin.site.register(Goods,GoodsAdmin)
admin.site.register(GoodsItems,ItemsAdmin)