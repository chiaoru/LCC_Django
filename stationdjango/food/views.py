from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from news.models import News
from product.models import Goods
from tour.models import Tour



def food(request):
    return render(request, 'food.html')


def index(request):
    
    # 這邊想要透過首頁來檢查 cookie 是否存在
    if 'UserEmail' in request.COOKIES:
        uemail = request.COOKIES['UserEmail']
        #uemail =  request.COOKIES.get('UserEmail')
        
    else:
        uemail = ''
        

    hotnews = News.objects.all().order_by('-id')[:3]
    hotgoods = Goods.objects.all().order_by('-id')[:3]
    hottour = Tour.objects.all().order_by('-id')[:3]
    
        
    return render(request, 'index.html', locals())
    

