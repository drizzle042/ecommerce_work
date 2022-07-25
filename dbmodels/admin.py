from django.contrib import admin
from django import forms
from django_image_compressor.mixins import ImageCompressorFormMixin, ImageCompressionAdminMixin
from django.contrib.auth.admin import UserAdmin
from dbmodels.models import *
from django.contrib import messages

# Write your model admin interface here

class Product_image_upload_form(ImageCompressorFormMixin, forms.ModelForm):
    class Meta:
        model = Product_image
        fields = ("name", "images")
    compressed_image_fields = ["images"]

class ProductImageInterface(ImageCompressionAdminMixin , admin.ModelAdmin):
    empty_value_display = "--None has been selected--"
    ordering = ["name"]
    custom_form = Product_image_upload_form
    
class Product_upload_form(ImageCompressorFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ("date",)
    compressed_image_fields = ["mainImage"]

class ProductInterface(ImageCompressionAdminMixin, admin.ModelAdmin):
    list_display = ["name", "mainCategory", "price"]
    ordering = ["mainCategory"]
    fields = ["name", "slug", ("price", "discount"), "mainImage", "mainCategory", "subCategory", "description"]
    custom_form = Product_upload_form

class OrderInterface(admin.ModelAdmin):
    list_display = ["user", "get_total_price", "ordered_date", "status"]
    ordering = ["ordered_date"]
    actions = ["change_order_status"]
    exclude = ["ordered"]

    @admin.action(description="Mark all selected 'Orders' as delivered")
    def change_order_status(self, request, queryset):
        queryset.update(status= "delivered")
        self.message_user(request, "All  marked orders have been updated successfully!", messages.SUCCESS)


# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(UserImage)
admin.site.register(Product, ProductInterface)
admin.site.register(Product_image, ProductImageInterface)
admin.site.register(Subscriber)
admin.site.register(Faq)
admin.site.register(CartItem)
admin.site.register(Order, OrderInterface)