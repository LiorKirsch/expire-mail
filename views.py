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


@never_cache
def getViewlimited(request, image_id):
    defaultImagePath = os.path.join(settings.PROJECT_ROOT, 'defaultImage.png')
    imageObject = LimitedViewImage.objects.get(image_id=image_id)
    theImage = imageObject.getImage(defaultImagePath)

    response = HttpResponse(mimetype="image/png")
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    theImage.save(response, "PNG")
    return response


def addViewlimited(request):

    
    text = request.GET.get('text')
    image_id = generateRandomString(10)
    image_file_name = "%s.png" % image_id 
    fullPath =  os.path.join(settings.PROJECT_IMAGE_FOLDER, image_file_name)
    image_path = text2Image.transformText2(text, fullPath)
    
    imageObject = LimitedViewImage(image_id=image_id, image_file_path = image_path)
    imageObject.save()
    imageUrl = 'http://expired-mail.liorkirsch.webfactional.com/viewlimited/%s' % image_id
    return sendObjectAsJson({"status":"success","image_id": image_id,"image_url": imageUrl})

def generateRandomString(N):
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(N))
    
    
def sendObjectAsJson(myObjectDict):
    data = simplejson.dumps(myObjectDict, indent=4) 
    #print 'returning: %s' % data
    resp = HttpResponse(data, mimetype='application/json')
    resp['Access-Control-Allow-Headers'] = '*'
    return resp









def base(request):
    
    if  request.user.is_authenticated():
        username = request.user.get_full_name()
    else:
        username = None
        
    my_data_dictionary = {'username':username}
    return render_to_response('index.html',
                          my_data_dictionary,
                          context_instance=RequestContext(request))

def LogoutRequest(request):
    logout(request)
    return HttpResponseRedirect('/')

#def logout_view(request):
#    logout(request)
#    return HttpResponseRedirect("/")
#def getPhotosJson(request):
#    photo_list = []
#    if not request.user.is_authenticated():
#        return HttpResponseRedirect('/login/?next=%s' % request.path)
#    else:
#        userInstance = UserSocialAuth.objects.filter(user=request.user).get()
#        photo_list = getFacebookPhotos(userInstance)
#        
#    return sendObjectAsJson(photo_list)

        
def somePrivateMethod(request):
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)
    else:
        userInstance = UserSocialAuth.objects.filter(user=request.user).get()
        access_token = userInstance.tokens['access_token']
        
        graphObject = Graph(access_token)
        facebookPhotos = graphObject['me'].photos(limit=20)
        
        returnObject = {'first_name':request.user.first_name,'last_name': request.user.last_name ,'access_token': access_token, 'status':'success','photos': facebookPhotos}
        response = sendObjectAsJson(returnObject)
    return response


def getFacegetImage(request):
    response = {};
    if (request.GET.has_key('urls')):
        imageUrl = request.GET.get('urls')
        response = getFace(imageUrl)
    
    return sendObjectAsJson(response)
        
def placeImageWithMashape(origPilImage,origImageUrl,imageHat, personIndex):
##################MASHAPE
    client = Face("1vgorh7zmjvdnjq2xjwqq6xnwm6xa4", "zhyjc7xytpu3rcwjy3akzzqiirb3ev")
    faceData = client.detect(images='http://www.taipeitimes.com/images/2012/11/08/thumbs/P03-121108-1.jpg')
    numberOfObjects = len(faceData.body['photos'][0]['tags'])
    if (personIndex is not None) and (0 <= personIndex < numberOfObjects):
        faceIndex = personIndex
    else:
        faceIndex = randrange(numberOfObjects)

    singleFaceData = faceData.body['photos'][0]['tags'][faceIndex]
    faceWidth = singleFaceData['width']
    faceHeight = singleFaceData['height']
    faceXcord = singleFaceData['center']['x'] 
    faceYcord = singleFaceData['center']['y']
    hatWidth = int(math.floor(faceWidth * 2))
    ratio = float(hatWidth) /float(imageHat.size[0])
    hatHeight = int(math.floor(imageHat.size[1] *ratio))  
    imageHatResized = imageHat.resize((hatWidth, hatHeight),PilImage.ANTIALIAS)
    faceX = int(math.floor(faceXcord - imageHatResized.size[0]/2.0))
    faceY = int(math.floor(faceYcord - imageHatResized.size[1]/2.0 - faceHeight/2.0*0.3 ))
    faceY = faceY - faceHeight/2 
    origPilImage.paste(imageHatResized, (faceX, faceY), imageHatResized)
    return (origPilImage , faceIndex)

def placeImageWithOpenCv(origPilImage,origImageUrl,imageHat, personIndex):
################## OPENCV
    faceData = getFace(origImageUrl)
    numberOfObjects = len(faceData['images'][0]['versions'][0]['objects'])
    if (personIndex is not None) and (0 <= personIndex < numberOfObjects):
        faceIndex = personIndex
    else:
        faceIndex = randrange(numberOfObjects)

    singleFaceData = faceData['images'][0]['versions'][0]['objects'][faceIndex]
    faceWidth = int(math.floor(singleFaceData['width'] * origPilImage.size[0]))
    faceHeight = int(math.floor(singleFaceData['height'] * origPilImage.size[1]))
    faceXcord = int(math.floor(singleFaceData['center']['x'] * origPilImage.size[0]))
    faceYcord = int(math.floor(   singleFaceData['center']['y'] * origPilImage.size[1])) 
    hatWidth = int(math.floor(faceWidth * 2.4))
    ratio = float(hatWidth) /float(imageHat.size[0])  
    hatHeight = int(math.floor(imageHat.size[1] *ratio))
    imageHatResized = imageHat.resize((hatWidth, hatHeight),PilImage.ANTIALIAS)
    
    faceX = int(math.floor(faceXcord - imageHatResized.size[0]/2.0))
    faceY = int(math.floor(faceYcord - imageHatResized.size[1]/2.0 - faceHeight/2.0*0.3 ))
    faceY = faceY - faceHeight/2 
    origPilImage.paste(imageHatResized, (faceX, faceY), imageHatResized)
    
    return (origPilImage ,faceIndex)

def placeImage(origPilImage,origImageUrl,finalImageHeight, personIndex):
    #
    imageHat = PilImage.open('%s/viet_hat_stright.png' % settings.HAT_FOLDER)
    #imageHat = PilImage.open('inception/farmer.png')
    #imageHat = PilImage.open('inception/viet_hat.png')

    #(modifiedImage, faceIndex) = placeImageWithMashape(origPilImage,origImageUrl,imageHat, personIndex)
    (modifiedImage, faceIndex) = placeImageWithOpenCv(origPilImage,origImageUrl,imageHat, personIndex)
    
    if (finalImageHeight is not None):
        ratio = float(finalImageHeight) /float(modifiedImage.size[1])  
        finalImageWidth = int(math.floor(ratio * modifiedImage.size[0] ))
        finalImageResized = modifiedImage.resize((finalImageWidth, finalImageHeight),PilImage.ANTIALIAS)
    else:
        finalImageResized = modifiedImage
     
    return (finalImageResized, faceIndex) 


    
