from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Product 
from .models import Wishlist
from django.urls import reverse
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



@login_required
def home(request):
    return render(request, 'home.html')


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




@login_required
def home(request):

    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )
        template = "search_results.html"
    else:
        products = Product.objects.all()
        template = "home.html"

    wishlist_items = Wishlist.objects.filter(user=request.user)

    wishlist_products = wishlist_items.values_list('product_id', flat=True)

    wishlist_count = wishlist_items.count()

    return render(request, template, {
        'products': products,
        'query': query,
        'wishlist_products': wishlist_products,
        'wishlist_count': wishlist_count
    })





@login_required
def add_to_wishlist(request, id):
    product = Product.objects.get(id=id)

    item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect('home')

@login_required
def add_to_wishlist(request, id):

    product = get_object_or_404(Product, id=id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def wishlist_page(request):

    items = Wishlist.objects.filter(user=request.user)

    return render(request,'wishlist.html',{'items':items})



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





@login_required
def add_to_wishlist(request, id):

    product = get_object_or_404(Product, id=id)

    item = Wishlist.objects.filter(user=request.user, product=product)

    if item.exists():
        item.delete()   
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






@login_required
def syrup_page(request):

    syrups = Product.objects.filter(category='Syrup')

    wishlist_items = Wishlist.objects.filter(user=request.user)

    wishlist_products = wishlist_items.values_list('product_id', flat=True)

    wishlist_count = wishlist_items.count()

    return render(request,'syrup.html',{
        'syrups':syrups,
        'wishlist_products':wishlist_products,
        'wishlist_count':wishlist_count
    })




@login_required
def injection_page(request):

    injections = Product.objects.filter(category='Injection')

    wishlist_items = Wishlist.objects.filter(user=request.user)

    wishlist_products = wishlist_items.values_list('product_id', flat=True)

    wishlist_count = wishlist_items.count()

    return render(request,'injection.html',{
        'injections':injections,
        'wishlist_products':wishlist_products,
        'wishlist_count':wishlist_count
    })




@login_required
def firstaid_page(request):

    firstaids = Product.objects.filter(category='First Aid')

    wishlist_items = Wishlist.objects.filter(user=request.user)

    wishlist_products = wishlist_items.values_list('product_id', flat=True)

    wishlist_count = wishlist_items.count()

    return render(request,'firstaid.html',{
        'firstaids':firstaids,
        'wishlist_products':wishlist_products,
        'wishlist_count':wishlist_count
    })





@login_required
def supplement_page(request):

    supplements = Product.objects.filter(category='Supplement')

    wishlist_items = Wishlist.objects.filter(user=request.user)

    wishlist_products = wishlist_items.values_list('product_id', flat=True)

    wishlist_count = wishlist_items.count()

    return render(request,'supplement.html',{
        'supplements':supplements,
        'wishlist_products':wishlist_products,
        'wishlist_count':wishlist_count
    })





@login_required
def add_to_wishlist(request, id):

    product = get_object_or_404(Product, id=id)

    item = Wishlist.objects.filter(user=request.user, product=product)

    if item.exists():
        item.delete()
    else:
        Wishlist.objects.create(user=request.user, product=product)

    return redirect(request.META.get('HTTP_REFERER'))







# @login_required
# def add_to_cart(request,id):

#     cart = request.session.get('cart',{})

#     if str(id) in cart:
#         cart[str(id)] += 1
#     else:
#         cart[str(id)] = 1

#     request.session['cart'] = cart

#     return redirect(request.META.get('HTTP_REFERER'))



def add_to_cart(request, id):

    cart = request.session.get('cart', {})

    if not isinstance(cart, dict):
        cart = {}

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    request.session['cart'] = cart

    # return redirect('home')
    return redirect(request.META.get('HTTP_REFERER'))






@login_required
def cart(request):

    cart = request.session.get('cart',{})

    product_ids = cart.keys()

    products = Product.objects.filter(id__in=product_ids)

    cart_items = []
    subtotal = 0

    for product in products:

        quantity = cart[str(product.id)]
        total_price = product.price * quantity

        subtotal += total_price

        cart_items.append({
            'product':product,
            'quantity':quantity,
            'total_price':total_price
        })

    gst = subtotal * 0.18
    total = subtotal + gst

    cart_count = sum(cart.values())

    return render(request,'cart.html',{
        'cart_items':cart_items,
        'subtotal':subtotal,
        'gst':gst,
        'total':total,
        'cart_count':cart_count
    })



def home(request):

    products = Product.objects.all()

    wishlist = Wishlist.objects.filter(user=request.user)
    wishlist_count = wishlist.count()

    return render(request,'home.html',{
        'products':products,
        'wishlist_count':wishlist_count
    })



def home(request):

    products = Product.objects.all()

    return render(request,'home.html',{
        'products':products
    })




def home(request):

    products = Product.objects.all()

    wishlist = Wishlist.objects.filter(user=request.user)
    wishlist_count = wishlist.count()

    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    return render(request,'home.html',{
        'products':products,
        'wishlist_count':wishlist_count,
        'cart_count':cart_count
    })


def home(request):

    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    wishlist = Wishlist.objects.filter(user=request.user)
    wishlist_count = wishlist.count()

    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    return render(request,'home.html',{
        'products':products,
        'wishlist_count':wishlist_count,
        'cart_count':cart_count
    })






@login_required
def home(request):

    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    wishlist_items = Wishlist.objects.filter(user=request.user)

    
    wishlist_products = wishlist_items.values_list('product_id', flat=True)

    wishlist_count = wishlist_items.count()


    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    return render(request,'home.html',{
        'products':products,
        'wishlist_products':wishlist_products,
        'wishlist_count':wishlist_count,
        'cart_count':cart_count
    })






@login_required
def add_to_wishlist(request, id):

    product = get_object_or_404(Product, id=id)

    item = Wishlist.objects.filter(user=request.user, product=product)

    if item.exists():
        item.delete()
    else:
        Wishlist.objects.create(user=request.user, product=product)

    return redirect(request.META.get('HTTP_REFERER'))







@login_required
def cart(request):

    query = request.GET.get('q')

    cart = request.session.get('cart', {})

    if not isinstance(cart, dict):
        cart = {}

    product_ids = cart.keys()

    products = Product.objects.filter(id__in=product_ids)


    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )

    cart_items = []
    total = 0

    for product in products:

        quantity = cart.get(str(product.id), 1)

        subtotal = product.price * quantity

        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    gst = total * 0.05
    final_total = total + gst

    context = {
        'cart_items': cart_items,
        'total': total,
        'gst': gst,
        'final_total': final_total,
        'query': query
    }

    return render(request, 'cart.html', context)







@login_required
def update_cart(request,id,action):

    cart = request.session.get('cart',{})

    if str(id) in cart:

        if action == "plus":
            cart[str(id)] += 1

        elif action == "minus":
            cart[str(id)] -= 1

            if cart[str(id)] <= 0:
                del cart[str(id)]

    request.session['cart'] = cart

    return redirect('cart')




@login_required
def remove_cart(request,id):

    cart = request.session.get('cart',{})

    if str(id) in cart:
        del cart[str(id)]

    request.session['cart'] = cart

    return redirect('cart')







@login_required
def search_results(request):
    query = request.GET.get('q', '')

    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(category__icontains=query)
    )

    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlist_products = wishlist_items.values_list('product_id', flat=True)
    wishlist_count = wishlist_items.count()


    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    return render(request, 'search_results.html', {
        'products': products,
        'query': query,
        'wishlist_products': wishlist_products,
        'wishlist_count': wishlist_count,
        'cart_count': cart_count
    })





@login_required
def home(request):
    products = Product.objects.all()

    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlist_products = wishlist_items.values_list('product_id', flat=True)
    wishlist_count = wishlist_items.count()

    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
            cart = {}
    cart_count = sum(cart.values())

    return render(request, 'home.html', {
        'products': products,
        'wishlist_products': wishlist_products,
        'wishlist_count': wishlist_count,
        'cart_count': cart_count
    })





@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    item = Wishlist.objects.filter(user=request.user, product=product)
    if item.exists():
        item.delete()
    else:
        Wishlist.objects.create(user=request.user, product=product)
    
    # Stay on the same page
    return redirect(request.META.get('HTTP_REFERER'))




@login_required
def redirect_search(request):
    query = request.GET.get('q', '').strip()
    category_map = {
        'tablet': 'tablet_page',
        'syrup': 'syrup_page',
        'injection': 'injection_page',
        'first aid': 'firstaid_page',
        'supplement': 'supplement_page'
    }

    for cat_name, url_name in category_map.items():
        if cat_name in query.lower():
            return redirect(f"{reverse(url_name)}?q={query}")

    return redirect(f"{reverse('search_results')}?q={query}")





def checkout(request):

    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for id, qty in cart.items():
        product = Product.objects.get(id=id)

        subtotal = product.price * qty
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': qty,
            'subtotal': subtotal
        })

    gst = total * 0.18
    grand_total = total + gst

    # ✅ PLACE ORDER
    if request.method == "POST":
        request.session['cart'] = {}   # clear cart
        return render(request, 'order_success.html', {
            'total': grand_total
        })

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'gst': gst,
        'grand_total': grand_total
    })