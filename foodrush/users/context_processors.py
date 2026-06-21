# users/context_processors.py
from order.models import Orders

def latest_order(request):
    if request.user.is_authenticated:
        order = Orders.objects.filter(user=request.user).order_by('-ordered_at').first()
        return {'latest_order': order}
    return {}
