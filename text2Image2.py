# -*- coding: utf-8 -*-
import cairo
import pango
import pangocairo
import subprocess
from django.conf import settings


def transformText2(text, file_path):
    font = '%s/FreeSans.ttf' % settings.PROJECT_FONT_FOLDER
    color = 'black'
    background = 'white'
    size = '13'
    
    labelargument =  u''.join(('label:', text)).encode('utf-8').strip()
    commandLineArguments = ['convert','-background',background,'-fill',color,'-pointsize',size,labelargument,file_path ]
    subprocess.call(commandLineArguments)
    
    return file_path

def transformText(text, file_path, fontname="Sans"):
    
#    fontname = sys.argv[2] if len(sys.argv) >= 3 else "Sans"
#    text = sys.argv[1] if len(sys.argv) >= 2 else u"Some text"
    
    
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 320, 120)
    context = cairo.Context(surf)
    
    #draw a background rectangle:
    context.rectangle(0,0,320,120)
    context.set_source_rgb(1, 1, 1)
    context.fill()
    
    #get font families:
    
    font_map = pangocairo.cairo_font_map_get_default()
    families = font_map.list_families()
    
    # to see family names:
    print [f.get_name() for f in   font_map.list_families()]
    
    #context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
    
    # Positions drawing origin so that the text desired top-let corner is at 0,0
    context.translate(50,25)
    
    pangocairo_context = pangocairo.CairoContext(context)
    pangocairo_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
    
    layout = pangocairo_context.create_layout()
    font = pango.FontDescription(fontname + " 18")
    layout.set_font_description(font)
    
    layout.set_text(text)
    context.set_source_rgb(0, 0, 0)
    pangocairo_context.update_layout(layout)
    pangocairo_context.show_layout(layout)
    
    with open(file_path, "wb") as image_file:
        surf.write_to_png(image_file)
        
    return file_path
