"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from food.views import food,index

from product.views import product

from tour.views import tour

from demotest.views import test

from cart.views import cart,addtocart,cartorder,cartok,cartordercheck,ECPayCredit,myorder

from contact.views import contact
from member.views import register,login,logout,forget,changepassword,member

from django.conf import settings

from django.conf.urls.static import static

from photos.views import index as photoindex

from sendmail.views import sendmail

from news.views import news

urlpatterns = [
    path('admin/', admin.site.urls),
    path('food/',food),
    path('',index),
    path('test/',test),
    path('product/',product),
    path('travel/',tour),
    path('cart/',cart),
    path('addtocart/<str:ctype>/',addtocart),
    path('addtocart/<str:ctype>/<int:productid>/',addtocart),
    path('cartorder/',cartorder),
    path('cartok/',cartok),
    path('cartordercheck/',cartordercheck),
    path('contact/',contact),
    path('register/',register),
    path('login/',login),
    path('logout/',logout),
    path('forget/',forget),
    path('changepassword/',changepassword),
    path('photos/',photoindex),
    path('sendmail',sendmail),
    path('creditcard/',ECPayCredit),
    path('member/',member),
    path('orderlist/',myorder),
    path('news/',news),
]

# <str:ctype> 在jango中帶參數

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    
    