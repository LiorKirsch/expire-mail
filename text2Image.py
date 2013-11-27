# -*- coding: utf-8 -*-
import sys,os

def transformText2(text, file_path):

    color = 'black'
    background = 'white'
    size = '13'
    image = 'convert -background '+background+' -fill '+color+' -pointsize '+size+' label'+':"'+text+'" "'+file_path + '"'
    os.system(image)

    return file_path
