from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.

class Subscriber(models.Model):
    email = models.EmailField(unique=True, serialize=True)

    def __str__(self) -> str:
        return self.email

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
    discount = models.IntegerField(blank=True, serialize=True)
    mainImage = models.ImageField()
    mainCategory = models.CharField(max_length=30, choices=mainCategoryChoices, serialize=True)
    subCategory = models.CharField(max_length=30, serialize=True)
    description = models.TextField(blank=True, help_text="Product details", serialize=True)
    date = models.DateTimeField(auto_now=True, serialize=True)

    def __str__(self) -> str:
        return self.name

class Product_image(models.Model):
    name = models.ForeignKey(to=Product, on_delete= CASCADE, serialize=True)
    images = models.ImageField()
    
    def __str__(self) -> str:
        return self.name.name