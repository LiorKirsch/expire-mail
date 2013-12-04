from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
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
from django.views.decorators.csrf import csrf_exempt

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
        
    return ip

@never_cache
def getViewlimited(request, image_id):
    
    creatingUser =  False #request.session.get(image_id, False)
         
    clientAdd = get_client_ip(request)
    debug = request.GET.get('debug') is not None
    defaultImagePath = os.path.join(settings.PROJECT_ROOT, 'defaultImage.png')
    imageObject = LimitedViewImage.objects.get(image_id=image_id)
    theImage = imageObject.getImage(defaultImagePath, clientAdd, debug, creatingUser)

    response = HttpResponse(mimetype="image/png")
    response["Cache-Control"] = "no-cache, private, no-store, must-revalidate"
    response["x-content-type-options"] = "nosniff"
    response["x-xss-protection"] = "1; mode=block"
    response["X-Robots-Tag"] = "NOARCHIVE, noindex"
    theImage.save(response, "PNG")
    return response

@csrf_exempt
def addViewlimited(request):

    clientAdd = get_client_ip(request)
    
    if request.method == 'POST':
        json_data = simplejson.loads(request.raw_post_data)
        try:
            text = json_data['text']
        except KeyError:
            HttpResponseServerError("text key not found")
    else:
        text = request.GET.get('text')
        html = request.GET.get('html')
        
    
    image_id = generateRandomString(10)
    image_file_name = "%s.png" % image_id 
    fullPath =  os.path.join(settings.PROJECT_IMAGE_FOLDER, image_file_name)
    image_path = text2Image.transformText2(html, fullPath)
    
    imageObject = LimitedViewImage(image_id=image_id, image_file_path = image_path, text=html,creating_client_ip = clientAdd)
    imageObject.save()
    imageUrl = 'http://%s/viewlimited/%s' % ( request.get_host() ,image_id)
    response = sendObjectAsJson({"status":"success","image_id": image_id,"image_url": imageUrl}) 
    response['Access-Control-Allow-Origin']  = settings.XS_SHARING_ALLOWED_ORIGINS
    response['Access-Control-Allow-Methods'] = ",".join( settings.XS_SHARING_ALLOWED_METHODS )
    
#    request.session[image_id] = True
#    response['Access-Control-Allow-Headers'] = "Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, If-Modified-Since, X-File-Name, Cache-Control"
    return response

def generateRandomString(N):
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(N))
    
    
def sendObjectAsJson(myObjectDict):
    data = simplejson.dumps(myObjectDict, indent=4) 
    #print 'returning: %s' % data
    resp = HttpResponse(data, mimetype='application/json')
    resp['Access-Control-Allow-Headers'] = '*'
    return resp

    
