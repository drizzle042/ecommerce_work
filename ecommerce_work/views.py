from django.shortcuts import redirect, render, get_object_or_404
from django.db.models.query_utils import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from dbmodels.models import *
from django.utils import timezone

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

def search(request):
    query = request.GET.get("search")
    if query is None or query == '':
        return redirect("homepage")
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

def sign_up(request):
    if request.method == "POST":
        username = request.POST.get("UserName")
        email = request.POST.get("Email")
        password = request.POST.get("Password")
        password2 = request.POST.get("Password2")

        if request.POST.get("FirstName"):
            firstname = request.POST.get("FirstName")
        else:
            firstname = ""

        if request.POST.get("LastName"):
            lastname = request.POST.get("LastName")
        else:
            lastname = ""

        if request.POST.get("BillingAddress"):
            billing_address = request.POST.get("BillingAddress")
        else:
            billing_address = ""

        if request.POST.get("State"):
            state = request.POST.get("State")
        else:
            state = ""
            
        if password == password2 and len(password) >= 8:
            passcode = password
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username=username, email=email, password=passcode)
                user.first_name = firstname
                user.last_name = lastname
                user.billing_address = billing_address
                user.state = state
                user.save()
                messages.success(request, "Success")
                print("Success")  
                
                return redirect("dashboardpage") 
            else:
                messages.error(request, "Sorry the email already exists in our database")
                print("Sorry the email already exists in our database")
                return redirect("homepage")
        elif len(password) < 8:
            messages.error(request, "Please make sure your password is above 8 (eight) characters long!")
            print("Please make sure your password is above 8 (eight) characters long!")
            return redirect("homepage")
        else:
            messages.error(request, "Your passwords do not match!")
            print("Your passwords do not match!")
            return redirect("homepage")
    else:
        return redirect("homepage")

@login_required
def update(request):
    if request.method == "POST":
        username = request.POST.get("UserName")
        email = request.POST.get("Email")
        current_password = request.POST["CurrentPassword"]
        password = request.POST.get("Password")
        password2 = request.POST.get("Password2")
        firstname = request.POST.get("FirstName")
        lastname = request.POST.get("LastName")
        billing_address = request.POST.get("BillingAddress")
        state = request.POST.get("State")
            
        if password == password2 and len(password) >= 8:
            passcode = password
            user = authenticate(request, email=email, password=current_password)
            if user is not None:
                user.first_name = firstname
                user.last_name = lastname
                user.username = username
                user.email = email
                user.billing_address = billing_address
                user.state = state
                user.set_password(passcode)
                user.save()
                messages.success(request, "Success")
                print("Success")  
                
                return redirect("dashboardpage") 
            else:
                messages.error(request, f"Wrong email: {email}, or password! \n Please review...")
                print(f"Wrong email: {email}, or password! \n Please review...")
                return redirect("dashboardpage")
        elif len(password) < 8:
            messages.error(request, "Please make sure your password is above 8 (eight) characters long!")
            print("Please make sure your password is above 8 (eight) characters long!")
            return redirect("dashboardpage")
        else:
            messages.error(request, "Your passwords do not match!")
            print("Your passwords do not match!")
            return redirect("dashboardpage")
    else:
        return redirect("dashboardpage")

def sign_in(request):
    if request.method == "POST":
        email = request.POST["Email"]
        password = request.POST["Password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome back!")
            return redirect("dashboardpage")
        else:
            messages.error(request, "Please check your login details")
            return redirect("signin_page")
    else:
        return render(request, "./signup-signin.html")

@login_required
def sign_out(request):
    logout(request)
    messages.success(request, "Bye!")
    return redirect("homepage")

@login_required
def dashboard(request):
    context = {
        "user": request.user
    }
    return render(request, "./dashboard.html", context)

@login_required
def order_summary(request):
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            context = {
                "object": order
            }
            return render(request, "./order_summary.html", context)

        except ObjectDoesNotExist:
            return redirect("/")
    else:
        return render(request, "./order_summary.html")

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            return redirect("order_summary_page_for_authenticated_users")
        else:
            order.items.add(order_item)
            return redirect("order_summary_page_for_authenticated_users")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        return redirect("order_summary_page_for_authenticated_users")

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.delete()
            messages.info(request, "Item \""+order_item.item.item_name+"\" remove from your cart")
            return redirect("order_summary_page_for_authenticated_users")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("detailspage", slug=slug)
    else:
        messages.info(request, "You do not have an Order")
        return redirect("detailspage", slug=slug)

def about(request):
    return render(request, './about.html')

def faqs(request):
    context = {
        "faqs" : Faq.objects.all()
    }
    return render(request, './faq.html', context)

def contact(request):
    return render(request, './contact.html')
    