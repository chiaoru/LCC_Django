#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 22:29:06 2022

@author: kate
"""

# 宣告使用 Flask
from flask import Flask

# 初始化 Flask 物件
app = Flask(__name__)

# 建立主網址的路徑 / => 根目錄
# @app.route("/callback") => linebot 寫的
# app.route 要對應一個函數
@app.route("/")

def home():
    return "這個是首頁"

app.run() # 執行