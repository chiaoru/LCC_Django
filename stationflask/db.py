#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 23:11:27 2022

@author: kate
"""

import pymysql

dbsetting = {
    
    "host": "127.0.0.1",
    "port": 3306,
    "user": "lccuser",
    "password": "987654321",
    "db": "lccdemo",
    "charset": "utf8"
    
    }

connect = pymysql.connect(**dbsetting)