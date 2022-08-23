from django import  template
from django.contrib.auth.models import User
import datetime
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
def money_soled_by_month(user):
    if user.is_authenticated:
        d1 = datetime.date.today()
        d2 = d1 - datetime.timedelta(30)
        qs =Order.objects.filter(ordered_date__gt=d2).values_list('products__total')
        if qs.exists():
            total = 0
            for i in qs:
                total += i[0]
            return total
    return 0

@register.filter
def order_by_month(user):
    if user.is_authenticated:
        today = datetime.date.today()
        month_ago = today - datetime.timedelta(30)
        qs =Order.objects.filter(ordered_date__gt=month_ago, ordered=True)
        print(qs)
        if qs.exists():
            total = qs.count()
            print(total)
            return total
    return 0
@register.filter
def interest_by_month(user):
    if user.is_authenticated:
        d1 = datetime.date.today()
        d2 = d1 - datetime.timedelta(30)
        qs =Order.objects.filter(ordered_date__gt=d2).values_list('products__total')
        if qs.exists():
            total = 0
            for i in qs:
                total += i[0]
            return total/100*58
    return 0
@register.filter
def money_soled(user):
    if user.is_authenticated:
        qs =Order.objects.values_list('products__total')
        if qs.exists():
            total = 0
            for i in qs:
                total += i[0]
            return total
    return 0

@register.filter
def cart_item_count_anonymous(request):
    try:
        device = request.COOKIES['device']
        qs = Order.objects.filter(user__customer__device=device, ordered=False)
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
    try:
        return int(value)
    except ValueError:
        return 0