from django.contrib import admin
from users.models import CustomUser,Review
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Review)