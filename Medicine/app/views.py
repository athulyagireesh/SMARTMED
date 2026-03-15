from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Product 
from .models import Wishlist
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
        return render(request, 'search_results.html', {'products': products, 'query': query})

    products = Product.objects.all()
    wishlist_count = Wishlist.objects.filter(user=request.user).count()

    return render(request,'home.html',{'products':products,'wishlist_count':wishlist_count})



# @login_required
# def add_to_wishlist(request, id):
#     product = Product.objects.get(id=id)

#     item, created = Wishlist.objects.get_or_create(
#         user=request.user,
#         product=product
#     )

#     return redirect('home')

@login_required
def add_to_wishlist(request, id):

    product = get_object_or_404(Product, id=id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect(request.META.get('HTTP_REFERER'))


# @login_required
# def wishlist_page(request):

#     items = Wishlist.objects.filter(user=request.user)

#     return render(request,'wishlist.html',{'items':items})



@login_required
def wishlist_page(request):

    query = request.GET.get('q')

    items = Wishlist.objects.filter(user=request.user)

    if query:
        items = items.filter(product__name__icontains=query)

    return render(request, 'wishlist.html', {'items': items})



@login_required
def remove_wishlist(request, id):

    item = get_object_or_404(Wishlist, id=id, user=request.user)
    item.delete()

    return redirect('wishlist_page')


# @login_required
# def tablet_page(request):

#     tablets = Product.objects.filter(category='Tablet')

#     wishlist_count = Wishlist.objects.filter(user=request.user).count()

#     return render(request, 'tablet.html', {
#         'tablets': tablets,
#         'wishlist_count': wishlist_count
#     })


@login_required
def add_to_wishlist(request, id):

    product = get_object_or_404(Product, id=id)

    item = Wishlist.objects.filter(user=request.user, product=product)

    if item.exists():
        item.delete()   # remove if already in wishlist
    else:
        Wishlist.objects.create(user=request.user, product=product)

    return redirect(request.META.get('HTTP_REFERER'))




@login_required
def tablet_page(request):

    tablets = Product.objects.filter(category='Tablet')

    wishlist_items = Wishlist.objects.filter(user=request.user)

    wishlist_products = wishlist_items.values_list('product_id', flat=True)

    wishlist_count = wishlist_items.count()

    return render(request,'tablet.html',{
        'tablets': tablets,
        'wishlist_products': wishlist_products,
        'wishlist_count': wishlist_count
    })