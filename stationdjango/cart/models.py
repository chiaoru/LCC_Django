from django.db import models

# Create your models here.

# 訂單
class OrdersModel(models.Model):
    subtotal = models.IntegerField(default=0)
    shipping = models.IntegerField(default=0)
    grandtotal = models.IntegerField(default=0)
    guestName = models.CharField(max_length=100)
    guestMail = models.CharField(max_length=100)
    guestPhone = models.CharField(max_length=50)
    guestAddress = models.CharField(max_length=200)
    payType = models.CharField(max_length=20)
    create_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.guestName
   
# 明細
class DetailModel(models.Model):
    detaiOrder = models.ForeignKey('OrdersModel', on_delete = models.CASCADE)
        # ForeignKey 外來鍵：外部來的主鍵
        # on_delete = models.CASCADE 當 OrdersModel 內容被刪除時，明細也會一起被刪除
    pname = models.CharField(max_length=100)
    unitprice = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    dtotal = models.IntegerField(default=0)
    
    def __str__(self):
        return self.pname