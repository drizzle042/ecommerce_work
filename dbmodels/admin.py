from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from dbmodels.models import *

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Product)
admin.site.register(Product_image)
admin.site.register(Subscriber)
admin.site.register(Faq)
admin.site.register(CartItem)
admin.site.register(Order)