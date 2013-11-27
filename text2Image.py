# -*- coding: utf-8 -*-
import sys,os
from django.conf import settings

def transformText2(text, file_path):
    font = '%s/FreeSans.ttf' % settings.PROJECT_FONT_FOLDER
    color = 'black'
    background = 'white'
    size = '13'
    image = 'convert -background '+background+' -fill '+color+ ' -font "' + font +  '" -pointsize '+size+' label'+':"'+text+'" "'+file_path + '"'
    os.system(image)

    return file_path
