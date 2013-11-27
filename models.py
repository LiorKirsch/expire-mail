from django.db import models
from urlparse import urlparse
from django.forms.models import model_to_dict
from django.db.models import F
import Image as PilImage 
import cStringIO
import os
import text2Image



class LimitedViewImage(models.Model):
    image_id = models.CharField(max_length=10)
    numberOfViews = models.IntegerField(default=0)
    image_file_path = models.CharField(max_length=1000)
    maxViews = models.IntegerField(default=4)
    text = models.CharField(max_length=1000)
    accessing_add = models.CharField(max_length=3000,default='')
    
    def getImage(self, defaultImagePath,clientAdd, clientHost):  
        self.accessing_add = '%s\n%s:%s' % (self.accessing_add, clientAdd, clientHost)
        if self.maxViews > self.numberOfViews:
#            imagePathToLoad = open(self.image_file_path, 'r')
            image_path = text2Image.transformText2('%s \n(%d)' % (self.text, self.numberOfViews), '%s' % self.image_file_path)
        else:
            image_path = text2Image.transformText2('mail deleted, accessed too many times (%d) %s' % (self.numberOfViews, self.accessing_add), '%s.png' % self.image_file_path)
        imagePathToLoad = open(image_path, 'r')
#	    imagePathToLoad = open(defaultImagePath, 'r')
    
        theImage = PilImage.open(imagePathToLoad)
        self.numberOfViews = self.numberOfViews +1
        self.save()
        return theImage
    
    
    def deleteImage(self): 
        os.remove(self.image_file_path)
        self.maxViews = 0
        
 
    
