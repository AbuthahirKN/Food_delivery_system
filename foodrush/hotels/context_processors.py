from hotels.models import Hotel
def hotel_list(request):
    hotels=Hotel.objects.all()
    return {'hotel_list':hotel_list}
