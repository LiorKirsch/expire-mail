# -*- coding: utf-8 -*-
import sys,os
from django.conf import settings

def transformText2(text, file_path):
    font = '%s/FreeSans.ttf' % settings.PROJECT_FONT_FOLDER
    color = 'black'
    background = 'white'
    size = '13'
    imageCommand = u''.join(( 'convert -background ',background,' -fill ',color,' -pointsize ',size,' label:"',text,'" "',file_path , '"' ))
    imageCommand = imageCommand.encode('utf-8').strip()
#    imageCommand = 'convert -background '+background+' -fill '+color+' -pointsize '+size+' label'+':"'+text+'" "'+file_path + '"'
    os.system(imageCommand)

    return file_path
