from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.urls import reverse
from django.core.mail import send_mail
from .models import Order, OrderItem 
from django.contrib import messages
from .models import Product, Wishlist, Cart
from .models import Product, Prescription
import pytesseract
import re
import cv2
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def register_view(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']
        User.objects.create_user(username=name, password=password)
        return redirect('login')
    return render(request, 'register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

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
    products = Product.objects.all()

    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlist_products = wishlist_items.values_list('product_id', flat=True)
    wishlist_count = wishlist_items.count()

    # ✅ FIXED CART COUNT
    cart_count = Cart.objects.filter(user=request.user).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    return render(request, 'home.html', {
        'products': products,
        'wishlist_products': wishlist_products,
        'wishlist_count': wishlist_count,
        'cart_count': cart_count
    })






@login_required
def tablet_page(request):
    tablets = Product.objects.filter(category='Tablet')

    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlist_products = wishlist_items.values_list('product_id', flat=True)
    wishlist_count = wishlist_items.count()

    cart_count = Cart.objects.filter(user=request.user).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    return render(request, 'tablet.html', {
        'tablets': tablets,
        'wishlist_products': wishlist_products,
        'wishlist_count': wishlist_count,
        'cart_count': cart_count
    })


@login_required
def syrup_page(request):
    syrups = Product.objects.filter(category='Syrup')

    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlist_products = wishlist_items.values_list('product_id', flat=True)
    wishlist_count = wishlist_items.count()

    cart_count = Cart.objects.filter(user=request.user).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    return render(request, 'syrup.html', {
        'syrups': syrups,
        'wishlist_products': wishlist_products,
        'wishlist_count': wishlist_count,
        'cart_count': cart_count
    })


@login_required
def injection_page(request):
    injections = Product.objects.filter(category='Injection')

    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlist_products = wishlist_items.values_list('product_id', flat=True)
    wishlist_count = wishlist_items.count()

    cart_count = Cart.objects.filter(user=request.user).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    return render(request, 'injection.html', {
        'injections': injections,
        'wishlist_products': wishlist_products,
        'wishlist_count': wishlist_count,
        'cart_count': cart_count
    })


@login_required
def firstaid_page(request):
    firstaids = Product.objects.filter(category='First Aid')

    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlist_products = wishlist_items.values_list('product_id', flat=True)
    wishlist_count = wishlist_items.count()

    cart_count = Cart.objects.filter(user=request.user).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    return render(request, 'firstaid.html', {
        'firstaids': firstaids,
        'wishlist_products': wishlist_products,
        'wishlist_count': wishlist_count,
        'cart_count': cart_count
    })


@login_required
def supplement_page(request):
    supplements = Product.objects.filter(category='Supplement')

    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlist_products = wishlist_items.values_list('product_id', flat=True)
    wishlist_count = wishlist_items.count()

    cart_count = Cart.objects.filter(user=request.user).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    return render(request, 'supplement.html', {
        'supplements': supplements,
        'wishlist_products': wishlist_products,
        'wishlist_count': wishlist_count,
        'cart_count': cart_count
    })



def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})




@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect(request.META.get('HTTP_REFERER'))



@login_required
def cart(request):

    items = Cart.objects.filter(user=request.user)

    cart_items = []
    total = 0

    for item in items:
        subtotal = item.product.price * item.quantity
        total += subtotal

        cart_items.append({
            'product': item.product,
            'quantity': item.quantity,
            'total_price': subtotal
        })

    gst = round(total * 0.18, 2)

    # ✅ CORRECT CART COUNT (DATABASE)
    cart_count = items.aggregate(total=Sum('quantity'))['total'] or 0

    # ✅ CORRECT WISHLIST COUNT
    wishlist_count = Wishlist.objects.filter(user=request.user).count()

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'gst': gst,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
    })



@login_required
def update_cart(request, id, action):
    item = get_object_or_404(Cart, user=request.user, product_id=id)

    if action == "plus":
        item.quantity += 1
    elif action == "minus":
        item.quantity -= 1
        if item.quantity <= 0:
            item.delete()
            return redirect('cart')

    item.save()
    return redirect('cart')


@login_required
def remove_cart(request, id):
    item = get_object_or_404(Cart, user=request.user, product_id=id)
    item.delete()
    return redirect('cart')



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
# def wishlist_page(request):
#     items = Wishlist.objects.filter(user=request.user)
#     return render(request, 'wishlist.html', {'items': items})


@login_required
def wishlist_page(request):

    items = Wishlist.objects.filter(user=request.user)

    # ✅ FIXED COUNTS (SAME AS CART & CHECKOUT)
    cart_count = Cart.objects.filter(user=request.user).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    wishlist_count = items.count()

    return render(request, 'wishlist.html', {
        'items': items,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count
    })


@login_required
def remove_wishlist(request, id):
    item = get_object_or_404(Wishlist, id=id, user=request.user)
    item.delete()
    return redirect('wishlist_page')




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

    cart_count = Cart.objects.filter(user=request.user).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    return render(request, 'search_results.html', {
        'products': products,
        'query': query,
        'wishlist_products': wishlist_products,
        'wishlist_count': wishlist_count,
        'cart_count': cart_count
    })


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

    for key, value in category_map.items():
        if key in query.lower():
            return redirect(f"{reverse(value)}?q={query}")

    return redirect(f"{reverse('search_results')}?q={query}")






# @login_required
# def my_orders(request):

#     orders = Order.objects.filter(user=request.user).order_by('-created_at')

#     cart_count = Cart.objects.filter(user=request.user).aggregate(
#         total=Sum('quantity')
#     )['total'] or 0

#     wishlist_count = Wishlist.objects.filter(user=request.user).count()

#     return render(request, 'my_orders.html', {
#         'orders': orders,
#         'cart_count': cart_count,
#         'wishlist_count': wishlist_count
#     })



@login_required
def my_orders(request):

    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # ✅ navbar count fix
    cart_items = Cart.objects.filter(user=request.user)
    wishlist_items = Wishlist.objects.filter(user=request.user)

    cart_count = sum(item.quantity for item in cart_items)
    wishlist_count = wishlist_items.count()

    return render(request, 'my_orders.html', {
        'orders': orders,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count
    })







# @login_required
# def checkout(request):
#     items = Cart.objects.filter(user=request.user)

#     total = 0
#     cart_items = []

#     for item in items:
#         subtotal = item.product.price * item.quantity
#         total += subtotal

#         cart_items.append({
#             'product': item.product,
#             'quantity': item.quantity,
#             'subtotal': subtotal
#         })

#     gst = total * 0.18
#     grand_total = total + gst

   
#     cart_count = Cart.objects.filter(user=request.user).aggregate(
#         total=Sum('quantity')
#     )['total'] or 0

#     wishlist_count = Wishlist.objects.filter(user=request.user).count()

#     if request.method == "POST":
#         items.delete()  
#         return render(request, 'order_success.html', {
#             'total': grand_total
#         })

#     return render(request, 'checkout.html', {
#         'cart_items': cart_items,
#         'total': total,
#         'gst': gst,
#         'grand_total': grand_total,
#         'cart_count': cart_count,
#         'wishlist_count': wishlist_count
#     })









# @login_required
# def checkout(request):

#     items = Cart.objects.filter(user=request.user)

#     total = 0
#     cart_items = []

#     for item in items:
#         subtotal = item.product.price * item.quantity
#         total += subtotal

#         cart_items.append({
#             'product': item.product,
#             'quantity': item.quantity,
#             'subtotal': subtotal
#         })

#     gst = round(total * 0.18, 2)
#     grand_total = total + gst

   
#     cart_count = items.aggregate(total=Sum('quantity'))['total'] or 0
#     wishlist_count = Wishlist.objects.filter(user=request.user).count()

#     if request.method == "POST":

#         if items.exists():   

#             order = Order.objects.create(
#                 user=request.user,
#                 total_amount=grand_total
#             )

#             for item in items:
#                 OrderItem.objects.create(
#                     order=order,
#                     product=item.product,
#                     quantity=item.quantity,
#                     price=item.product.price
#                 )

      
#             items.delete()

#             return render(request, 'order_success.html', {
#                 'total': grand_total
#             })

#     return render(request, 'checkout.html', {
#         'cart_items': cart_items,
#         'total': total,
#         'gst': gst,
#         'grand_total': grand_total,
#         'cart_count': cart_count,
#         'wishlist_count': wishlist_count
#     })













# @login_required
# def checkout(request):

#     cart_items = Cart.objects.filter(user=request.user)

#     total = 0

#     for item in cart_items:
#         total += item.product.price * item.quantity

#     if request.method == "POST":

#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         address = request.POST.get('address')
#         payment = request.POST.get('payment')

    
#         order = Order.objects.create(
#             user=request.user,
#             name=name,
#             email=email,
#             phone=phone,
#             address=address,
#             payment_method=payment,
#             total_amount=total
#         )

#         for item in cart_items:
#             OrderItem.objects.create(
#                 order=order,
#                 product=item.product,
#                 quantity=item.quantity,
#                 price=item.product.price
#             )

    
#         cart_items.delete()

        
#         send_mail(
#             'Order Placed Successfully',
#             f'Hi {name}, your order #{order.id} is confirmed!',
#             'your_email@gmail.com',
#             [email],
#             fail_silently=True,
#         )

#         return redirect('order_success')

#     return render(request, 'checkout.html', {
#         'cart_items': cart_items,
#         'total': total
#     })









# @login_required
# def checkout(request):
#     items = Cart.objects.filter(user=request.user)

#     total = 0
#     cart_items = []

#     for item in items:
#         subtotal = item.product.price * item.quantity
#         total += subtotal

#         cart_items.append({
#             'product': item.product,
#             'quantity': item.quantity,
#             'subtotal': subtotal
#         })

#     gst = total * 0.18
#     grand_total = total + gst

#     if request.method == "POST":
#         items.delete()
#         return render(request, 'order_success.html', {
#             'total': grand_total
#         })

#     return render(request, 'checkout.html', {
#         'cart_items': cart_items,
#         'total': total,
#         'gst': gst,
#         'grand_total': grand_total
#     })




@login_required
def upload_prescription(request):

    if request.method == "POST":
        image = request.FILES.get('prescription')

        if image:
            # ✅ Save image
            prescription = Prescription.objects.create(
                user=request.user,
                image=image
            )

            # 🔥 IMAGE PREPROCESSING (IMPORTANT)
            img = cv2.imread(prescription.image.path)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Improve clarity
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

            processed_path = prescription.image.path.replace('.jpg', '_processed.jpg')
            cv2.imwrite(processed_path, thresh)

            # 🔥 OCR
            text = pytesseract.image_to_string(processed_path)

            print("OCR TEXT:", text)

            # 🔥 CLEAN TEXT
            text = text.lower()
            text = re.sub(r'[^a-zA-Z\s]', '', text)

            words = text.split()

            # 🔥 IGNORE WORDS
            ignore_words = [
                'tab','tablet','mg','ml','take','after','before',
                'morning','night','daily','once','twice','days',
                'q','rx','age','name','sex','date'
            ]

            filtered_words = [
                word for word in words
                if word not in ignore_words and len(word) > 4
            ]

            print("Filtered Words:", filtered_words)

            # 🔥 MATCH PRODUCTS
            matched_products = Product.objects.none()

            for word in filtered_words:
                results = Product.objects.filter(name__icontains=word)
                if results.exists():
                    matched_products |= results

            # 🔥 EXTRA ACCURACY (full name match)
            for product in Product.objects.all():
                if product.name.lower() in text:
                    matched_products |= Product.objects.filter(id=product.id)

            matched_products = matched_products.distinct()

            return render(request, 'prescription_result.html', {
                'products': matched_products,
                'text': text,
                'manual_input': ""
            })

    return redirect('home')







@login_required
def checkout(request):

    cart_items = Cart.objects.filter(user=request.user)
    wishlist_items = Wishlist.objects.filter(user=request.user)

    # ✅ COUNT FIX
    cart_count = sum(item.quantity for item in cart_items)
    wishlist_count = wishlist_items.count()

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    if request.method == "POST":

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment = request.POST.get('payment')

        order = Order.objects.create(
            user=request.user,
            name=name,
            email=email,
            phone=phone,
            address=address,
            payment_method=payment,
            total_amount=total
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart_items.delete()

        return redirect('order_success')

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'cart_count': cart_count,          # ✅ FIX
        'wishlist_count': wishlist_count   # ✅ FIX
    })


@login_required
def order_success(request):
    return render(request, 'order_success.html')

def order_success(request):
    # Get cart count
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values()) if cart else 0

    # Get wishlist count
    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    else:
        wishlist_count = 0

    return render(request, 'order_success.html', {
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
    })

# @login_required
# def my_orders(request):
#     orders = Order.objects.filter(user=request.user).order_by('-created_at')
#     return render(request, 'my_orders.html', {'orders': orders})



@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == "Pending":
        order.status = "Cancelled"
        order.save()

    return redirect('my_orders')


@login_required
def remove_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == "Cancelled":
        order.delete()
        messages.success(request, "Order removed successfully.")
    return redirect('my_orders')