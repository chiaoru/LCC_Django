from django.shortcuts import render, redirect

# Create your views here.

from .forms import UploadModelForm
from .models import Photo

def index(request):
    photos = Photo.objects.all() # 從資料表抓取目前存放在資料表中的資料
    form = UploadModelForm() # 生成物件，上傳圖片做表單驗證
    
    if request.method == "POST":
        form = UploadModelForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/photos')
        
    context = {
        'photos' : photos,
        'form' : form
        }
    
    return render(request, 'photos.html', locals())
    
