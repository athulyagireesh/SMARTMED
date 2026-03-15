from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Product
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q



def register_view(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        User.objects.create_user(username=name, password=password)

        return redirect('login')

    return render(request, 'register.html')





def login_view(request):
    if request.method == "POST":
        username = request.POST ['username']
        password = request.POST ['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect('login')



# @login_required
# def home(request):
#     return render(request, 'home.html')


@login_required
def home(request):

    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, 'home.html', {'products': products})





def tablet_page(request):
    tablets = Product.objects.filter(category='Tablet')
    return render(request, 'tablet.html', {'tablets': tablets})



def syrup_page(request):
    syrups = Product.objects.filter(category='Syrup')
    return render(request, 'syrup.html', {'syrups': syrups})


def injection_page(request):
    injections = Product.objects.filter(category='Injection')
    return render(request, 'injection.html', {'injections': injections})


def firstaid_page(request):
    firstaid = Product.objects.filter(category='First Aid')
    return render(request, 'firstaid.html', {'firstaids': firstaid})


def supplement_page(request):
    supplements = Product.objects.filter(category='Supplement')
    return render(request, 'supplement.html', {'supplements': supplements})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})



def add_to_cart(request, id):
    product = Product.objects.get(id=id)

    cart = request.session.get('cart', [])

    cart.append(product.id)

    request.session['cart'] = cart

    return redirect('cart')



def cart(request):
    cart = request.session.get('cart', [])

    products = Product.objects.filter(id__in=cart)

    return render(request, 'cart.html', {'products': products})


@login_required
def home(request):

    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )
    else:
        products = Product.objects.all()

    return render(request, 'home.html', {'products': products})