from django.db import models
from urlparse import urlparse
from django.forms.models import model_to_dict
from django.db.models import F
import Image as PilImage 
import cStringIO
import os
import text2Image
from datetime import datetime, timedelta



class LimitedViewImage(models.Model):
    image_id = models.CharField(max_length=10)
    numberOfViews = models.IntegerField(default=0)
    effectiveNumberOfViews = models.IntegerField(default=0)

    image_file_path = models.CharField(max_length=1000)
    maxViews = models.IntegerField(default=1)
    text = models.CharField(max_length=1000)
    accessing_add = models.CharField(max_length=3000,default='')
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)
    creating_client_ip = models.CharField(max_length=1000)
    
    def getImage(self, defaultImagePath,clientAdd,debug, creatingUser = False):  
        self.accessing_add = '%s\n%s' % (self.accessing_add, clientAdd)
        if self.maxViews > self.effectiveNumberOfViews:
            if debug:
                image_path = text2Image.transformText2('%s \n(%d,%d)' % (self.text, self.effectiveNumberOfViews,self.numberOfViews), '%s' % self.image_file_path)
            else:
                image_path = self.image_file_path
            
        else:
            if debug:
                image_path = text2Image.transformText2('mail deleted, accessed too many times (%d,%d) %s' % (self.effectiveNumberOfViews, self.numberOfViews, self.accessing_add), '%s.png' % self.image_file_path)
            else:
                image_path = text2Image.transformText2('mail deleted, accessed too many times (%d)' % (self.effectiveNumberOfViews), '%s.png' % self.image_file_path)
            
        imagePathToLoad = open(image_path, 'r')
#	    imagePathToLoad = open(defaultImagePath, 'r')
    
        theImage = PilImage.open(imagePathToLoad)
        if (not creatingUser):
            if (clientAdd != self.creating_client_ip) | (datetime.now() > self.creation_date + timedelta(seconds=30) ):
                self.effectiveNumberOfViews = self.effectiveNumberOfViews +1
            
        self.numberOfViews = self.numberOfViews +1
        self.save()
        return theImage
    
    
    def deleteImage(self): 
        os.remove(self.image_file_path)
        self.maxViews = 0
        
 
    
