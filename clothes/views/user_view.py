import datetime
from random import randint
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.views import View
from django.views.generic import ListView, DetailView

from clothes.forms import CheckoutForm
from clothes.models import Product, OrderProduct, Order, Product_img, Customer, Size, PaymentModel
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

import stripe
# stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"
stripe.api_key=settings.STRIPE_SECRET_KEY

#--------------- home index view ----------------------
def HomeClass(request):
    aophongnam = Product.objects.filter(category_id_id=1, type_id_id=1).order_by("-soled")[:4]
    aopolonam = Product.objects.filter(category_id_id=1, type_id_id=2).order_by("-soled")[:4]
    quanjeannam = Product.objects.filter(category_id_id=1, type_id_id=3).order_by("-soled")[:4]
    # orser = Oder
    return render(request, 'clothes/web_site/index_site.html', {"aophongnam":aophongnam, "aopolonam":aopolonam, "quanjeannam":quanjeannam})

def HomeBaseClass(request):
    try:
        order_cart_tag = Order.objects.filter(user=request.user, ordered=False).all()
    except:
        device = request.COOKIES['device']
        order_cart_tag = ""
    return render(request, 'clothes/web_site/base.html', {"order_cart_tag":order_cart_tag})
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
                    messages.success(request, "Cập nhật số lượng thành công", extra_tags='success')
                    return redirect("clothes:product_detail", pk=pk)
                else:
                    order.products.add(OrderProduct.objects.create(
                        product=product,
                        quantity=quantity,
                        user=request.user,
                        size=size,
                        total=float(quantity) * float(product.product_price),
                    ))
                    messages.success(request, "Đã thêm vào giỏ hàng" , extra_tags='success')
                    return redirect("clothes:product_detail", pk=pk)
            else:
                ordered_date = datetime.datetime.now()
                print(ordered_date)
                order = Order.objects.create(user=request.user, ordered_date=ordered_date)
                order.products.add(OrderProduct.objects.create(
                    product=product,
                    quantity=quantity,
                    user=request.user,
                    size=size,
                    total=float(quantity) * float(product.product_price),
                ))
                messages.success(request, "Đã thêm vào giỏ hàng", extra_tags='success')
                return redirect("clothes:product_detail", pk=pk)
            return redirect("clothes:product_detail", pk=pk)
    else:
        device = request.COOKIES['device']
        if Customer.objects.filter(device=device).exists():
            u = get_object_or_404(User, customer__device__exact=device)
            order_qs = Order.objects.filter(user__customer__device__exact=device, ordered=False)
            if order_qs.exists():
                order = order_qs[0]
                exist_product_order = order.products.filter(product__id=product.pk, size=size)
                if exist_product_order.exists():
                    for i in exist_product_order:
                        i.quantity = int(i.quantity) + int(quantity)
                        i.total = float(i.total) + float(product.product_price) * float(quantity)
                        i.save()
                    messages.success(request, "Cập nhật số lượng thành công", extra_tags='success')
                    return redirect("clothes:product_detail", pk=pk)
                else:
                    order.products.add(OrderProduct.objects.create(
                        product=product,
                        quantity=quantity,
                        user=u,
                        size=size,
                        total=float(quantity) * float(product.product_price),
                    ))
                    messages.success(request, "Đã thêm vào giỏ hàng", extra_tags='success')
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
                ordered_date = datetime.datetime.now()
                order = Order.objects.create(user=u, ordered_date=ordered_date)
                order.products.add(OrderProduct.objects.create(
                    product=product,
                    quantity=quantity,
                    user=u,
                    size=size,
                    total=float(quantity) * float(product.product_price),
                ))
                messages.success(request, "Đã thêm vào giỏ hàng", extra_tags='success')

            except:
                username = randint(1, 10)
                print("except")
                u = User(username=username, first_name='', last_name='')
                u.set_unusable_password()
                u.save()
                Customer.objects.create(user=u)
                ordered_date = datetime.datetime.now()
                order = Order.objects.create(user=u, ordered_date=ordered_date)
                order.products.add(OrderProduct.objects.create(
                    product=product,
                    quantity=quantity,
                    user=u,
                    size=size,
                    total=float(quantity) * float(product.product_price),
                ))
                messages.success(request, "Đã thêm vào giỏ hàng", extra_tags='success')
        return redirect("clothes:product_detail", pk=pk)


def remove_from_cart(request, pk):
    size = request.POST.get('size_in_pay')
    product = get_object_or_404(Product, pk=pk)
    if request.user.is_authenticated:
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
                        messages.success(request, "Đã xoá sản phẩm", extra_tags='success')
                    i.save()
                return redirect("clothes:payment")
            else:
                return redirect("clothes:payment", pk=pk)
        else:
            return redirect("clothes:payment", pk=pk)
    else:
        device = request.COOKIES['device']
        order_qs = Order.objects.filter(user__customer__device=device, ordered=False)
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
                        messages.success(request, "Đã xoá sản phẩm", extra_tags='success')
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
    if request.user.is_authenticated:
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
    else:
        device = request.COOKIES['device']
        order_qs = Order.objects.filter(user__customer__device=device, ordered=False)
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
                user = Customer.objects.filter(device=device).all()
                order = Order.objects.get(user__customer__device__exact=device, ordered=False)
                print(user)
                context = {
                    'user': user,
                    'object': order,
                }
                return render(self.request, 'clothes/web_site/pay.html', context)
        except:
            print("vao else")
            return render(self.request, 'clothes/web_site/pay.html')
    def post(self, request, *args, **kwargs):
        try:
            try:
                customer_name = request.POST.get('ten_khachhang')
                customer_email = request.POST.get('email_khachhang')
                customer_phone = request.POST.get('sdt_khachhang')
                customer_address = request.POST.get('diachi_nhanhang')
                payment_method = request.POST.get('exampleRadios')
                user = Customer.objects.filter(user=request.user)
                if user.exists():
                    Customer.objects.filter(user=request.user).update(phone_number=customer_phone)
                else:
                    new_customer = Customer()
                    new_customer.user = request.user
                    new_customer.name = customer_name
                    new_customer.email = customer_email
                    new_customer.address = customer_address
                    new_customer.phone_number = customer_phone
                    new_customer.save()

                if payment_method=="option1":  #thanh toan COD
                    print("thanh toan khi nhan hang")
                    Order.objects.filter(user=request.user, ordered=False).update(
                        payment_method="COD",
                        shipping_address=customer_address
                    )
                    return redirect('clothes:confirm_checkout')
                else:  #Thanh toan online
                    Order.objects.filter(user=request.user, ordered=False).update(
                        payment_method="Online_Banking",
                        shipping_address=customer_address
                    )
                    print("thanh toan qua chuyen khoan ngan hang")
                    return redirect('clothes:online_payment')
            except:
                device = request.COOKIES['device']
                customer_name = request.POST.get('ten_khachhang')
                customer_email = request.POST.get('email_khachhang')
                customer_phone = request.POST.get('sdt_khachhang')
                customer_address = request.POST.get('diachi_nhanhang')
                payment_method = request.POST.get('exampleRadios')
                Customer.objects.filter(device=device, ).update(
                    name=customer_name,
                    email=customer_email,
                    address=customer_address,
                    phone_number=customer_phone,
                )

                if payment_method=="option1":
                    print("thanh toan khi nhan hang")
                    Order.objects.filter(user__customer__device=device, ordered=False).update(
                        payment_method="COD",
                        shipping_address=customer_address
                    )
                    return redirect('clothes:confirm_checkout')
                else:
                    Order.objects.filter(user__customer__device=device, ordered=False).update(
                        payment_method="Online_Banking",
                        shipping_address=customer_address
                    )
                    print("thanh toan qua chuyen khoan ngan hang")
                    return redirect('clothes:online_payment')
        except:
            messages.warning(request, "Bạn chưa có sản phảm nào trong giỏ hàng!" , extra_tags='error')
            return redirect("clothes:payment")

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
            messages.success(request, "Đã hoàn tất đơn hàng, mời bạn tiếp tục mua sắm", extra_tags='success')
            return redirect("clothes:home")
        except:
            device = request.COOKIES['device']
            Order.objects.filter(user__customer__device__exact=device).update(ordered=True)
            # order = Order.objects.get(user=self.request.user, ordered=False)
            # # Product.objects.filter()
            # order.products.update(soled=1, quantity=45)
            messages.success(request, "Đã hoàn tất đơn hàng, mời bạn tiếp tục mua sắm", extra_tags='success')
            return redirect("clothes:home")

#online method
class OnlinePayment(View):
    def get(self, request, *args, **kwargs):
        try:
            user = Customer.objects.get(user=self.request.user)
            order = Order.objects.get(user=self.request.user, ordered=False)

            if order:
                context = {
                    'order': order,
                    'DISPLAY_COUPON_FORM': False,
                    'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
                    'user': user,
                }
            return render(self.request, 'clothes/web_site/card_payment1.html', context)
        except:
            device = request.COOKIES['device']
            user = Customer.objects.get(device=device)
            order = Order.objects.get(user__customer__device=device , ordered=False)
            if order:
                context = {
                    'order': order,
                    'DISPLAY_COUPON_FORM': False,
                    'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
                    'user': user,
                }
            return render(self.request, 'clothes/web_site/card_payment1.html', context)
    def post(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            token = self.request.POST.get('stripeToken')
            amount = int(order.get_total())
            try:

                charge = stripe.Charge.create(
                    amount=amount,
                    currency="usd",
                    source=token,
                )
                print('try payment')
                # create the payment
                payment = PaymentModel()
                payment.stripe_charge_id = charge['id']
                payment.user = self.request.user
                payment.amount = order.get_total()
                payment.save()
                order.ordered = True
                order.paymnent = payment
                order.save()

                messages.success(self.request, "Bạn đã thanh toán đơn hàng thành công, hãy xem lại trong Đơn hàng nhé !!!" , extra_tags='success')
                return redirect('clothes:home')

            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, f"{err.get('message')}")
                return redirect("/")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error")
                return redirect("/")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                messages.warning(self.request, "Invalid parameters")
                return redirect("/")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(self.request, "Not authenticated")
                return redirect("/")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, "Network error")
                return redirect("/")

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(self.request, "Something went wrong. You were not charge. Please try again")
                return redirect("/")

            except Exception as e:
                # Something else happened, completely unrelated to Stripe
                messages.warning(self.request, "A serious error occurred. We have been notifed")
                return redirect("/")

        #online payment with anonymous
        except:
            device = request.COOKIES['device']
            user = get_object_or_404(User, customer__device__exact=device)
            order = Order.objects.get(user__customer__device=device, ordered=False)
            token = self.request.POST.get('stripeToken')
            amount = int(order.get_total())
            try:

                charge = stripe.Charge.create(
                    amount=amount,
                    currency="usd",
                    source=token,
                )
                print('try payment')
                # create the payment
                payment = PaymentModel()
                payment.stripe_charge_id = charge['id']
                payment.user = user
                payment.amount = order.get_total()
                payment.save()
                order.ordered = True
                order.paymnent = payment
                order.save()

                messages.success(self.request, "Bạn đã thanh toán đơn hàng thành công, hãy xem lại trong Đơn hàng nhé !!!", extra_tags='success')
                return redirect('clothes:home')

            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, f"{err.get('message')}")
                return redirect("/")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error")
                return redirect("/")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                messages.warning(self.request, "Invalid parameters")
                return redirect("/")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(self.request, "Not authenticated")
                return redirect("/")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, "Network error")
                return redirect("/")

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(self.request, "Something went wrong. You were not charge. Please try again")
                return redirect("/")

            except Exception as e:
                # Something else happened, completely unrelated to Stripe
                messages.warning(self.request, "A serious error occurred. We have been notifed")
                return redirect("/")

#search in Website
def search_data(request):
    if request.method == "POST":
        search_data = request.POST['search_data']
        match_data = Product.objects.filter(product_name__contains=search_data).all()
        return render(request,'clothes/web_site/search_data.html', {'search_data': search_data, 'match_data':match_data})
    else:
        return render(request, 'clothes/web_site/index_site.html', {})


class OrderManage(View):
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.filter(user=request.user, ordered=True).order_by('-ordered_date').all()
            user = Customer.objects.filter(user=request.user).all()
        except:
            # device = request.COOKIES['device']
            # order = Order.objects.filter(user__customer__device=device, ordered=True).order_by('-ordered_date').all()
            messages.warning(request, "Bạn chưa có đơn hàng nào! Hãy tiếp tục mua sắm" , extra_tags='error')
            return redirect('/')
        return render(request, 'clothes/web_site/customer_manage_order.html', {'order':order, 'user':user})
    def post(self, request, *args, **kwargs):
        id = request.POST.get('id_Don_hang')
        feedback = request.POST.get('danhgia')
        if 'danhanhang' in request.POST:
            messages.success(self.request, "Cảm ơn bạn vì đã tin dùng sản phảm của chúng tôi !!!", extra_tags='success')
            Order.objects.filter(id=id).update(payment_status=True)
        elif 'guidanhgia' in request.POST:
            print("vao gui danh gia")
            if feedback != []:
                messages.success(self.request, "Cảm ơn những đánh giá của bạn, nếu hài lòng hãy tiếp tục mua hàng nhé !!!", extra_tags='success')
                Order.objects.filter(id=id).update(feedback=feedback)
            else:
                messages.warning(request, "Hãy cho chúng tôi xin đánh giá của bạn trước khi gửi đánh giá nhé", extra_tags='error')
                return redirect("clothes:manage_order")
        return redirect("clothes:manage_order")