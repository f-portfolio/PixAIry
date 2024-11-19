from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django_resized import ResizedImageField
from accounts.models import Profile
from Webpagestructure.models import SiteStructure

# Create your models here.


class MidjernyImage(models.Model):
    site_name = models.ForeignKey('webpage.SiteStructure', on_delete=models.CASCADE, null=True, blank=True,)
    title = models.CharField(max_length=200, unique=True) 
    description = models.CharField(max_length=250, null=True, blank=True)
    midjerny_id = models.CharField(max_length=100, unique=True)
    publisher = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='posts_publisher')
    image_webp = ResizedImageField(force_format="WEBP", quality=75, upload_to="images/webp/", unique=True)
    image_original = models.ImageField(upload_to='images/original/', unique=True) 
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True,)
    tags = models.ManyToManyField("Tag", related_name='posts_tag')
    size_picture = models.ManyToManyField("Size_picture", related_name='posts_size_picture')
    counted_likes = models.IntegerField(default=0)  
    counted_save = models.IntegerField(default=0)
    created_date = jmodels.jDateTimeField(auto_now_add=True)
    updated_date = jmodels.jDateTimeField(auto_now=True)
   
    def __str__(self):
        return self.title
        
    class Meta:
        ordering = ['created_date']
        

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
        
        
class Tag(models.Model):
    name = models.CharField (max_length=30,  unique=True)
    user_adder = models.ForeignKey('accounts.Profile',  on_delete=models.SET_NULL, null=True, blank=True, related_name='user_adder',)
    created_date = jmodels.jDateTimeField(auto_now_add=True, null=True, blank=True)
    updated_date = jmodels.jDateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        

class Size_picture(models.Model):
    name = models.CharField(max_length=30,  unique=True)
    value= models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        

class PictureLike(models.Model):
    user = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    picture_post = models.ForeignKey(MidjernyImage, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.user.username} likes {self.picture_post.title}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'picture_post'], name='unique_like')
        ]

class Dislike(models.Model):
    user = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    picture_post = models.ForeignKey(MidjernyImage,  on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.user.username} likes {self.picture_post.title}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'picture_post'], name='unique_dislike')
        ]
       
       
class Save(models.Model):
    user = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    picture_post = models.ForeignKey(MidjernyImage, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.user.username} likes {self.picture_post.title}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'picture_post'], name='unique_save')
        ]
