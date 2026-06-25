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
from hotels import views
app_name = 'hotels'
urlpatterns = [
   path('addhotel/',views.AddHotels.as_view(),name='addhotels'),
   path('hoteldashboard',views.HotelDashboard.as_view(),name='hoteldashboard'),
   path('fooditems/<int:hotel_id>/',views.AddFoodItems.as_view(),name='fooditems'),
   path('orders/<int:hotel_id>/', views.HotelOrders.as_view(), name='hotel_orders'),
   path('orders/<int:hotel_id>/<int:order_id>/update/',views.UpdateStatus.as_view(),name='updatestatus'),
   path('editfood/<int:i>',views.EditFoodItem.as_view(),name='editfood'),
   path('delete/<int:i>',views.DeleteFoodItem.as_view(),name='delete'),
   path('hotelreviews/<int:hotel_id>',views. HotelReviews.as_view(), name='hotelreviews'),
   path('edithotel/<int:i>',views.EditHotel.as_view(),name='edithotel'),
   path('deletehotel/<int:i>',views.DeleteHotel.as_view(),name='deletehotel')
]
