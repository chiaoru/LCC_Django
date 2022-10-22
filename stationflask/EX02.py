#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 22:50:39 2022

@author: kate
"""

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "這個是首頁"

@app.route("/news")
def news():
    return "這個是新聞頁"

@app.route("/product")
def goods():
    return "這個是產品頁"

app.run()