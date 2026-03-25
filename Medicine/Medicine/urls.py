"""
URL configuration for Medicine project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URL configuration for Medicine project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home,name='home'), 
    path('logout/', views.logout_view, name='logout'),
    path('tablet/', views.tablet_page, name='tablet_page'),
    path('syrup/', views.syrup_page, name='syrup_page'),
    path('injection/', views.injection_page, name='injection_page'),
    path('firstaid/', views.firstaid_page, name='firstaid_page'),
    path('supplement/', views.supplement_page, name='supplement_page'),

    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),


    path('search/', views.search_results, name='search_results'),

    path('update-cart/<int:id>/<str:action>/',views.update_cart,name='update_cart'),
    path('remove-cart/<int:id>/',views.remove_cart,name='remove_cart'),
    path('add-wishlist/<int:id>/', views.add_to_wishlist, name='add_wishlist'),
    path('wishlist/', views.wishlist_page, name='wishlist_page'),
    path('remove-wishlist/<int:id>/', views.remove_wishlist, name='remove_wishlist'),


    path('redirect-search/', views.redirect_search, name='redirect_search'),

    path('upload-prescription/', views.upload_prescription, name='upload_prescription'),

    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
