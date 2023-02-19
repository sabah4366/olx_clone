from django.urls import path
from . import views

urlpatterns=[
    path('',views.LoginView.as_view(),name='signin'),
    path('register',views.RegistrationsView.as_view(),name="signup"),
    path('home',views.HomePage.as_view(),name="home"),
    path('home/<int:pk>',views.HomePage.as_view(),name="home"),
    path('category/<int:pk>/products',views.CategoryProductsView.as_view(),name="category-product-list"),
    path('profile',views.UserProfileView.as_view(),name='profile'),
    path('update/<int:pk>/update',views.UserProfileUpdateView.as_view(),name="update-profile"),
    path('showprofile/<int:pk>',views.ShowProfile.as_view(),name='show-profile') , 
    path('sell',views.ProductSellingView.as_view(),name='selling'),
    path('product-detail/<int:pk>',views.ProductDetailView.as_view(),name="product-detail"),
    path('user-product',views.UserProducts.as_view(),name="user-product"),
    path('product/<int:pk>/remove',views.ProductDeleteView.as_view(),name="remove-product"),
    path('product/<int:pk>/update',views.ProductUpadteView.as_view(),name="product-update"),
    path('add/<int:pk>/image',views.ProductImageCreateView.as_view(),name='create-product-image'),
    path('product-sold/<int:pk>',views.productsold,name='product-sold'),
    path('notifications/<int:pk>/add',views.NotificationView.as_view(),name='notification'),
    path('show-notifications',views.NotificationListView.as_view(),name='show-notification'),

    path('logout',views.logoutview,name='signout')


]