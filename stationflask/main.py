#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 23:23:43 2022

@author: kate
"""

from flask import request, Flask, render_template
import db
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    sql = "select * from travel order by id desc limit 3"
    cursor = db.connect.cursor()
    cursor.execute(sql)
    db.connect.commit()
    travel = cursor.fetchall()
    
    sql = "select * from goods order by id desc limit 3"
    cursor = db.connect.cursor()
    cursor.execute(sql)
    db.connect.commit()
    goods = cursor.fetchall()
    
    return render_template("index.html", **locals())

@app.route("/product",methods=['GET'])
def goods():
    #productid
    p = request.args.get('goodsname')
    if p == None:
        sql = "select * from goods order by id desc"
    else:
        # '%{}%' 這個是關鍵字搜尋
        sql = "select * from goods where title like '%{}%' ".format(p)
        
    cursor = db.connect.cursor()
    cursor.execute(sql)
    db.connect.commit()
    result = cursor.fetchall() # 抓取查詢出來的全部資料 二維陣列
    return render_template("product.html",result = result)  

@app.route("/news",methods=['GET'])
def news():
    plat =request.args.get('station') # 帶入參數 platform=' '
    if plat == None:
        sql = "select * from news"
    else:
        sql = "select * from news where station='{}' order by id desc".format(plat)
    
    # http://127.0.0.1:5000/news?platform=tvbs -> 只顯示tvbs的新聞
    
    cursor = db.connect.cursor()
    cursor.execute(sql)
    db.connect.commit()
    result = cursor.fetchall()

    return render_template("news.html",result=result) # result=result 要寫才有內容

@app.route("/travel",methods=['GET'])
def travel():
    #travelid
    tid =  request.args.get('id')
    if tid == None:
        sql =  "select * from travel order by id desc"
    else:
        sql = "select * from travels where id={} ".format(tid)
        
    cursor = db.connect.cursor()
    cursor.execute(sql)
    db.connect.commit()
    result = cursor.fetchall()
    return render_template("travel.html",result=result)


@app.route("/message")
def message():
    return render_template("message.html")

@app.route("/addMessage",methods=['POST'])
def addMessage():
    if request.method== 'POST':
        modify_date = datetime.today()
        mdate = datetime.strftime(modify_date,"%Y-%m-%d")
        
        username = request.form.get('cuname')
        title = request.form.get('title')
        email = request.form.get('email')
        content = request.form.get('content')
        
        sql = "insert into contact(name, email, subject, content, create_date) values('{}','{}','{}','{}','{}') ".format(username,email,title,content,mdate)
        cursor = db.connect.cursor()
        cursor.execute(sql)
        db.connect.commit()
        
    return render_template("message.html")

@app.route("/display/<int:username>")
def displayName(username):
    if username == 100:
        return "Hello"
    elif username == 200:
        return "Go"
    else:
        sql = "select * from travel order by id desc limit 3"
        cursor = db.connect.cursor()
        cursor.execute(sql)
        db.connect.commit()
        travel = cursor.fetchall()
        
        sql = "select * from goods order by id desc limit 3"
        cursor = db.connect.cursor()
        cursor.execute(sql)
        db.connect.commit()
        goods = cursor.fetchall()
        
        return render_template("index.html", **locals())

#預設參數型態為：字串
@app.route('/show/<name>')
def show(name):
    return "Hello" + name

@app.route('/two/<one>/<other>')
def showOther(one,other):
    return "Hello" + one + "-" + other

if __name__ == "__main__":
    app.debug = True
    app.run()

