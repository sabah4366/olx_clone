from django.contrib import admin
from .models import Categories,Products,UserProfile,ProductImages,Notifications



admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(UserProfile)
admin.site.register(ProductImages)
admin.site.register(Notifications)

# Register your models here.
