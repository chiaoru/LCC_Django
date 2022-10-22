from django.shortcuts import render

# Create your views here.

from .models import Tour

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def tour(request):
    
    tour = ''
    
    
    if "tour" in request.GET:
        
        t = request.GET['tour']
        
        if (len(t) > 0):
            data = Tour.objects.filter(title__contains=t).order_by('price')
        else:
            data = Tour.objects.all().order_by('-id') 
    else:
    
        data = Tour.objects.all().order_by('-id') 
        # 表示所有的資料all()由大到小排序order_by('-id')
        # order_by 排序 id 是欄位名稱
        # order_by('id') 依 id 做遞增
        # order_by('-id') 依 id 做遞減
        
    paginator = Paginator(data,16)
    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    
    except PageNotAnInteger:
        data = paginator.page(1)
        
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
        
   
    content = {'tour':data}  
    return render(request,'travel.html',content)
    # locals() 將函式 tour 中的變數整個帶過去給 travel.html