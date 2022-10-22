from django.shortcuts import render

from .models import Goods, GoodsItems

from member.models import Member
from django.http import HttpResponseRedirect,HttpResponse

# 做分頁 EmptyPage 空白頁
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger 
# Create your views here.

def product(request):
    
    p = ''
    startPrice = ''
    endPrice = ''
    itemType = 0 # 預設為0
    
    # 網址中是否有參數名稱為：goods
    if "goods" in request.GET:
        
        p = request.GET['goods']
        startPrice = request.GET['startprice']
        endPrice = request.GET['endprice']
        itemType = request.GET['items']
        
        # 以防按上下頁時找不到內容出錯
        if len(itemType) == 0:
            itemType = 0
        
        # 使用者只搜尋商品名稱，並沒有輸入價格及種類
        if (len(p) > 0 and len(startPrice) == 0 and len(endPrice) == 0 and itemType == "0"):
            allGoods = Goods.objects.filter(title__contains=p).order_by('price')
            
        # 使用者只搜尋商品名稱，並沒有輸入價格
        elif (len(p) > 0 and len(startPrice) == 0 and len(endPrice) == 0 and itemType != "0"):
            allGoods = Goods.objects.filter(title__contains=p,items=itemType).order_by('price')
            
        # 使用者搜尋商品名稱、價格，種類沒選擇
        elif (len(p) > 0 and len(startPrice) > 0 and len(endPrice) > 0 and itemType == "0"):
            allGoods = Goods.objects.filter(title__contains=p,price__gte=startPrice,price__lte=endPrice).order_by('price')
            
        # 使用者搜尋商品名稱、價格、種類
        elif (len(p) > 0 and len(startPrice) > 0 and len(endPrice) > 0 and itemType != "0"):
            allGoods = Goods.objects.filter(title__contains=p,price__gte=startPrice,price__lte=endPrice,items=itemType).order_by('price')
        
        # 使用者只搜尋價格範圍，其他都沒有
        elif (len(p) == 0 and len(startPrice) > 0 and len(endPrice) > 0 and itemType == "0"):
            allGoods = Goods.objects.filter(price__gte=startPrice,price__lte=endPrice).order_by('price')
            
        # 使用者只搜尋價格範圍、種類
        elif (len(p) == 0 and len(startPrice) > 0 and len(endPrice) > 0 and itemType != "0"):
            allGoods = Goods.objects.filter(price__gte=startPrice,price__lte=endPrice,items=itemType).order_by('price')
            
        # 使用者只搜尋種類
        elif (len(p) == 0 and len(startPrice) == 0 and len(endPrice) == 0 and itemType != "0"):
            allGoods = Goods.objects.filter(items=itemType).order_by('price')
        
        # 如亂輸入，會給予所有的資料
        else:
            allGoods = Goods.objects.all().order_by('-id')
        
    else:
        allGoods = Goods.objects.all().order_by('-id')
        

    paginator = Paginator(allGoods,15) # 15筆為一頁
    page = request.GET.get('page') # GET另一種寫法
    try:
        allGoods = paginator.page(page)
    
    except PageNotAnInteger:
        allGoods = paginator.page(1) # 不是整數，就跳到第一頁
    
    except EmptyPage:
        allGoods = paginator.page(paginator.num_pages) # 跳至最後一頁
        

        
    content = {"goods":allGoods,"product":p,"startprice":startPrice,"endprice":endPrice,"items":itemType} # 用字典方式傳送
    return render(request, 'product.html',content)

    
    


