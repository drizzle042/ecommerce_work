from django.shortcuts import redirect, render
from django.conf import settings
from django.db.models.query_utils import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
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
        if not Subscriber.objects.filter(email = email).exists():
            Subscriber.objects.create(email=email)
            subscriber = Subscriber.objects.all().order_by("-date")[0]
            subscriber_email = subscriber.email
            print(subscriber_email)
            subject = "Thank you for subscribing"
            message = """
            We are happy you are interested in our Products. We assure you the very best of all our quality products we have to offer \n
            Our products are highly organic and made from purely quality stuff. You will witness this first hand.
                    """
            sender = settings.EMAIL_HOST_USER
            recipient = [str(subscriber_email),]

            send_mail(
                subject=subject,
                message=message,
                from_email=sender,
                recipient_list=recipient,
                fail_silently=True
            )
        else:
            pass
        messages.info(request, f"Your email {email} has been successfully subscribed to our mailing list")
        return redirect("homepage")
        
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

        if request.POST.get("ProfilePic"):
            profile_photo = request.POST.get("ProfilePic")
        else:
            profile_photo = ""
            
        if password == password2 and len(password) >= 8:
            passcode = password
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username=username, email=email, password=passcode)
                user.first_name = firstname
                user.last_name = lastname
                user.billing_address = billing_address
                user.state = state
                user.profile_pic = profile_photo
                user.save()
                messages.success(request, "Success")
                
                return redirect("dashboardpage") 
            else:
                messages.error(request, "Sorry the email already exists in our database")
                return redirect("homepage")
        elif len(password) < 8:
            messages.error(request, "Please make sure your password is above 8 (eight) characters long!")
            return redirect("homepage")
        else:
            messages.error(request, "Your passwords do not match!")
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
        profile_photo = request.POST.get("ProfilePic")
            
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
                user.profile_pic = profile_photo
                user.set_password(passcode)
                user.save()
                messages.success(request, "Success")
                
                return redirect("dashboardpage") 
            else:
                messages.error(request, f"Wrong email: {email}, or password! \n Please review...")
                return redirect("dashboardpage")
        elif len(password) < 8:
            messages.error(request, "Please make sure your password is above 8 (eight) characters long!")
            return redirect("dashboardpage")
        else:
            messages.error(request, "Your passwords do not match!")
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
    messages.success(request, "Bye! see you later")
    return redirect("homepage")

@login_required
def dashboard(request):
    cart = CartItem.objects.filter(user=request.user, has_ordered=False)
    context = {
        "user": request.user,
        "cart": cart,
    }
    return render(request, "./dashboard.html", context)

@csrf_exempt
@login_required
def add_to_cart(request):
    query = request.POST.getlist("cart_item")
    quantity_amount = request.POST.getlist("quantity_amount")
    for (i, n) in zip(query, quantity_amount):
        item = Product.objects.get(name=i)
        order_item, created = CartItem.objects.get_or_create(
            item = item,
            user = request.user,
            has_ordered = False
        )
        num = int(n) - 1
        order_item.quantity += num
        order_item.save()
        messages.success(request, f"{order_item.item} added to cart!")
    return redirect("dashboardpage")

@login_required
def remove_from_cart(request):
    slug = request.POST["delete"]
    item = Product.objects.get(slug=slug)
    cart_item_to_remove = CartItem.objects.get(
            item = item,
            user = request.user,
            has_ordered = False
        )
    cart_item_to_remove.delete()
    messages.info(request, f"Item '{item}' removed from your cart")
    return redirect("dashboardpage")

@login_required        
def reduce_quantity_item(request):
    slug = request.POST["reduce"]
    item = Product.objects.get(slug=slug)
    order_item = CartItem.objects.get(
        item=item,
        user=request.user,
        has_ordered=False
    )
    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
    else:
        order_item.delete()
    messages.info(request, "Your cart has been updated!")
    return redirect("dashboardpage")

@login_required
def order_view(request):
    cart = CartItem.objects.filter(user=request.user, has_ordered=False)
    if not Order.objects.filter(user=request.user, ordered = False).exists():
        orders = Order.objects.create(user = request.user)
        orders.items.add(*cart)
        messages.info(request, "Go ahead and place your order below")
    elif Order.objects.filter(user=request.user, ordered = False).exists():
        orders = Order.objects.get(user = request.user )
        orders.items.add(*cart)
        messages.info(request, "Go ahead and place your order below")
    else:
        messages.info(request, "Go ahead and place your order below")

    order_summary = Order.objects.all()
    context = {
        "user": request.user,
        "orders": order_summary,
    }
    return render(request, "./order_summary.html", context)

def transaction(request, slug):
    orders = Order.objects.filter(user = request.user, ordered = False)
    if slug == "success":
        for i in orders:
            i.ordered = True
        messages.success(request, "Your orders have successfully been placed!")
    else:
        messages.error(request, "Your orders were not placed successfully, why not try again?")

    return redirect("dashboardpage")

def about(request):
    return render(request, './about.html')

def faqs(request):
    context = {
        "faqs" : Faq.objects.all()
    }
    return render(request, './faq.html', context)

def contact(request):
    return render(request, './contact.html')
    