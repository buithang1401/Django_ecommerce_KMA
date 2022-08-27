from django.contrib.auth.models import User
from django.forms import ModelForm, widgets
from .models import Product, ClothesType, Category
from django import forms
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category_id', 'product_description',
                  'product_status','type_id','product_image','product_price','quantity','size',]

class TypeForm(ModelForm):
    class Meta:
        model = ClothesType
        fields = ['type_name',]

class CateForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name_category',]

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','groups', 'user_permissions' ]

class CheckoutForm(forms.Form):
    street_address = forms.CharField()
    department_address = forms.CharField(required=False)
    # country = CountryField(blank_label=('Select Country'))
    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput())
    save_info = forms.BooleanField(widget=forms.CheckboxInput())
    payment_option = forms.BooleanField(widget=forms.RadioSelect())