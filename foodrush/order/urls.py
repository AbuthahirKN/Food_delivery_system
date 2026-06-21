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
from order import views
app_name = 'order'
urlpatterns = [
    path('addtocart/<int:i>',views.AddToCart.as_view(),name="addtocart"),
    path('cartview',views.CartView.as_view(),name="cartview"),
    path('decrement/<int:i>',views.CartDecrement.as_view(),name="decrement"),
    path('increment/<int:i>',views.CartIncrement.as_view(),name='increment'),
    path('removecart/<int:i>',views.CartRemove.as_view(),name="removecart"),
    path('checkout',views.Checkout.as_view(),name="checkout"),
    path('placeorder',views.PlaceOrder.as_view(),name="placeorder"),
    path('paymentsuccess', views.PaymentSuccess.as_view(), name="paymentsuccess"),
    path('history',views.OrderHistory.as_view(),name='history'),

]
