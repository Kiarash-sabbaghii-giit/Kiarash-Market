from django.urls import path
from . import views

urlpatterns = [
    # صفحات اصلی
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('support/', views.support, name='support'),

    # احراز هویت
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # دسته بندی و محصولات
    path('categories/', views.category_list, name='categories'),
    path('category/<str:category_en>/', views.category_products, name='category_products'),

    # جستجو
    path('search/', views.search_page, name='search'),
    path('api/search-suggestions/', views.search_suggestions, name='search_suggestions'),

    # پروفایل و سفارشات
    path('profile/', views.profile_view, name='profile'),
    path('orders/', views.orders_view, name='orders'),

    # سبد خرید
    path('cart/', views.cart_view, name='cart'),
    path('api/cart/add/', views.cart_add, name='cart_add'),
    path('api/cart/update/', views.cart_update, name='cart_update'),
    path('api/cart/count/', views.cart_count, name='cart_count'),

    # تسویه حساب و پرداخت
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment/<int:order_id>/', views.payment_view, name='payment'),
    path('online-payment/<int:order_id>/', views.online_payment_view, name='online_payment'),
    path('process-payment/<int:order_id>/', views.process_payment, name='process_payment'),

    # پنل مدیریت (ادمین)
    path('admin-panel/', views.admin_categories, name='admin_categories'),
    path('admin-panel/category/edit/<str:category_en>/', views.admin_category_edit, name='admin_category_edit'),
    path('admin-panel/category/delete/<str:category_en>/', views.admin_category_delete, name='admin_category_delete'),
    path('admin-panel/products/', views.admin_products, name='admin_products'),
    path('admin-panel/products/<str:category_en>/', views.admin_products, name='admin_products'),
    path('admin-panel/product/add/<str:category_en>/', views.admin_product_add, name='admin_product_add'),
    path('admin-panel/product/edit/<str:category_en>/<str:product_name>/', views.admin_product_edit,
         name='admin_product_edit'),
    path('admin-panel/product/delete/<str:category_en>/<str:product_name>/', views.admin_product_delete,
         name='admin_product_delete'),
    path('admin-panel/orders/', views.admin_orders_report, name='admin_orders_report'),
    path('admin-panel/orders/export/excel/', views.admin_orders_export_excel, name='admin_orders_export_excel'),
    path('admin-panel/orders/export/pdf/', views.admin_orders_export_pdf, name='admin_orders_export_pdf'),
    path('api/order-details/<int:order_id>/', views.order_details_api, name='order_details_api'),
]