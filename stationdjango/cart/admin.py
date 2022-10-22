from django.contrib import admin

# Register your models here.

from cart import models

class OrdersModelAdmin(admin.ModelAdmin):
    list_display = ('id','guestName','guestMail','grandtotal','create_date')
    
class DetailModelAdmin(admin.ModelAdmin):
    list_display = ('detaiOrder','pname','dtotal')

admin.site.register(models.OrdersModel,OrdersModelAdmin)
admin.site.register(models.DetailModel,DetailModelAdmin)
