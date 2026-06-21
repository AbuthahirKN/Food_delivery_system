"""
URL configuration for foodrush project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views
app_name = 'users'
urlpatterns = [
    path('',views.Home.as_view(),name='home'),
    path('register/', views.Register.as_view(), name='register'),
    path('login', views.Login.as_view(), name='login'),
    path('search/',views.SearchFood.as_view(),name='search'),
    path('reviews/<int:i>',views.AddReview.as_view(),name='reviews'),
    path('viewmenu/<int:i>',views.ViewMenu.as_view(),name='viewmenu'),
    path('hoteldetail/<int:i>',views.HotelDetails.as_view(),name='hoteldetail'),
    path('fooddetails/<int:i>',views.FoodDetails.as_view(),name='fooddetails'),
    path('admindashboard/',views.AdminDashboard.as_view(),name='admindashboard'),
    path('orders/<int:order_id>/tracking/',views.Tracking.as_view(), name='tracking'),
    path('logout', views.Logout.as_view(),name='logout'),
]
