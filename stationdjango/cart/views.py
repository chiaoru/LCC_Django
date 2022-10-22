from django.shortcuts import render, redirect
# redirect 導向

from cart.models import OrdersModel,DetailModel

from product.models import Goods

from django.http import HttpResponseRedirect

from member.models import Member

from django.utils.html import format_html

# 崁入 ECPay 的 SDK 設定
import os
basedir = os.path.dirname(__file__) # 抓取預設目錄位置

file = os.path.join(basedir, 'ecpay_payment_sdk.py')

import importlib.util
spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk",
    file
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
from datetime import datetime

# Create your views here.

cartlist = list() # 購物車內容

customName = "" # 客戶姓名
customPhone = "" # 客戶電話
customAddress = "" # 客戶地址
customEmail = "" # 客戶 email

orderTotal = 0 # 消費總額
goodsTitle = list() # 放入購物車的商品名稱


def cart(request): # 顯示購物車內容
    global cartlist # 設定全域變數
    allcart = cartlist
    total = 0


    # unit[0] 商品名稱
    # unit[1] 價格
    # unit[2] 數量
    # unit[3] 價格＊數量
    for unit in cartlist:
        total += int(unit[3])
    grandtotal = total + 100 # 運費 100 元
    return render(request, 'cart.html', locals())

# 加入至購物車中，並未將商品資訊寫入至資料庫中
def addtocart(request,ctype=None,productid=None):
    global cartlist
    
    if ctype=="add": # 將商品加入到購物車中
        product = Goods.objects.get(id=productid)
        flag = True # 預設購物車中沒有相同的商品，表示購物車在此商品不存在
        
        # 先檢查購物車中的商品是否有重複
        for unit in cartlist:
            if product.title == unit[0]: #表示有這個商品
                unit[2] = str(int(unit[2]) +1) # 數量在+1
                unit[2] = str(int(unit[3]) +product.price) # 累計金額
                flag = False # 表示商品之前已加入到購物車中
                break
            
        if flag: # 之前都沒有加入到購物車中
            templist = list()
            templist.append(product.title)
            templist.append(str(product.price))
            templist.append('1')
            templist.append(str(product.price))
            cartlist.append(templist) # 將一維資料加入 cartlist 成為二維陣列
            
        request.session['cartlist'] = cartlist # 將購物車內容存入至 Session 中
        return redirect('/cart/') # 跳轉到購物車的網址，之後再跳到上面 cart 的函式中
            
        
    elif ctype == "update":
        n = 0
        for unit in cartlist: # 修改 cartlist內的數量及總價
            unit[2] = request.POST.get('quantity'+str(n),'1') # 抓取qantity0..4，預設值為1(沒抓到時會以1帶入)
            unit[3] = str( int(unit[1]) * int(unit[2]) )
            n += 1
        request.session['cartlist'] = cartlist
        return redirect('/cart/')
    
    # redirect 直接掉到指定的網址，並沒有帶任何參數過去
    # render 跳至指定網址，並將要求(request) 將參數內容傳過去

    
    elif ctype == "empty":
        cartlist = list() # 指向空的串列
        request.session['cartlist'] = cartlist # 將空的串列再丟到session中
        return redirect('/cart/') # 並重新導向 購物車網頁
    
    elif ctype == 'remove':
        del cartlist[int(productid)] # 將放入的商品索引值刪除
        request.session['cartlist'] = cartlist
        return redirect('/cart/')
    
    
# 結帳 與cartorder.html 相關 
def cartorder(request): # 結帳
    # 結帳是要登入的，我們先不做登入
    
    # 補上登入功能，沒有登入不能結帳
    if 'isAlive' in request.session:
    
        
        global cartlist, customName, customPhone, customAddress, customEmail
        total = 0
        allcart = cartlist
        for unit in cartlist:
            total += int(unit[3])
        grandtotal = total + 100 # 運費
        
        userinfo = ''
        if userinfo == '':
            userinfo = Member.objects.get(email=request.session['myMail'])
            
            name = userinfo.name
            phone = userinfo.phone
            address = userinfo.address
            email = userinfo.email
        else:
        
        
            name = customName
            phone = customPhone
            address = customAddress
            email = customEmail
        
        
        return render(request, 'cartorder.html', locals())
    
    else:
        return HttpResponseRedirect('/login')
    
    
def cartok(request):
    
    if 'isAlive' in request.session:
    
        
        global cartlist, customName, customPhone, customAddress, customEmail
        
        global orderTotal, goodsTitle
        
        
        total = 0
        for unit in cartlist:
            total += int(unit[3])
        grandtotal = total + 100 # 運費
        
        orderTotal = grandtotal
        
        
        userinfo = Member.objects.get(email=request.session['myMail'])
      
        if customName != userinfo.name:
            customName = request.POST.get('cuName','')
            customPhone = request.POST.get('cuPhone','')
            customAddress = request.POST.get('cuAddress','')
            customEmail = request.POST.get('cuEmail','')
            payType = request.POST.get('payType','')
            
            unitorder = OrdersModel.objects.create(subtotal=total,shipping=100,grandtotal=grandtotal,guestName=customName,guestMail=customEmail,guestPhone=customPhone,guestAddress=customAddress,payType=payType)
        
        else:
            customName = userinfo.name
            customPhone = userinfo.phone
            customAddress = userinfo.address
            customEmail = userinfo.email
            payType = request.POST.get('payType','')
                
            unitorder = OrdersModel.objects.create(subtotal=total,shipping=100,grandtotal=grandtotal,guestName=customName,guestMail=customEmail,guestPhone=customPhone,guestAddress=customAddress,payType=payType)
            
            
        for unit in cartlist:
            goodsTitle.append(unit[0]) # 將要買的商品名稱新增至goodsTitle
            total = int(unit[1]) * int(unit[2])
            unitdetail = DetailModel.objects.create(detaiOrder=unitorder, pname=unit[0], unitprice=unit[1], quantity=unit[2], dtotal=total)
            
        orderid = unitorder.id # 取得訂單編號
        name = unitorder.guestName
        email = unitorder.guestMail
        cartlist = list()
        request.session['cartlist'] = cartlist
        
        if payType == '信用卡':
            return HttpResponseRedirect('/creditcard')
            # return render(request, 'paycredit.html',locals())
        
        else:return render(request, 'cartok.html',locals())
        
        
        
    
    else:
        
        total = 0
        for unit in cartlist:
            total += int(unit[3])
        grandtotal = total + 100 # 運費
        
        orderTotal = grandtotal
        
        customName = request.POST.get('cuName','')
        customPhone = request.POST.get('cuPhone','')
        customAddress = request.POST.get('cuAddress','')
        customEmail = request.POST.get('cuEmail','')
        payType = request.POST.get('payType','')
        
        # 新增資料至資料表中，models.py中的欄位名稱 = views.py中的變數名稱
        unitorder = OrdersModel.objects.create(subtotal=total,shipping=100,grandtotal=grandtotal,guestName=customName,guestMail=customEmail,guestPhone=customPhone,guestAddress=customAddress,payType=payType)
        
        for unit in cartlist:
            goodsTitle.append(unit[0]) # 將要買的商品名稱新增至goodsTitle
            total = int(unit[1]) * int(unit[2])
            unitdetail = DetailModel.objects.create(detaiOrder=unitorder, pname=unit[0], unitprice=unit[1], quantity=unit[2], dtotal=total)
            
        orderid = unitorder.id # 取得訂單編號
        name = unitorder.guestName
        email = unitorder.guestMail
        cartlist = list()
        request.session['cartlist'] = cartlist
        
        if payType == '信用卡':
            # ECPayCredit(request)
            return HttpResponseRedirect('/creditcard')
        
        else:
            return render(request, 'cartok.html',locals())
        
        
    
    
# 訂單查詢  
def cartordercheck(request):
    orderid = request.GET.get('orderid','')
    customEmail = request.GET.get('customEmail','')
    
    if orderid == '' and customEmail == '':
        firstsearch = 1
    
    else:
        order = OrdersModel.objects.filter(id=orderid).first() # 抓第一筆資料
        if order == None or order.guestMail != customEmail:
            notfound = 1
            
        else:
            details = DetailModel.objects.filter(detaiOrder=order)
        # 寫法二
        # order = models.OrdersModel.objects.filter(id=orderid,customEmail=customEmail)
        # if order == None:
        #   notfound = 1
        # else:
        #   details = models.DetailModel.objects.filter(detaiOrder=order)
        
    return render(request, 'cartordercheck.html', locals())
        
def ECPayCredit(request):
    
    global orderTotal, goodsTitle
    
    Title = ""
    for i in goodsTitle:
        Title += i + "#"
    
    order_params = {
        'MerchantTradeNo': datetime.now().strftime("NO%Y%m%d%H%M%S"),
        'StoreID': '',
        'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        'PaymentType': 'aio',
        'TotalAmount': orderTotal,
        'TradeDesc': 'Kate-Django-訂單測試',
        'ItemName': Title,
        'ReturnURL': 'https://www.lccnet.com.tw/lccnet',
        'ChoosePayment': 'Credit',
        'ClientBackURL': 'https://www.lccnet.com.tw/lccnet',
        'ItemURL': 'https://www.ecpay.com.tw/item_url.php',
        'Remark': '交易備註',
        'ChooseSubPayment': '',
        'OrderResultURL': 'https://www.lccnet.com.tw/lccnet',
        'NeedExtraPaidInfo': 'Y',
        'DeviceSource': '',
        'IgnorePayment': '',
        'PlatformID': '',
        'InvoiceMark': 'N',
        'CustomField1': '',
        'CustomField2': '',
        'CustomField3': '',
        'CustomField4': '',
        'EncryptType': 1,
    }
    
    goodsTitle = list() # 加入綠界後，將list 清空

    extend_params_1 = {
        'BindingCard': 0,
        'MerchantMemberID': '',
    }

    extend_params_2 = {
        'Redeem': 'N',
        'UnionPay': 0,
    }

    inv_params = {
        # 'RelateNumber': 'Tea0001', # 特店自訂編號
        # 'CustomerID': 'TEA_0000001', # 客戶編號
        # 'CustomerIdentifier': '53348111', # 統一編號
        # 'CustomerName': '客戶名稱',
        # 'CustomerAddr': '客戶地址',
        # 'CustomerPhone': '0912345678', # 客戶手機號碼
        # 'CustomerEmail': 'abc@ecpay.com.tw',
        # 'ClearanceMark': '2', # 通關方式
        # 'TaxType': '1', # 課稅類別
        # 'CarruerType': '', # 載具類別
        # 'CarruerNum': '', # 載具編號
        # 'Donation': '1', # 捐贈註記
        # 'LoveCode': '168001', # 捐贈碼
        # 'Print': '1',
        # 'InvoiceItemName': '測試商品1|測試商品2',
        # 'InvoiceItemCount': '2|3',
        # 'InvoiceItemWord': '個|包',
        # 'InvoiceItemPrice': '35|10',
        # 'InvoiceItemTaxType': '1|1',
        # 'InvoiceRemark': '測試商品1的說明|測試商品2的說明',
        # 'DelayDay': '0', # 延遲天數
        # 'InvType': '07', # 字軌類別
    }

    # 建立實體
    ecpay_payment_sdk = module.ECPayPaymentSdk(
        MerchantID='2000132',
        HashKey='5294y06JbISpM5x9',
        HashIV='v77hoKGq4kWxNNIS'
    )

    # 合併延伸參數
    order_params.update(extend_params_1)
    order_params.update(extend_params_2)

    # 合併發票參數
    order_params.update(inv_params)

    try:
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)

        # 產生 html 的 form 格式
        action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
        # action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
        html = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)
        #print(html)
        html = format_html(html) # 格式化 html 將文字的 html 轉換為網頁的 html
        return render(request, 'paycredit.html',locals())
        
    except Exception as error:
        print('An exception happened: ' + str(error))
        
        
        
def myorder(request):
    
    # 判斷 myMail 是否有在 session 中
    if "myMail" in request.session:
        
        # 抓取 session 的對應值
        email = request.session['myMail'] 
        isalive = request.session['isAlive'] 
        
        
        order = OrdersModel.objects.filter(guestMail=email) # 抓最後一筆資料
   
        #details = DetailModel.objects.filter(detaiOrder=order)
        
            
    return render(request, 'myorder.html', locals())

    

    
    
