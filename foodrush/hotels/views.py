from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from hotels.forms import HotelForm,FoodItemForm
from hotels.models import Hotel, FoodItem
from order.models import Orders,OrderItem
from users.models import Review
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

@method_decorator(login_required,name='dispatch')
class AddHotels(View):
    def post(self,request):
        form_instance = HotelForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('users:home')
    def get(self,request):
        form_instance = HotelForm()
        context = {'form':form_instance}
        return render(request,'addhotels.html',context)

@method_decorator(login_required,name='dispatch')
class HotelDashboard(View):
    def get(self, request):
        hotel = get_object_or_404(Hotel, owner=request.user)
        foods = FoodItem.objects.filter(hotel=hotel)
        orders = Orders.objects.filter(items__fooditem__hotel=hotel).distinct().order_by('-id')
        reviews = Review.objects.filter(hotel=hotel)

        context = {
            'hotel': hotel,
            'total_foods': foods.count(),
            'total_orders': orders.count(),
            'pending': orders.filter(status='Pending').count(),
            'reviews_count': reviews.count(),
            'food_list': foods[:5],
            'order_list': orders[:5],
            'review_list': reviews.order_by('-id')[:5],
        }
        return render(request, 'hotelsdashboard.html', context)


class AddFoodItems(View):
    def post(self,request,hotel_id):
        owner=request.user
        hotel=Hotel.objects.get(id=hotel_id,owner=owner)
        form_instance = FoodItemForm(request.POST,request.FILES)
        if form_instance.is_valid():
           food=form_instance.save(commit=False)
           food.hotel=hotel
           food.save()
           return redirect('users:viewmenu',hotel.id)
        return render(request, 'additems.html', {'form':form_instance,'hotel':hotel})
    def get(self,request,hotel_id):
        owner = request.user
        hotel=Hotel.objects.get(id=hotel_id,owner=owner)
        form_instance = FoodItemForm()
        context={'form':form_instance,'hotel':hotel}
        return render(request,'additems.html',context)

class EditFoodItem(View):
    def post(self,request,i):
        item = FoodItem.objects.get(id=i)
        form_instance = FoodItemForm(request.POST,request.FILES,instance=item)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('hotels:viewmenu')
    def get(self,request,i):
        item=FoodItem.objects.get(id=i)
        form_instance=FoodItemForm(instance=item)
        context={'form':form_instance}
        return render(request,'edit.html',context)

class DeleteFoodItem(View):
    def post(self,request,i):
        item=FoodItem.objects.get(id=i)
        item.delete()
        return redirect('hotels:viewmenu')

class HotelOrders(View):
    def get(self, request, hotel_id):
        hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)
        orders = Orders.objects.filter(items__fooditem__hotel=hotel).exclude(status='Delivered').distinct()
        return render(request, 'hotel_order.html', {'hotel': hotel, 'orders': orders})

class UpdateStatus(View):
    def post(self,request,hotel_id,order_id):
        owner = request.user
        hotel = Hotel.objects.get(id=hotel_id, owner=owner)
        order = get_object_or_404(Orders.objects.filter(items__fooditem__hotel=hotel).distinct(), id=order_id)
        status= request.POST.get('status')
        order.status=status
        order.save()
        return redirect('hotels:hotel_orders',hotel_id=hotel.id)
    def get(self,request,hotel_id,order_id):
        owner =request.user
        hotel=Hotel.objects.get(id=hotel_id,owner=owner)
        order=get_object_or_404(Orders.objects.filter(items__fooditem__hotel=hotel).distinct(),id=order_id)
        context={'hotel':hotel,'orders':order}
        return render(request, 'updatestatus.html',context)

class HotelReviews(View):
    def get(self, request, hotel_id):
        hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)
        reviews = Review.objects.filter(hotel=hotel).order_by('-id')
        return render(request, 'hotelreview.html', {
            'hotel': hotel,
            'reviews': reviews
        })

class EditHotel(View):
    def get(self,request,i):
        hotel=Hotel.objects.get(id=i)
        form_instance = HotelForm(instance=hotel)
        context={'form':form_instance,'hotel':hotel}
        return render(request,'edithotel.html',context)
    def post(self,request,i):
        hotel = Hotel.objects.get(id=i)
        form_instance = HotelForm(request.POST,request.FILES,instance=hotel)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('users:admindashboard')
        return render(request, 'edithotel.html', {'form':form_instance, 'hotel':hotel})
class DeleteHotel(View):
    def post(self,request,i):
        hotel = Hotel.objects.get(id=i)
        hotel.delete()
        return redirect('users:admindashboard')

