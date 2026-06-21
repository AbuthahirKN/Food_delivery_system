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
from delivery import views
app_name = 'delivery'
urlpatterns = [
    path('deliverydashboard',views.DeliveryDashboard.as_view(),name='deliverydashboard'),
   path('accept/<int:i>',views.AssignDelivery.as_view(),name='accept_order'),
    path('update/<int:i>',views.UpdateDelivery.as_view(),name='update_order'),
    path('mark/<int:i>',views.MarkAsDelivered.as_view(),name='mark')


]
