from django.db import models
from urlparse import urlparse
from django.forms.models import model_to_dict
from django.db.models import F
import Image as PilImage 
import cStringIO
import os



class LimitedViewImage(models.Model):
    image_id = models.CharField(max_length=10)
    numberOfViews = models.IntegerField(default=0)
    image_file_path = models.CharField(max_length=10)
    maxViews = models.IntegerField(default=2)
    
    def getImage(self, defaultImagePath):  
        if self.maxViews > self.numberOfViews:
            imagePathToLoad = open(self.image_file_path, 'r')
        else:
            imagePathToLoad = open(defaultImagePath, 'r')
    
        theImage = PilImage.open(imagePathToLoad)
        self.numberOfViews = self.numberOfViews +1
        self.save()
        return theImage
    
    
    def deleteImage(self): 
        os.remove(self.image_file_path)
        self.maxViews = 0
        
 
    
