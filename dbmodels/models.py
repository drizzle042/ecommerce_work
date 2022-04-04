from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import CASCADE
from django.shortcuts import reverse

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=80, blank=True)
    billing_address = models.TextField(blank=True)
    state = models.CharField(max_length=80, blank=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

class Subscriber(models.Model):
    email = models.EmailField(unique=True, serialize=True)

    def __str__(self) -> str:
        return self.email

class Faq(models.Model):
    question = models.TextField(unique=True)
    answer = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.question
        
class Product(models.Model):
    mainCategoryChoices = [
        ('fashion', 'fashion'),
        ('meat-and-seafood', 'meat-and-seafood'),
        ('kitchen-tools', 'kitchen-tools'),
        ('cook-ware', 'cook-ware'),
        ('oil-vinegar', 'oil-vinegar'),
        ('fast-food', 'fast-food'),
        ('snack-food', 'snack-food'),
        ('organic-food', 'organic-food'),
    ]
    name = models.CharField(max_length=120, unique=True, serialize=True)
    slug = models.SlugField(allow_unicode=True, unique=True, serialize=True)
    price = models.IntegerField(serialize=True)
    discount = models.IntegerField(blank=True, serialize=True, default=0)
    mainImage = models.ImageField()
    mainCategory = models.CharField(max_length=30, choices=mainCategoryChoices, serialize=True)
    subCategory = models.CharField(max_length=30, serialize=True)
    description = models.TextField(blank=True, help_text="Product details", serialize=True)
    date = models.DateTimeField(auto_now=True, serialize=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("detailspage", kwargs={
            "pk": self.pk
        })
    
    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            "pk": self.pk
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            "pk": self.pk
        })

class Product_image(models.Model):
    name = models.ForeignKey(to=Product, on_delete= CASCADE, serialize=True)
    images = models.ImageField()
    
    def __str__(self) -> str:
        return self.name.name

class CartItem(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=CASCADE)
    item = models.ForeignKey(to=Product, on_delete=CASCADE)
    has_ordered = models.BooleanField(default=False)
    quantity = models.SmallIntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.quantity} {self.item.name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount(self):
        return self.quantity * self.item.discount

    def get_total_final_price(self):
        return self.get_total_item_price() - self.get_total_discount()

    def get_total_amount_saved(self):
        return self.get_total_item_price() - self.get_total_final_price()

class Order(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=CASCADE)
    items = models.ManyToManyField(CartItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def get_total_price(self):
        total_amount = 0
        for n in self.items.all():
            total_amount += n.get_total_final_price()
        return total_amount

    def __str__(self) -> str:
        return self.user.username