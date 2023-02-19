from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,CreateView,FormView,ListView,UpdateView,DetailView
from .models import Categories,Products,UserProfile,ProductImages,Notifications
from .forms import RegistrationForm,LoginForm,ProfileForm,SellingForm,ProductsImagesForm,NotificationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q,Count
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


def signinRequired(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,'you must login')
            return redirect('signin')
        else:
            return fn(request,*args,**kwargs)
        
    return wrapper


    

desc=[never_cache,signinRequired]


class RegistrationsView(CreateView):
    template_name='products/register.html'
    form_class=RegistrationForm
    success_url=reverse_lazy('signin')

    def form_valid(self, form) :
        messages.success(self.request,'Account has been created')
        return super().form_valid(form)
    

    def form_invalid(self, form):
        messages.error(self.request,'Account creation failed') 
        return super().form_invalid(form)



class LoginView(FormView):
    template_name='products/login.html'
    form_class=LoginForm

    def post(self,request, *args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get('username')
            pswrd=form.cleaned_data.get('password')
            usr=authenticate(request,username=uname,password=pswrd)
            if usr:
                login(request,usr)
                messages.success(request,'You are logged in')
                return redirect('home')
            else:
                messages.error(request,'invalid credentials')
                return render(request,'products/login.html',{"form":form})
        



@method_decorator(desc,name='dispatch')
class HomePage(ListView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        
        # if id is  prescent then filter products based on that id else all products  
        if id:
            products=Products.objects.filter(category=id).exclude(owner=request.user)
                
        else:
            products=Products.objects.all().exclude(owner=request.user)

        profile=UserProfile.objects.all()
        
        categories=Categories.objects.annotate(total_products=Count('products'))
        searchquery=request.GET.get('q')
        if searchquery:
            products=Products.objects.filter(
                Q(name__icontains=searchquery) |
                Q(brand__icontains=searchquery)|
                Q(category__category_name__icontains=searchquery) 
            ).exclude(owner=request.user)  
            
            
        searchqrytwo=request.GET.get('y')
        if searchqrytwo:
            products=Products.objects.filter(
                Q(state__icontains=searchqrytwo) |
                Q(city__icontains=searchqrytwo) 
            ).exclude(owner=request.user)  
            
        productimages=ProductImages.objects.all()
        paginator = Paginator(products, 16) # Show 2 contacts per page.

        page= request.GET.get('page')
        products = paginator.get_page(page)


        context={"products":products,"profile":profile,"categories":categories,"productimages":productimages}
        return render(request,'products/product-list.html',context)



# profile section start
@method_decorator(desc,name='dispatch')
class UserProfileView(CreateView):
    template_name='products/profile.html'
    form_class=ProfileForm
    success_url=reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,'Profile hasbeen created')
        return super().form_valid(form)
    

    def form_invalid(self, form):
        messages.success(self.request,'profile creation failed') 
        return super().form_invalid(form)


# def updateprofile(request,pk):
#     prof=UserProfile.objects.get(id=pk)
#     form=ProfileForm(instance=prof)
#     if request.method == "POST":
#         form=ProfileForm(request.POST,instance=prof)
#         if form.is_valid():
#             form.user=request.user
#             form.save()
#             messages.success(request,"Profile Has Been Updated")
#             return redirect('home')
#     return render(request,'products/profile.html',{"form":form})


# this is class based view for update profile
@method_decorator(desc,name='dispatch')
class UserProfileUpdateView(UpdateView):
    template_name='products/profile.html'
    model=UserProfile
    fields=['profile_pic','bio','phone_no']
    success_url=reverse_lazy('home')




    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,'Profile hasbeen updated')
        return super().form_valid(form)
    

    def form_invalid(self, form):
        messages.success(self.request,'profile updation failed') 
        return super().form_invalid(form)




class ShowProfile(DetailView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        profile=UserProfile.objects.get(id=id)
        # for listing all products owner at the time of clicking product listing page owner
        products=Products.objects.filter(owner=id)
        print('gdsaasdfghjhgfgh')
        print(products)
        print(id)
        print(profile)
        return render(request,"products/profilepage.html",{"profile":profile,"products":products})
    
# profile end here






# product based view start
@method_decorator(desc,name='dispatch')    
class ProductSellingView(CreateView):
    template_name='products/selling.html'
    form_class=SellingForm
    success_url=reverse_lazy('home')

    def form_valid(self, form):
        form.instance.owner=self.request.user
        messages.success(self.request,'Product added')
        return super().form_valid(form)
    

    def form_invalid(self, form):
        messages.success(self.request,'product creation failed') 
        return super().form_invalid(form)



@method_decorator(desc,name='dispatch')
class ProductUpadteView(UpdateView):
    model=Products
    template_name="products/selling.html"
    fields=['name','brand','description','price','category','state','city','condition','image_1','status']
    success_url=reverse_lazy('home')

  




@method_decorator(desc,name='dispatch')
class ProductDetailView(DetailView):
   
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        productimages=ProductImages.objects.filter(product=id)
        product=Products.objects.get(id=id)
        msg=False
        if request.user.is_authenticated:
            user=request.user

            if product.likes.filter(id=user.id).exists():
                msg=True

        

        return render(request,'products/product-details.html',{"product":product,"productimages":productimages,"msg":msg})

    
    
    def post(self,request,*args,**Kwargs):
        id=Kwargs.get('pk')
        productimages=ProductImages.objects.filter(product=id)
        product=Products.objects.get(id=id)
        if request.user.is_authenticated:
            user=request.user
            if product.likes.filter(id=user.id).exists():
                product.likes.remove(user)
                msg=False

            else:
                product.likes.add(user)
                msg=True 

        return render(request,'products/product-details.html',{"product":product,"msg":msg,"productimages":productimages})
    
    


@method_decorator(desc,name='dispatch')
class ProductImageCreateView(CreateView):
    template_name='products/add_product_image.html'
    form_class=ProductsImagesForm
    success_url=reverse_lazy('user-product')
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        product=Products.objects.get(id=id)
        form=self.form_class(initial={"product":product})

        return render(request,"products/add_product_image.html" ,{"form":form})



    

   





class CategoryProductsView(ListView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        categories=Categories.objects.filter(id=id)
        if id:
            products=Products.objects.filter(category=id).exclude(owner=request.user)              
        else:
            products=Products.objects.all().exclude(owner=request.user)  

        context={"products":products,"categories":categories}
        return render(request,'products/category_product_list.html',context)

    

   

@method_decorator(desc,name='dispatch')
class UserProducts(ListView):
    template_name="products/userproducts.html"
    model=Products
    context_object_name="products"
    
    def get_queryset(self) :
        return Products.objects.filter(owner=self.request.user)


@method_decorator(desc,name='dispatch')
class ProductDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        Products.objects.filter(id=id).delete()
        return redirect('home')
    
# products end here

class NotificationView(CreateView):
    template_name="products/notifications.html"
    form_class=NotificationForm
    success_url=reverse_lazy('home')
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        product=Products.objects.get(id=id)
        form=self.form_class(initial={"product":product})

        return render(request,"products/notifications.html" ,{"form":form})

    def form_valid(self, form):
        form.instance.buyer=self.request.user
        return super().form_valid(form)



class NotificationListView(ListView):
    template_name='products/show-msg.html'
    model=Notifications
    context_object_name='notifications'







def productsold(request,*args,**kwargs):
    id=kwargs.get('pk')
    Products.objects.filter(id=id).update(status="sold")
    return redirect('home')



# logout view

def logoutview(request,*args,**kwargs):
    logout(request)
    messages.success(request,"You are logouted")
    return redirect('signin')