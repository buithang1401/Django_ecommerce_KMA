from random import randint, uniform

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from clothes.forms import CheckoutForm
from clothes.models import Product, OrderProduct, Order, Product_img, Customer, Size
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

#--------------- home index view ----------------------
def HomeClass(request):
    aophongnam = Product.objects.filter(category_id_id=1, type_id_id=1).order_by("-soled")[:4]
    aopolonam = Product.objects.filter(category_id_id=1, type_id_id=2).order_by("-soled")[:4]
    quanjeannam = Product.objects.filter(category_id_id=1, type_id_id=3).order_by("-soled")[:4]
    # orser = Oder
    return render(request, 'clothes/web_site/index_site.html', {"aophongnam":aophongnam, "aopolonam":aopolonam, "quanjeannam":quanjeannam})


# ---------------  men clothes view ------------------
class ClothesMenView(ListView):
    template_name = 'clothes/web_site/men_site_clothes/quan_ao_nam.html'
    def get_queryset(self):
        return Product.objects.filter(category_id_id=1).all()

class AoPhongNamView(ListView):
    template_name = 'clothes/web_site/men_site_clothes/ao_phong_nam.html'
    # paginate_by = 6
    def get_queryset(self):
        return Product.objects.filter(category_id_id=1, type_id_id=1).all()

class AoPoloNamView(ListView):
    template_name = 'clothes/web_site/men_site_clothes/ao_polo_nam.html'
    def get_queryset(self):
        return Product.objects.filter(category_id_id=1, type_id_id=2).all()

class QuanJeanNamView(ListView):
    template_name = 'clothes/web_site/men_site_clothes/quan_jean_nam.html'
    def get_queryset(self):
        return Product.objects.filter(category_id_id=1, type_id_id=3).all()

class QuanShortNamView(ListView):
    template_name = 'clothes/web_site/men_site_clothes/quan_short_nam.html'
    def get_queryset(self):
        return Product.objects.filter(category_id_id=1, type_id_id=4).all()

#------------- product detail , add to cart, payment ----------------------------
class ItemDetail(DetailView):
    model = Product
    template_name = 'clothes/web_site/men_site_clothes/ao_phong_nam_detail.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['img'] = Product_img.objects.filter(product=self.kwargs['pk'])
        context['size'] = Size.objects.all()
        return context

# @login_required(login_url='/login/')
def add_to_cart(request, pk):
    quantity = request.POST.get('quantity')
    size = request.POST.get('size')
    product = get_object_or_404(Product, pk=pk)
    if request.user.is_authenticated:
            order_qs = Order.objects.filter(user=request.user, ordered=False)
            if order_qs.exists():
                order = order_qs[0]
                exist_product_order = order.products.filter(product__id=product.pk, size=size)
                if exist_product_order.exists():
                    for i in exist_product_order:
                        i.quantity = int(i.quantity) + int(quantity)
                        i.total = float(i.total) + float(product.product_price) * float(quantity)
                        i.save()
                    messages.info(request, "Cập nhật số lượng thành công")
                    return redirect("clothes:product_detail", pk=pk)
                else:
                    order.products.add(OrderProduct.objects.create(
                        product=product,
                        quantity=quantity,
                        user=request.user,
                        size=size,
                        total=float(quantity) * float(product.product_price),
                        ordered=False
                    ))
                    messages.info(request, "Đã thêm vào giỏ hàng")
                    return redirect("clothes:product_detail", pk=pk)
            else:
                ordered_date = timezone.now()
                order = Order.objects.create(user=request.user, ordered_date=ordered_date)
                order.products.add(OrderProduct.objects.create(
                    product=product,
                    quantity=quantity,
                    user=request.user,
                    size=size,
                    total=float(quantity) * float(product.product_price),
                    ordered=False
                ))
                messages.info(request, "Đã thêm vào giỏ hàng")
                return redirect("clothes:product_detail", pk=pk)
            return redirect("clothes:product_detail", pk=pk)
    else:
        device = request.COOKIES['device']
        if Customer.objects.filter(device=device).exists():
            u = get_object_or_404(User, customer__device__exact=device)
            print(u)
            order_qs = Order.objects.filter(user__customer__device__exact=device, ordered=False)
            if order_qs.exists():
                order = order_qs[0]
                exist_product_order = order.products.filter(product__id=product.pk, size=size)
                if exist_product_order.exists():
                    for i in exist_product_order:
                        i.quantity = int(i.quantity) + int(quantity)
                        i.total = float(i.total) + float(product.product_price) * float(quantity)
                        i.save()
                    messages.info(request, "Cập nhật số lượng thành công")
                    return redirect("clothes:product_detail", pk=pk)
                else:
                    order.products.add(OrderProduct.objects.create(
                        product=product,
                        quantity=quantity,
                        user=u,
                        size=size,
                        total=float(quantity) * float(product.product_price),
                        ordered=False
                    ))
                    messages.info(request, "Đã thêm vào giỏ hàng")
                    return redirect("clothes:product_detail", pk=pk)
        else:
            #tao user anonymous
            username = randint(1, 10)
            try:
                u = User.objects.create(username=username, first_name='', last_name='')
                u.set_unusable_password()
                u.save()
                Customer.objects.create(user=u , device=device)
                my_group = Group.objects.get(name='customer')
                my_group.user_set.add(u)
                ordered_date = timezone.now()
                order = Order.objects.create(user=u, ordered_date=ordered_date)
                order.products.add(OrderProduct.objects.create(
                    product=product,
                    quantity=quantity,
                    user=u,
                    size=size,
                    total=float(quantity) * float(product.product_price),
                    ordered=False
                ))
                messages.info(request, "Đã thêm vào giỏ hàng")

            except:
                username = randint(1, 10)
                print("except")
                u = User(username=username, first_name='', last_name='')
                u.set_unusable_password()
                u.save()
                Customer.objects.create(user=u)
                ordered_date = timezone.now()
                order = Order.objects.create(user=u, ordered_date=ordered_date)
                order.products.add(OrderProduct.objects.create(
                    product=product,
                    quantity=quantity,
                    user=u,
                    size=size,
                    total=float(quantity) * float(product.product_price),
                    ordered=False
                ))
                messages.info(request, "Đã thêm vào giỏ hàng")
        return redirect("clothes:product_detail", pk=pk)


def remove_from_cart(request, pk):
    print("vao day")
    size = request.POST.get('size_in_pay')
    print(size)
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        exist_product_order = order.products.filter(product__id=product.pk, size=size)
        print(exist_product_order)
        if exist_product_order.exists():
            for i in exist_product_order:
                i.quantity = int(i.quantity) - 1
                i.total = float(i.total) - float(product.product_price)
                if i.quantity==0:
                    exist_product_order.delete()
                    messages.info(request, "Đã xoá sản phẩm")
                i.save()
            return redirect("clothes:payment")
        else:
            return redirect("clothes:payment", pk=pk)
    else:
        return redirect("clothes:payment", pk=pk)

def add_single_to_cart(request, pk):
    size = request.POST.get('size_in_pay')
    print(size)
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        exist_product_order = order.products.filter(product__id=product.pk, size=size )
        if exist_product_order.exists():
            for i in exist_product_order:
                i.quantity = int(i.quantity) + 1
                i.total = float(i.total) + float(product.product_price)
                i.save()
            return redirect("clothes:payment")
        else:
            return redirect("clothes:payment", pk=pk)
    else:
        return redirect("clothes:payment", pk=pk)

class Payment(View):
    def get(self, request, *args, **kwargs, ):
        try:
            try:
                print("vao try")
                user = Customer.objects.filter(user=request.user)
                order = Order.objects.get(user=self.request.user, ordered=False)
                if user.exists():
                    user1 = Customer.objects.get(user=self.request.user)
                    context = {
                        'object': order,
                        'user':user1
                    }
                    return render(self.request, 'clothes/web_site/pay.html', context)
                else:
                    context = {
                        'object': order,
                    }
                    return render(self.request, 'clothes/web_site/pay.html', context)

            except:
                print("vao except")
                device = request.COOKIES['device']
                user = Customer.objects.filter(device=device)
                order = Order.objects.get(user__customer__device__exact=device, ordered=False)
                context = {
                    'object': order,
                }
                return render(self.request, 'clothes/web_site/pay.html', context)
        except:
            print("vao else")
            return render(self.request, 'clothes/web_site/pay.html')
    def post(self, request, *args, **kwargs):
        try:
            try:
                print("vao try")
                customer_name = request.POST.get('ten_khachhang')
                customer_email = request.POST.get('email_khachhang')
                customer_phone = request.POST.get('sdt_khachhang')
                customer_address = request.POST.get('diachi_nhanhang')
                payment_method = request.POST.get('exampleRadios')
                print(customer_phone, customer_address, customer_email, customer_name, payment_method)
                user = Customer.objects.filter(user=request.user)
                if user.exists():
                    user_exisited = user.get(user=request.user)
                else:
                    new_customer = Customer()
                    new_customer.user = request.user
                    new_customer.address = customer_address
                    new_customer.phone_number = customer_phone
                    new_customer.save()
                    print("tao user r")

                if payment_method=="option1":
                    print("thanh toan khi nhan hang")
                    return redirect('clothes:confirm_checkout')
                else:
                    print("thanh toan qua chuyen khoan ngan hang")
                    return redirect('clothes:home')
            except:
                print("vao except")
                device = request.COOKIES['device']
                customer_name = request.POST.get('ten_khachhang')
                customer_email = request.POST.get('email_khachhang')
                customer_phone = request.POST.get('sdt_khachhang')
                customer_address = request.POST.get('diachi_nhanhang')
                payment_method = request.POST.get('exampleRadios')
                print(customer_phone, customer_address, customer_email, customer_name, payment_method)
                Customer.objects.filter(device=device, ).update(
                    name = customer_name,
                    email= customer_email,
                    address = customer_address,
                    phone_number = customer_phone,
                )

                if payment_method=="option1":
                    print("thanh toan khi nhan hang")
                    return redirect('clothes:confirm_checkout')
                else:
                    print("thanh toan qua chuyen khoan ngan hang")
                    return redirect('clothes:online_payment')
                return redirect('clothes:login')
        except:
            messages.info(request, "Bạn chưa có sản phảm nào trong giỏ hàng!")
            return redirect("clothes:payment")


class Checkout_view(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm
        context = {
            'form':form
        }
        return render(self.request, 'clothes/web_site/pay.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            print("the form is valid")
            return redirect('clothes:payment')

class ConfirmCheckout(View):
    def get(self, request, *args, **kwargs):
        try:
            user = Customer.objects.get(user=self.request.user)
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order,
                'user': user
            }
            return render(self.request, 'clothes/web_site/confrim_payment.html',context)
        except:
            device = request.COOKIES['device']
            user = Customer.objects.get(device=device)
            order = Order.objects.get(user__customer__device__exact=device, ordered=False)
            context = {
                'object': order,
                'user': user
            }

            return render(self.request, 'clothes/web_site/confrim_payment.html', context)
    def post(self, request, *args, **kwargs):
        try:
            Order.objects.filter(user=self.request.user).update(ordered=True)
            messages.info(request, "Đã hoàn tất đơn hàng, mời bạn tiếp tục mua sắm")
            return redirect("clothes:home")
        except:
            device = request.COOKIES['device']
            Order.objects.filter(user__customer__device__exact=device).update(ordered=True)
            # order = Order.objects.get(user=self.request.user, ordered=False)
            # # Product.objects.filter()
            # order.products.update(soled=1, quantity=45)
            messages.info(request, "Đã hoàn tất đơn hàng, mời bạn tiếp tục mua sắm")
            return redirect("clothes:home")

#online method
class OnlinePayment(ListView):
    model = Order
    template_name = 'clothes/web_site/online_payment.html'
class OnlinePayment1(ListView):
    model = Order
    template_name = 'clothes/web_site/online_payment2.html'

#search in Website
def search_data(request):
    if request.method == "POST":
        search_data = request.POST['search_data']
        match_data = Product.objects.filter(product_name__contains=search_data).all()
        return render(request,'clothes/web_site/search_data.html', {'search_data': search_data, 'match_data':match_data})
    else:
        return render(request, 'clothes/web_site/index_site.html', {})