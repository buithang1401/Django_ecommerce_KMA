from django import  template
from django.contrib.auth.models import User

from clothes.models import Order, OrderProduct, Product

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].products.count()
    return 0

@register.filter
def money_soled(user):
    if user.is_authenticated:
        qs = Product.objects.filter(soled__gt=0).all()
        if qs.exists():
            total = 0
            for i in qs:
                total += i.soled * i.product_price
            return total
    return 0

@register.filter
def cart_item_count_anonymous(request):
    try:
        device = request.COOKIES['device']
        qs = Order.objects.filter(user__customer__device=device, ordered=False)
        print(qs)
        if qs.exists():
            return qs[0].products.count()
        else:
            return 0
    except:
        return 0

@register.filter
def show_admin(user):
    if user.is_authenticated:
        admin = User.objects.filter(username=user)
        if admin.exists():
            return admin[0].username
    return None

@register.filter()
def to_int(value):
    return int(value)