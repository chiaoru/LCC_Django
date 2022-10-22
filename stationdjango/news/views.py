from django.shortcuts import render

# Create your views here.

from .models import News

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger 

def news(request):
    
    
    station = ''
    
    if 'station' in request.GET:
        
        station = request.GET['station']
        
        
        if (station == "三立新聞"):
            allnews = News.objects.filter(station="三立新聞").order_by('-create_date')
            
        elif (station == 'TVBS'):
            allnews = News.objects.filter(station='TVBS').order_by('-create_date')
            
        elif (station == '東森新聞'):
            allnews = News.objects.filter(station='東森新聞').order_by('-create_date')
          
        else:
            allnews = News.objects.all().order_by('-create_date')
            
    else:
        allnews = News.objects.all().order_by('-create_date')
            
    
    
    paginator = Paginator(allnews,10) # 10筆為一頁
    page = request.GET.get('page') # GET另一種寫法
    try:
        allnews = paginator.page(page)
    
    except PageNotAnInteger:
        allnews = paginator.page(1) # 不是整數，就跳到第一頁
    
    except EmptyPage:
        allnews = paginator.page(paginator.num_pages) # 跳至最後一頁

    
    return render(request, 'news.html', locals())




