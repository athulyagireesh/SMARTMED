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


  

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


