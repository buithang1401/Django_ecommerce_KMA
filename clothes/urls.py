from django.urls import path

from clothes.views.admin_views import AdminView, TableAdminView, ChartAdminView, ProductAdminView, UpdateProduct, \
    DeleteProduct, Login, AddProduct, TypeAdminView, AddType, DeleteType, UpdateType, CateAdminView, UpdateCate, \
    AddCate, DeleteCate, Register, FogetPassword, ChangePassword, UserAdminView, AddUser, UpdateUser, DeleteUser, \
    Logout, CusAdminView, OrderAdminView, OrderStaticAdminView
from clothes.views.user_view import HomeClass, AoPhongNamView, ItemDetail, AoPoloNamView, QuanJeanNamView, \
    QuanShortNamView, ClothesMenView, add_to_cart, Payment, remove_from_cart, add_single_to_cart, ConfirmCheckout, \
    OnlinePayment, OrderManage, search_data, buy_immediately, ClothesWomenView, AoPhongNuView, AoPoloNuView, \
    QuanJeanNuView, QuanShortNuView, VayNuView

app_name = 'clothes'
urlpatterns = [
    #user
    path('', HomeClass, name='home'),
    path('search_data', search_data, name='search_data'),
    path('payment/', Payment.as_view(), name='payment'),
    path('confirm_pay/', ConfirmCheckout.as_view(), name='confirm_checkout'),
    path('onlinepayment/', OnlinePayment.as_view(), name='online_payment'),
    path('order_manage/', OrderManage.as_view(), name='manage_order'),

    path('add_to_cart/<pk>', add_to_cart, name='add_to_cart'),
    path('buy_immediately', buy_immediately, name='buy_immediately'),
    path('remove_from_cart/<pk>', remove_from_cart, name='remove_from_cart'),
    path('add_single_to_cart/<pk>', add_single_to_cart, name='add_single_to_cart'),

    #ao phong nam
    path('product/nam/', ClothesMenView.as_view(), name='quan_ao_nam'),
    path('product/nam/aophong/', AoPhongNamView.as_view(), name='ao_phong_nam'),
    path('product/nam/aopolo/', AoPoloNamView.as_view(), name='ao_polo_nam'),
    path('product/nam/quanjean/', QuanJeanNamView.as_view(), name='quan_jean_nam'),
    path('product/nam/quanshort/', QuanShortNamView.as_view(), name='quan_short_nam'),
    path('detail/nam/<int:pk>', ItemDetail.as_view(), name='product_detail'),

    # ao phong nu
    path('product/nu/', ClothesWomenView.as_view(), name='quan_ao_nu'),
    path('product/nu/aophong/', AoPhongNuView.as_view(), name='ao_phong_nu'),
    path('product/nu/aopolo/', AoPoloNuView.as_view(), name='ao_polo_nu'),
    path('product/nu/quanjean/', QuanJeanNuView.as_view(), name='quan_jean_nu'),
    path('product/nu/quanshort/', QuanShortNuView.as_view(), name='quan_short_nu'),
    path('product/nu/vay/', VayNuView.as_view(), name='vay_nu'),

    #admin site
    path('adminview/', AdminView, name='admin_view'),
    path('table/', TableAdminView, name='table_view'),
    path('chart/', ChartAdminView.as_view(), name='chart_view'),

    #admin manage product
    path('productadmin/', ProductAdminView.as_view(), name='product_admin'),
    path('createproduct/', AddProduct.as_view(), name="add_product"),
    path('update/<int:pk>', UpdateProduct.as_view(), name='product_edit_admin'),
    path('delete/<int:pk>', DeleteProduct.as_view(), name="product_delete_admin"),

    #admin manage type
    path('typeadmin/', TypeAdminView.as_view(), name='type_admin'),
    path('updatetype/<int:pk>', UpdateType.as_view(), name='edit_type'),
    path('deletetype/<int:pk>', DeleteType.as_view(), name="delete_type"),
    path('createtype/', AddType.as_view(), name="add_type"),

    #admin manage category
    path('cateadmin/', CateAdminView.as_view(), name='cate_admin'),
    path('updatecate/<int:pk>', UpdateCate.as_view(), name='edit_cate'),
    path('deletecate/<int:pk>', DeleteCate.as_view(), name="delete_cate"),
    path('createcate/', AddCate.as_view(), name="add_cate"),

    #admin manager user
    path('user/', UserAdminView.as_view(), name='user_admin'),
    path('updateuser/<int:pk>', UpdateUser.as_view(), name='edit_user'),
    path('deleteuser/<int:pk>', DeleteUser.as_view(), name="delete_user"),
    path('createuser/', AddUser.as_view(), name="add_user"),

    # admin manager user
    path('cus/', CusAdminView.as_view(), name='cus_admin'),
    # path('updatecus/<int:pk>', UpdateCus.as_view(), name='edit_user'),
    # path('deletecus/<int:pk>', DeleteUser.as_view(), name="delete_user"),
    # path('createcus/', AddUser.as_view(), name="add_user"),

    # admin manager order
    path('order/', OrderAdminView.as_view(), name='order_admin'),
    path('orderstatic/', OrderStaticAdminView.as_view(), name='order_static_admin'),

    #login
    path('login/', Login, name="login"),
    path('logout/',Logout, name="logout" ),
    path('register/', Register.as_view(), name="register"),
    path('forgetpass/', FogetPassword.as_view(), name="forget_password"),
    path('changepass/<token>/', ChangePassword, name="change_password"),

]