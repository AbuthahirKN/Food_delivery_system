from django.shortcuts import render,redirect,get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from hotels.models import FoodItem
from order.models import Cart,Orders,OrderItem
from order.forms import OrderForm
from django.views import View
from django.conf import settings
import hmac, hashlib
from django.contrib.auth.decorators import login_required
import razorpay

class AddToCart(View):
    def get(self,request,i):
        u = request.user
        f=get_object_or_404(FoodItem, id=i)
        try:
            c = Cart.objects.get(user=u,fooditem=f)
            c.quantity+=1
            c.save()
        except:
            c = Cart.objects.create(user=u,fooditem=f,quantity=1)
            c.save()
        return redirect('order:cartview')

class CartView(View):
    def get(self, request):
        u = request.user
        item = Cart.objects.filter(user=u)
        total = 0
        for i in item:
            total += i.totalamount()
        context = {'cart': item, 'total': total}
        return render(request, 'cart.html', context)

class CartDecrement(View):
    def get(self,request,i):

        try:
            item = Cart.objects.get(id=i)
            if item.quantity > 1:
               item.quantity-=1
               item.save()
            else:
               item.delete()
        except:
            pass
        return redirect('order:cartview')
class CartIncrement(View):
    def get(self,request,i):
        try:
            item=Cart.objects.get(id=i)
            if item.quantity <= 1:
                item.quantity +=1
                item.save()
        except:
            pass
        return redirect('order:cartview')
class CartRemove(View):
    def get(self,request,i):
        try:
           item=Cart.objects.get(id=i)
           item.delete()
        except:
            pass
        return redirect('order:cartview')

class Checkout(View):
    def get(self, request):
        u = request.user
        item = Cart.objects.filter(user=u)
        total = 0
        for i in item:
            total += i.totalamount()
        context = {'cart': item, 'total': total}
        return render(request, 'checkout.html', context)
import uuid

class PlaceOrder(View):
    def post(self, request):
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user

            cart_items = Cart.objects.filter(user=request.user)

            if not cart_items.exists():
                return redirect('order:cartview')

            total = 0
            for item in cart_items:
                total += item.fooditem.price * item.quantity

            order.amount = total
            order.save()

            # ONLINE PAYMENT
            if order.payment_method == 'ONLINE':
                client = razorpay.Client(
                    auth=(
                        settings.RAZORPAY_KEY_ID,
                        settings.RAZORPAY_KEY_SECRET
                    )
                )

                payment = client.order.create({
                    'amount': int(order.amount * 100),  # paise
                    'currency': 'INR',
                    'payment_capture': 1
                })
                print(payment)
                # Store Razorpay Order ID
                order.order_id = payment['id']
                order.save()

                context = {
                    'payment': payment,
                    'order': order,
                    'razorpay_key': settings.RAZORPAY_KEY_ID,
                }

                return render(request, 'payment.html', context)


            else:
                order.order_id = 'COD_' + uuid.uuid4().hex[:10]
                order.is_ordered = True
                order.payment_status = 'Pending'
                order.save()

                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        fooditem=item.fooditem,
                        quantity=item.quantity
                    )

                cart_items.delete()

                return redirect('order:history')

        print(form.errors)
        return redirect('order:checkout')

@method_decorator(csrf_exempt, name='dispatch')
class PaymentSuccess(View):
    def post(self, request):
        order_id = request.POST.get("razorpay_order_id")
        payment_id = request.POST.get("razorpay_payment_id")
        signature = request.POST.get("razorpay_signature")

        try:
            order = Orders.objects.get(order_id=order_id)
        except Orders.DoesNotExist:
            return render(request, "paymentfailed.html", {"error": "Order not found"})

        # Verify Razorpay signature
        msg = f"{order_id}|{payment_id}"
        generated_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            msg.encode(),
            hashlib.sha256
        ).hexdigest()

        if generated_signature != signature:
            return render(request, "payment_failed.html", {"error": "Authentication failed"})


        if not order.is_ordered:
            order.payment_id = payment_id
            order.payment_status = "Paid"
            order.is_ordered = True
            order.save()

            cart_items = Cart.objects.filter(user=order.user)
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    fooditem=item.fooditem,
                    quantity=item.quantity
                )
            cart_items.delete()

        return render(request, "paymentsuccess.html", {"order": order})

    # def post(self, request):
    #     order_id = request.POST.get("razorpay_order_id")
    #     payment_id = request.POST.get("razorpay_payment_id")
    #
    #     order = Orders.objects.get(order_id=order_id)
    #
    #     if not order.is_ordered:
    #         order.payment_id = payment_id
    #         order.payment_status = "Paid"
    #         order.is_ordered = True
    #         order.save()
    #
    #         cart_items = Cart.objects.filter(user=order.user)
    #
    #         for item in cart_items:
    #             OrderItem.objects.create(
    #                 order=order,
    #                 fooditem=item.fooditem,
    #                 quantity=item.quantity
    #             )
    #
    #         cart_items.delete()
    #
    #     return render(
    #         request,
    #         "paymentsuccess.html",
    #         {"order": order}
    #     )


class OrderHistory(View):
    def get(self,request):
        orders=Orders.objects.filter(user=request.user, status="DELIVERED").order_by('-ordered_at')
        context={'orders':orders}
        return render(request, 'history.html',context)
