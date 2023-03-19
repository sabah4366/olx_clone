from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile',)
    profile_pic=models.ImageField(upload_to='profile-pic',null=True,blank=True)
    bio=models.CharField(max_length=200)
    phone_no=models.IntegerField()
    follower=models.ManyToManyField(User,related_name="follower")

    def __str__(self) :
        return self.user.username
    

class Categories(models.Model):
    #for product category
    category_name=models.CharField(max_length=200)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.category_name


    
class Products(models.Model):
    #for products

    CONDITION_TYPE=(
        ('Used','Used'),
        ('New',('New'))
    )

    OPTIONAL=(
        ('for-sale','for-sale'),
        ('exchnage','exchnage'),
        ('sold','sold')

    )
    name=models.CharField(max_length=200)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='forowner')
    brand=models.CharField(max_length=200,blank=True,null=True)
    description=models.TextField(max_length=500)
    price=models.FloatField()
    category=models.ForeignKey(Categories,null=True,on_delete=models.SET_NULL)
    state=models.CharField(max_length=200)
    city=models.CharField(max_length=150)
    condition=models.CharField(max_length=200,choices=CONDITION_TYPE)
    image_1=models.ImageField(upload_to='main_product',blank=False,null=False)
    status=models.CharField(max_length=200,choices=OPTIONAL,default='for-sale')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    likes=models.ManyToManyField(User,related_name='forlikes')

    class Meta:
        ordering=['-updated','-created']

    def __str__(self) :
        return self.name


class ProductImages(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="product-image")

    

class Notifications(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    buyer=models.ForeignKey(User,on_delete=models.CASCADE)
    description=models.CharField(max_length=300)
    created=models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering=['-created']
