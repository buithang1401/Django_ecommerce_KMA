from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from phone_field import PhoneField
# Create your models here.

from Web_clothes_1 import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE )
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name_category = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id) +" - "+ self.name_category

class ClothesType(models.Model):
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id) +" - "+ self.type_name

    def get_absolute_url(self):
        return reverse('clothes:type_admin')

class Size(models.Model):
    size = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.size

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_description = models.TextField()
    product_status = models.CharField(max_length=50)
    type_id = models.ForeignKey(ClothesType, on_delete=models.CASCADE)
    product_image = models.ImageField(null=True, blank=True, upload_to="images/")
    product_price = models.FloatField(max_length=50, default=199000)
    quantity = models.IntegerField(default=50)
    size = models.ManyToManyField(Size)
    soled = models.IntegerField(default=0)
    def __str__(self):
        return str(self.id) +" - "+ self.product_name

    def get_absolute_url(self):
        return reverse('clothes:product_admin', kwargs={'pk': self.id})

    def get_add_to_cart_url(self):
        return reverse('clothes:add_to_cart', kwargs={'pk': self.id})

    def get_remove(self):
        return reverse('clothes:remove_from_cart', kwargs={'pk': self.id})

    def get_all_img(self):
        return Product_img.objects.filter(product=self.pk)

    def get_toal_product_soled(self):
        return self.soled * self.product_price


class Customer(models.Model):
    user = models.OneToOneField(User, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    phone_number = PhoneField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    device = models.CharField(max_length=100)
    # def __str__(self):
    #     return  self.user

class Product_img(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.product.product_name +" - "+ str(self.product.id)

class OrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    total = models.FloatField(blank=True, null=True)
    def __str__(self):
        return self.product.product_name +" - "+ str(self.size)+" - "+ str(self.user)

    def get_toal_product_price(self):
        return self.quantity * self.product.product_price

    # def get_total_money_soled(self):
    #     total = 0
    #     for oder_product in self.product.soled:
    #         total += oder_product.get_toal_product_soled()
    #     return total
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True )
    products = models.ManyToManyField(OrderProduct)
    # start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    payment_status = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for oder_product in self.products.all():
            total += oder_product.get_toal_product_price()
        return total
