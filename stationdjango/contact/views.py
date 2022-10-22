from django.shortcuts import render

# Create your views here.

from .models import Message

from member import models

def contact(request):
    if 'cuname' in request.POST:
        cuname = request.POST['cuname']
        email = request.POST['email']
        title = request.POST['title']
        content = request.POST['content']
        
        obj = Message.objects.create(name=cuname,email=email,subject=title,content=content)
        obj.save()
        
    if "myMail" in request.session and "isAlive" in request.session:
        
        userinfo = models.Member.objects.get(email=request.session['myMail'])
        
        name = userinfo.name
        phone = userinfo.phone
        address = userinfo.address
        email = userinfo.email
        
        return render(request, 'contact.html', locals())
        
    return render(request, 'contact.html')
