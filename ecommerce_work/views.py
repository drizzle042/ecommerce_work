from django.shortcuts import render
from django.db.models.query_utils import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from dbmodels.models import *

products = Product.objects.all()

product_images =  Product_image.objects.all()

def home(request):
    context = {
        'vegetables': products.filter(subCategory="vegetables").order_by('-date')[:3],
        "vegetables_item_image": product_images,
        "meats_and_sea_food": products.filter(subCategory="meats & seafood").order_by('-date')[:3],
        "bakery": products.filter(subCategory="bakery").order_by('-date')[:3],
        "fashion": products.filter(subCategory="fashion").order_by('-date')[:3],
        "latest_products_grid_1": products.order_by('-date')[:4],
        "latest_products_grid_2": products.order_by('-date')[4:8],
    }
    if request.method == "POST":
        email = request.POST["Email"]
        Subscriber.objects.create(email=email)
        return render(request, './index.html', context=context)
        
    else:
        return render(request, './index.html', context=context)

def details(request, slug):
    product_details = products.get(slug=slug)
    context = {
        "detail" : product_details,
    }
    return render(request, './single.html', context=context)

def shop(request, category):
    category_objects = products.filter(mainCategory=category).order_by("-date")
    page_number = request.GET.get("page")
    paginator = Paginator(category_objects, 9, orphans=0).get_page(page_number)
    context = {
        "paginator": paginator,
        "products_row_1": paginator[:3],
        "products_row_2": paginator[3:6],
        "products_row_3": paginator[6:9],
        "item_image": product_images,
        "Category_": category,
    }
    return render(request, './products.html', context=context)

def about(request):
    return render(request, './about.html')

def faqs(request):
    return render(request, './faq.html')

def contact(request):
    return render(request, './contact.html')

def search(request):
    query = request.GET.get("search")
    if query is None or query == '':
        # return redirect("about/")
        pass
    else:
        postresult = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(slug__icontains=query) | Q(mainCategory__icontains=query) | Q(subCategory__icontains=query)
            ).distinct()
        page_number = request.GET.get("page")
        paginator_object = Paginator(postresult, 9, orphans=0)
        try:
            paginator = paginator_object.page(page_number)
        except PageNotAnInteger:
            paginator = paginator_object.page(1)
        except EmptyPage:
            paginator = paginator_object.page(paginator.num_pages)
        context = {
            "paginator": paginator,
            "products_row_1": paginator[:3],
            "products_row_2": paginator[3:6],
            "products_row_3": paginator[6:9],
            "item_image": product_images,
            "query": query,
        }
        return render(request, './products.html', context=context)
    