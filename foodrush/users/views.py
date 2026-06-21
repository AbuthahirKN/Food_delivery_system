from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.db.models import Count,Avg,Q,Sum
from users.forms import SignupForm,LoginForm,ReviewForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from hotels.forms import HotelForm,FoodItemForm
from hotels.models import Hotel, FoodItem
from order.models import Orders
from delivery.models import Delivery
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

class Home(View):
    def get(self, request):
        foods = FoodItem.objects.all()[:9]
        hotels = Hotel.objects.annotate(
            avg_rating=Avg('reviews__rating'),
            rating_count=Count('reviews'),
            count_4=Count('reviews', filter=Q(reviews__rating=4 ))
        )
        for hotel in hotels:
            display_rating = hotel.avg_rating or 0

            if hotel.count_4 >= 2:
                display_rating = 3.9 + (hotel.count_4 - 2) * 0.1
                if display_rating > 4.7:
                    display_rating = 4.7
            hotel.display_rating = display_rating
        context = {
            'foods': foods,
            'hotels': hotels
        }
        return render(request, 'home.html', context)


class Register(View):
    def post(self, request):
        form_instance = SignupForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('users:home')
        else:
            return render(request, 'register.html', {'form': form_instance})
    def get(self, request):
        form_instance = SignupForm()
        context = {'form': form_instance}
        return render(request, 'register.html', context)
class Login(View):
    def post(self,request):
        form_instance = LoginForm(request.POST)
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            u=data['username']
            p=data['password']
            user=authenticate(username=u,password=p)
            if user and user.is_superuser:
                login(request,user)
                return redirect('users:admindashboard')
            elif user and user.role=="CUSTOMER":
                login(request,user)
                return redirect('users:home')
            elif user and user.role=="HOTELS":
                login(request,user)
                return redirect('hotels:hoteldashboard')
            elif user and user.role=="DELIVERY":
                login(request,user)
                return redirect("delivery:deliverydashboard")
            else:
                messages.error(request,"invalid credentials")
                return redirect('users:login')
        return render(request, 'login.html', {'form': form_instance})
    def get(self,request):
        form_instance = LoginForm()
        context ={'form':form_instance}
        return render(request,'login.html',context)

@method_decorator(login_required,name='dispatch')
class HotelDetails(View):
    def get(self, request,i):
        h = Hotel.objects.get(id=i)
        context = {'hotel':h}
        return render(request,'hoteldetail.html' ,context)

@method_decorator(login_required,name='dispatch')
class ViewMenu(View):
    def get(self,request,i):
        hotel = Hotel.objects.get(id=i)
        menu=FoodItem.objects.filter(hotel=hotel)
        context = {'menu': menu,'hotel':hotel}
        return render(request,'menu.html',context)

@method_decorator(login_required,name='dispatch')
class FoodDetails(View):
    def get(self,request,i):
        item=FoodItem.objects.get(id=i)
        context = {'item':item}
        return render(request,'food_detail.html',context)


class Tracking(View):
    def get(self, request, order_id):
        order = get_object_or_404(Orders, id=order_id, user=request.user)
        delivery = Delivery.objects.filter(order=order).first()
        context = {
            'order': order,
            'delivery': delivery,
        }
        return render(request, 'tracking.html', context)


@method_decorator(login_required,name='dispatch')
class SearchFood(View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        if query:
            foods = FoodItem.objects.filter(food_name__icontains=query, available=True)
            if foods.count() == 1:
                return redirect('users:fooddetails', i=foods.first().id)
            if foods.exists():
                context = {'foods': foods, 'query': query}
                return render(request, 'search.html', context)
            return render(request, 'search.html', {
                'foods': [],
                'query': query,
                'message': "No such food found."
            })
        return render(request, 'search.html', {
            'foods': [],
            'query': '',
            'message': "no food named that."
        })


class AdminDashboard(View):
    def get(self, request):
        # Aggregate revenue per hotel
        hotels = Hotel.objects.annotate(
            revenue=Sum('food__orderitem__order__amount')
        ).order_by('-revenue')

        context = {
            'hotels': hotels,
            'total_revenue': hotels.aggregate(Sum('revenue'))['revenue__sum'] or 0
        }
        return render(request, 'admin.html', context)

@method_decorator(login_required,name='dispatch')
class AddReview(View):
    def post(self, request, i):
        hotel = Hotel.objects.get(id=i)
        form_instance = ReviewForm(request.POST)
        if form_instance.is_valid():
            review = form_instance.save(commit=False)
            review.hotel = hotel
        review.user = request.user
        review.save()
        return redirect('users:home')

    def get(self,request,i):
        hotel = Hotel.objects.get(id=i)
        form_instance=ReviewForm()
        context = {'hotel':hotel,'form':form_instance}
        return render(request,'reviews.html',context)

class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('users:login')