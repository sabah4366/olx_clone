from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile,Products,ProductImages,Notifications

class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']


class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()



class ProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['profile_pic','bio','phone_no']

    


class SellingForm(forms.ModelForm):
    class Meta:
        model=Products
        fields=['name','brand','description','price','category','state','city','condition','image_1','status']

        widgets={
            "name":forms.TextInput(attrs={"class":"form-control "}),
            "category":forms.Select(attrs={"class":"form-select"}),
            "image_1":forms.FileInput(attrs={"class":"form-control"}),
            "condition":forms.Select(attrs={"class":"form-select"}),
            "status":forms.Select(attrs={"class":"form-select"}),
            "brand":forms.TextInput(attrs={"class":"form-control"}),
            "description":forms.Textarea(attrs={"class":"form-control"}),
            "price":forms.NumberInput(attrs={"class":"form-control"}),  
            "state":forms.TextInput(attrs={"class":"form-control"}),
            "city":forms.TextInput(attrs={"class":"form-control"}),         
        }

class ProductsImagesForm(forms.ModelForm):
    class Meta:
        model=ProductImages
        fields=['product','image']

        widgets={
            'image':forms.FileInput(attrs={'class':"form-control"}),
            'product':forms.Select(attrs={"class":"form-control"})
        }
        

class NotificationForm(forms.ModelForm):
    class Meta:
        model=Notifications
        fields=['product','description']


        widgets={
            'product':forms.Select(attrs={"class":"form-control"}),
            'description':forms.TextInput(attrs={"class":"form-control"})
        }