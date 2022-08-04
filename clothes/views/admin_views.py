import uuid
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
import collections
from clothes.decorators import unauthenticated_user, allow_users
from clothes.forms import ProductForm, TypeForm, CateForm, UserForm
from clothes.models import Product, ClothesType, Category, Profile, Customer, Order, OrderProduct
from clothes.helpers import send_forget_password_mail

#login
@unauthenticated_user
def Login(request):
    if request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('pass_word')
        my_user = authenticate(username=username, password=password)
        if my_user is None:
            return render(request, 'clothes/login/login_site.html', {'alert_flag': True})
        login(request, my_user)
        return redirect('clothes:admin_view')
    return render(request, 'clothes/login/login_site.html')

def Logout(request):
    logout(request)
    return redirect('clothes:login')
class Register(View):
    def get(self, request):
        return render(request, 'clothes/login/register.html')
    def post(self, request):
        username = request.POST.get('user_name')
        password = request.POST.get('pass_word')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')


        if User.objects.filter(username=username).first():
            return render(request, 'clothes/login/register.html', {'alert_flag1': True})
        if User.objects.filter(email=email).first():
            return render(request, 'clothes/login/register.html', {'alert_flag2': True})

        user_obj = User(username=username, email=email, first_name=first_name, last_name=last_name)
        user_obj.set_password(password)
        user_obj.save()

        Customer.objects.create(
            user=user_obj,
            name=first_name + " " + last_name,
            email=email
        )

        profile_obj = Profile.objects.create(user=user_obj)
        profile_obj.save()
        return render(request, 'clothes/login/login_site.html', {'alert_flag3': True})

class FogetPassword(View):
    def get(self, request):
        return render(request, 'clothes/login/forget_password.html')
    def post(self, request):
        username = request.POST.get('user_name')
        if not User.objects.filter(username=username).first():
            return render(request, 'clothes/login/forget_password.html', {'alert_flag': True})
        user_obj = User.objects.get(username=username)
        token = str(uuid.uuid4())
        profile_obj = Profile.objects.get(user=user_obj)
        profile_obj.forget_password_token = token
        profile_obj.save()
        send_forget_password_mail(user_obj.email, token)
        return render(request, 'clothes/login/forget_password.html', {'alert_flag1': True})

def ChangePassword(request, token):
    context = {}
    try:
        profile_obj = Profile.objects.get(forget_password_token=token)
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                return render(request, 'clothes/login/change_password.html', {'alert_flag1': True})
            if new_password != confirm_password:
                return render(request, 'clothes/login/change_password.html', {'alert_flag2': True})

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('clothes:login')
        context = {'user_id' : profile_obj.user_id}
    except Exception as e:
        print(e)
    return render(request, 'clothes/login/change_password.html', context)


#admin home
@login_required(login_url='/login/')
@allow_users(allowed_roled=['admin'])
def AdminView(request):
    product = Product.objects.all()
    type = ClothesType.objects.all()
    category = Category.objects.all()
    money_soled = OrderProduct.objects.all()
    return render(request, 'clothes/admin_site/index.html', {"product": product, "type": type, "category": category, "money_soled": money_soled})
def TableAdminView(request):
    product = Product.objects.all()
    type = ClothesType.objects.all()
    category = Category.objects.all()
    # orser = Oder
    return render(request, 'clothes/admin_site/tables.html', {"product":product, "type":type, "category":category})

class ChartAdminView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model = Product
    template_name = 'clothes/admin_site/charts.html'

class UserDisplay(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model = User
    template_name = 'clothes/admin_site/admin_base.html'

# admin manage product ---------------------------
class AddProduct(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    template_name = 'clothes/admin_site/product/product_add.html'
    form_class = ProductForm
    success_url = reverse_lazy('clothes:product_admin')

class ProductAdminView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model = Product
    template_name = 'clothes/admin_site/product/product_table.html'

class UpdateProduct(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    model = Product
    template_name = 'clothes/admin_site/product/product_update.html'
    form_class = ProductForm
class DeleteProduct(LoginRequiredMixin,DeleteView):
    login_url = '/login/'
    model = Product
    template_name = 'clothes/admin_site/product/product_delete.html'
    success_url = reverse_lazy('clothes:product_admin')

# admin manage type ----------------------------
class TypeAdminView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model = ClothesType
    template_name = 'clothes/admin_site/type/type_table.html'

class AddType(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    template_name = 'clothes/admin_site/type/type_add.html'
    form_class = TypeForm
    success_url = reverse_lazy('clothes:type_admin')

class UpdateType(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    model = ClothesType
    template_name = 'clothes/admin_site/type/type_update.html'
    form_class = TypeForm

class DeleteType(LoginRequiredMixin,DeleteView):
    login_url = '/login/'
    model = ClothesType
    template_name = 'clothes/admin_site/type/type_delete.html'
    success_url = reverse_lazy('clothes:type_admin')

# admin manage category ----------------------------
class CateAdminView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model = Category
    template_name = 'clothes/admin_site/category/category_table.html'

class AddCate(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    template_name = 'clothes/admin_site/category/category_add.html'
    form_class = CateForm
    success_url = reverse_lazy('clothes:type_admin')

class UpdateCate(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    model = Category
    template_name = 'clothes/admin_site/category/category_update.html'
    form_class = TypeForm

class DeleteCate(LoginRequiredMixin,DeleteView):
    login_url = '/login/'
    model = Category
    template_name = 'clothes/admin_site/category/category_delete.html'
    success_url = reverse_lazy('clothes:type_admin')

# admin manage user ----------------------------
class UserAdminView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model = User
    template_name = 'clothes/admin_site/user/user_table.html'

class AddUser(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    template_name = 'clothes/admin_site/user/user_add.html'
    form_class = UserForm
    success_url = reverse_lazy('clothes:user_admin')

class UpdateUser(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    model = User
    template_name = 'clothes/admin_site/user/user_update.html'
    form_class = UserForm

class DeleteUser(LoginRequiredMixin,DeleteView):
    login_url = '/login/'
    model = User
    template_name = 'clothes/admin_site/user/user_delete.html'
    success_url = reverse_lazy('clothes:user_admin')

#admin manager customer
class CusAdminView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model = Customer
    template_name = 'clothes/admin_site/customer/cus_table.html'

#admin manager order
class OrderAdminView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model = Order
    template_name = 'clothes/admin_site/order/order_table.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['customer'] = Customer.objects.all()
        context['order_product'] = OrderProduct.objects.all()
        return context

#admin manager order
class OrderStaticAdminView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        product = Product.objects.all().order_by('-soled')

        customer = Customer.objects.all()
        order_product = OrderProduct.objects.all()
        context = {
            "product":product
        }
        return render(request, 'clothes/admin_site/order/order_static.html', context )
    def post(self, request, *args, **kwargs):
        date_start = request.POST.get('date_start')
        date_end = request.POST.get('date_end')
        number_of_top = request.POST.get('number_of_top')
        order_in_time = Order.objects.filter(ordered_date__range=[date_start, date_end], ordered=True).order_by('-ordered_date')
        top_product = OrderProduct.objects.filter(order__ordered_date__range=[date_start, date_end], order__ordered=True).values_list('product_id', 'product__product_name',)
        print(top_product)
        print(collections.Counter(top_product).most_common())
        a = collections.Counter(top_product).most_common()[:int(number_of_top)]
        context = {
            'order_in_time': order_in_time,
            'date_start': date_start,
            'date_end': date_end,
            'top_product': a,
            'number_of_top':number_of_top,
        }
        if date_start < date_end:
            return render(request, 'clothes/admin_site/order/order_static.html', context)
        else:
            messages.error(request, "Ngày bắt đầu phải nhỏ hơn ngày kết thúc", extra_tags='error')
            return redirect('clothes:order_static_admin')
