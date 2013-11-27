from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import logout
from django.utils import simplejson 
from models import LimitedViewImage
from random import randrange
import math
import cStringIO
import urllib, urllib2
import Image as PilImage 
from django.conf import settings
from django.views.decorators.cache import never_cache
import random, string
import text2Image
import os

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
        
    host = request.META.get('REMOTE_HOST')
    return (ip,host)

@never_cache
def getViewlimited(request, image_id):
    (clientAdd,clientHost) = get_client_ip(request)
    
    defaultImagePath = os.path.join(settings.PROJECT_ROOT, 'defaultImage.png')
    imageObject = LimitedViewImage.objects.get(image_id=image_id)
    theImage = imageObject.getImage(defaultImagePath, clientAdd)

    response = HttpResponse(mimetype="image/png")
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    theImage.save(response, "PNG")
    return response


def addViewlimited(request):

    (clientAdd,clientHost) = get_client_ip(request)
    text = request.GET.get('text')
    image_id = generateRandomString(10)
    image_file_name = "%s.png" % image_id 
    fullPath =  os.path.join(settings.PROJECT_IMAGE_FOLDER, image_file_name)
    image_path = text2Image.transformText2(text, fullPath)
    
    imageObject = LimitedViewImage(image_id=image_id, image_file_path = image_path, text=text,creating_client_ip = clientAdd)
    imageObject.save()
    imageUrl = 'http://%s/viewlimited/%s' % (settings.SERVER_EXTERNAL_URL ,image_id)
    return sendObjectAsJson({"status":"success","image_id": image_id,"image_url": imageUrl})

def generateRandomString(N):
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(N))
    
    
def sendObjectAsJson(myObjectDict):
    data = simplejson.dumps(myObjectDict, indent=4) 
    #print 'returning: %s' % data
    resp = HttpResponse(data, mimetype='application/json')
    resp['Access-Control-Allow-Headers'] = '*'
    return resp

    
