from django.contrib import admin

# Register your models here.
from clothes.models import Category, Product, ClothesType, Profile, Product_img, OrderProduct, Order, Customer, Size, PaymentModel

admin.site.register(Category)
admin.site.register(ClothesType)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Customer)
admin.site.register(Size)
admin.site.register(PaymentModel)


class ProductImageAdmin(admin.StackedInline):
    model = Product_img

@admin.register(Product)
class Product_admin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

    class Meta:
        model=Product