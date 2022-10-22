#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 16:44:19 2022

@author: kate
"""


from .models import Member

obj1 = Member.objects.filter(email="test@gmail.com")

print(obj1)