"""ecommerce_work URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='homepage'),
    path('about/', about, name='aboutpage'),
    path('faq/', faqs, name='faqpage'),
    path('contact_us/', contact, name='contactpage'),
    path("signup/", sign_up, name="signup_page"),
    path("update-user/", update, name="updateview"),
    path("signin/", sign_in, name="signin_page"),
    path("signout/", sign_out, name="signout_page"),
    path("dashboard", dashboard, name="dashboardpage"),
    path('details/<slug:slug>/', details, name='detailspage'),
    path('admin/', admin.site.urls),
    path('search/', search, name='searchpage'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path("delete/", remove_from_cart, name="delete_from_cart"),
    path("reduce/", reduce_quantity_item, name="reduce_item"),
    path("make-order/", order_view, name="orderView"),
    path("transaction/<slug:slug>/", transaction, name="transactionView"),
    path('shop/<slug:category>/', shop, name='shop_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)
