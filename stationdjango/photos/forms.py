#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 20:29:18 2022

@author: kate
"""

from django import forms

from .models import Photo

class UploadModelForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image',)
        widgets ={
            'image': forms.FileInput(attrs={'class':'form-control-file'})
            }