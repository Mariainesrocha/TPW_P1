from django.contrib import admin
from django.urls import path
from TechSekai import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('login/<str:accountType>/', views.login, name='login'),
    path('account/', views.account, name='account'),
    path('logout/', views.logout, name='logout'),

    path('shopcart/', views.shopcart, name='shopcart'),
    path('wishlist', views.wishlist, name='wishlist'),

    path('add/<str:pType>/', views.addProduct, name='addProduct'),
    path('edit/<int:pID>/', views.editProduct, name='editProduct'),
]