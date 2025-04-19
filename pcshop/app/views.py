from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Product,Category,Cart,CartItem,CustomUser,Order,OrderItem,Profile
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login , get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.views.decorators.http import require_POST


# Create your views here.
def base(request):
    return render(request , 'app/base.html')

def index(request):
    return render(request , 'app/index.html')

def search(request):
    return render(request , 'app/search.html')

def login(request):
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                
                if user.is_superuser:
                    return redirect('/admin/')
                auth_login(request, user)
                return redirect('app:base')  
        else:
            form = AuthenticationForm()

        return render(request, 'app/login.html', {'form': form})

@login_required
def mycart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        cart_items = None

    context = {
        'cart_items': cart_items,
    }
    return render(request, 'app/mycart.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart , _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('app:mycart')

@login_required
def update_cart_item(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if action == "increase":
        item.quantity += 1
    elif action == "decrease" and item.quantity > 1:
        item.quantity -= 1
    item.save()
    
    return redirect('app:mycart')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('app:mycart')


User = get_user_model()

@login_required
def checkout_view(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()
    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        address = request.POST.get('address')
        if not address:
            messages.error(request, "Address is required.")
            return redirect('checkout')

        # Create Order
        order = Order.objects.create(user=request.user, address=address, total=total)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear cart after order
        cart.items.all().delete()

        return render(request, 'app/order_confirmation.html', {
            'order': order,
            'items': order.items.all()
        })

    return render(request, 'app/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })
    
    

@login_required
def user_details(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=request.user)
    # Fetching user's order history
    orders = Order.objects.filter(user=user)
    
    # Handle missing profile
    try:
        profile = user.profile
        address = profile.shipping_address
        phone_number = profile.phone_number
        pin_code = profile.pin_code
    except user.profile.DoesNotExist:
        # Fallback in case the profile doesn't exist
        address = phone_number = pin_code = None

    context = {
        'user': user,
        'orders': orders,
        'address': address,
        'phone_number': phone_number,
        'pin_code': pin_code,
    }
    return render(request, 'app/user_details.html', context)


    
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email    = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('confirm_password')

        if password != password2:
            messages.error(request, "Passwords do not match")
            return redirect('app:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('app:register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        auth_login(request, user)
        return redirect('app:base')
    return render(request, 'app/register.html')

@require_POST
def logout_view(request):
    logout(request)
    request.session.flush()
    return render(request, 'app/logout.html')
    
        # if request.method == 'POST':
        #     form = CustomUserCreationForm(request.POST)
        #     if form.is_valid():
        #         user = form.save()
        #         auth_login(request, user)
        #         return redirect('app:login')  
        # else:
        #     form = CustomUserCreationForm()
        # return render(request, 'app/register.html', {'form': form})

# def products(request):
#     return render(request , 'app/products.html')

# def details(request, product_id):
#     product = get_object_or_404(product, id=product_id)  
#     return render(request, 'app/details.html', {'productid': product_id})

def products(request):
    product_list = Product.objects.all()
    return render(request, 'app/products.html', {'products': product_list})

def details(request, product_id):
    product = get_object_or_404(Product, id=product_id)  
    return render(request, 'app/details.html', {'product': product})



