from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from delivery.models import Delivery
from order.models import Orders
from delivery.forms import DeliveryForm
from django.contrib.auth.decorators import login_required
# Create your views here.

class DeliveryDashboard(View):
    def get(self,request):
        available_orders=Orders.objects.filter(status='OUT FOR DELIVERY',
        delivery__isnull=True)
        my_orders=Delivery.objects.filter(delivery_partner=request.user)
        context={'available_orders':available_orders,'my_orders':my_orders}
        return render(request,'deliverydashboard.html',context)


class AssignDelivery(View):
    def get(self, request, i):
        order =get_object_or_404(Orders, id=i, status='OUT FOR DELIVERY')
        delivery,created= Delivery.objects.get_or_create( order=order,
            defaults={
                'delivery_partner': request.user,
                'status': 'ASSIGNED'
            }
        )
        if not created:
            delivery.delivery_partner=request.user
            delivery.status = 'ASSIGNED'
            delivery.save()
        return redirect('delivery:deliverydashboard')
import uuid
class UpdateDelivery(View):
    def post(self,request,i):
        delivery_partner=request.user
        delivery=Delivery.objects.get(id=i,delivery_partner=delivery_partner)
        status=request.POST.get('status')
        delivery.status=status
        delivery.save()
        if status == 'DELIVERED':
            order = delivery.order
            order.status = 'DELIVERED'
            order.save()

        return redirect('delivery:deliverydashboard')
    def get(self,request,i):
        delivery_partner = request.user
        delivery = Delivery.objects.get(id=i, delivery_partner=delivery_partner)
        context={'delivery':delivery}
        return render(request,'deliverystatus.html',context)

class MarkAsDelivered(View):
    def get(self,request, i):
      order = get_object_or_404(Orders, id=i)
      order.status = "Delivered"
      if order.payment_method == "COD":
         order.payment_status = "Paid"
         if not order.payment_id:
             order.payment_id = "CODPAY_" + uuid.uuid4().hex[:10].upper()
         order.save()

         return redirect("delivery:deliverydashboard")




