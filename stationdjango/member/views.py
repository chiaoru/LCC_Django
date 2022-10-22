from django.shortcuts import render

# Create your views here.

import hashlib
from .models import Member

from django.http import HttpResponseRedirect,HttpResponse


def register(request):
    
    msg = ""
    
    if 'cuname' in request.POST:
        
        username = request.POST['cuname']
        email = request.POST['email']
        password = request.POST['pwd']
        sex = request.POST['sex']
        tel = request.POST['phone']
        birthday = request.POST['birthday']
        address = request.POST['address']
        
        # 密碼加密
        password = hashlib.sha3_256(password.encode('utf-8')).hexdigest()
        
        obj = Member.objects.filter(email=email).count() # 筆數
        if obj == 0: # 表示這個 email 沒有在資料表中
            # 新增資料
            Member.objects.create(name=username,sex=sex,birthday=birthday,email=email,phone=tel,address=address,password=password)
            mag = "註冊成功！"
        else:
            msg = "此 Email 已經存在，請換一個！"
    return render(request, 'register.html')
        

def login(request):
    
    msg =""
    
    if 'email' in request.POST:
        email = request.POST['email']
        password = request.POST['password']
        password = hashlib.sha3_256(password.encode('utf-8')).hexdigest()
        
        # 確認帳密是否有在資料庫中
        obj = Member.objects.filter(email=email,password=password).count() # 計算筆數
        
        if obj > 0 : # 表示有這個使用者，且帳密都對
            request.session['myMail'] = email # 儲存session資料 
            request.session['isAlive'] = True
          
            # 加 Cookie 功能，若使用者禁用時，就會無效
            
            # 宣告 cookie 物件
            response = HttpResponseRedirect('/') # 指向根目錄 (index.html)
            
            # max_age = 1200 秒 -->只能存活 1200秒 ＝ 20 分鐘
            response.set_cookie('UserEmail',email,max_age=1200)
            
            
            return response # 切換至根目錄 (index.html)
            
        else:
            msg = "帳密錯誤，請重新輸入"
            return render(request, 'login.html',locals())
            # 當需要從views.py 傳值到 html 中時，需要加上 locals() ->會將定義的值 全部傳道 html中
        
    else:
        return render(request, 'login.html', locals())
    

def logout(request):
    del request.session['isAlive']
    del request.session['myMail']
    return HttpResponseRedirect('/login')

def forget(request):
    pass

def changepassword(request):
    msg = ''
    if "password" in request.POST:
        oldpwd = request.POST['password']
        repwd = request.POST['repassword']
        
        if oldpwd == repwd:
            changepwd = hashlib.sha3_256(oldpwd.encode('utf-8')).hexdigest()
            email = request.session['myMail']
            
            user = Member.objects.get(email=email)
            user.password = changepwd
            user.save()
            msg = "密碼變更完成"
            
        else:
            msg = "兩次密碼不匹對"
            
    return render(request, 'changepwd.html', locals())
    

def member(request):
    
    # 確認使用者是否已登入
    if "myMail" in request.session and "isAlive" in request.session:
        
        userinfo = Member.objects.get(email=request.session['myMail'])
        
        name = userinfo.name
        phone = userinfo.phone
        address = userinfo.address
        email = userinfo.email
        
        return render(request, 'member.html', locals())
    
    else:
        return HttpResponseRedirect('/login')
    

    