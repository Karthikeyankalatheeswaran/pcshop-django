from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Product,Category,Cart,CartItem,CustomUser,Order,OrderItem,Profile,Brand,Review,Wishlist
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
from .forms import UserUpdateForm,ReviewForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def base(request):
    return render(request , 'app/base.html')

def index(request):
    return render(request , 'app/index.html')

def search(request):
    query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')
    brand_filter = request.GET.get('brand', '')

    products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category_filter:
        products = products.filter(category__name=category_filter)

    if brand_filter:
        products = products.filter(brand__name=brand_filter)

    for category in categories:
        category.selected = (category.name == category_filter)
    for brand in brands:
        brand.selected = (brand.name == brand_filter)


    return render(request, 'app/search.html', {
        'query': query,
        'products': products,
        'categories': categories,
        'brands': brands,
        'category_filter': category_filter,
        'brand_filter': brand_filter
    })

def search_suggestions(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        product_matches = Product.objects.filter(name__icontains=query)[:6]
        category_matches = Category.objects.filter(name__icontains=query)[:4]

        results += [{'name': p.name, 'type': 'Product'} for p in product_matches]
        results += [{'name': c.name, 'type': 'Category'} for c in category_matches]

    return JsonResponse({'results': results})



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
    if product.stock < 1:
        messages.error(request, "This product is out of stock.")
        return redirect('app:products')
    cart , _ = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if cart_item.quantity < product.stock:
        cart_item.quantity += 1
    else:
        messages.warning(request, f"You've reached the maximum available stock for {product.name}.")

    
    if not created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f"{product.name} quantity updated in your cart.")
        else:
            messages.warning(request, f"You've reached the maximum available stock for {product.name}.")
    else:
        cart_item.quantity = 1
        cart_item.save()
        messages.success(request, f"{product.name} added to your cart.")

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
        user = request.user
        user.first_name = request.POST.get('full_name', '')
        user.phone = request.POST.get('phone', '')
        user.street = request.POST.get('street', '')
        user.city = request.POST.get('city', '')
        user.state = request.POST.get('state', '')
        user.zip_code = request.POST.get('zip_code', '')
        user.landmark = request.POST.get('landmark', '')
        user.save()
        # address = request.POST.get('address')
        full_address = f"{user.street}, {user.landmark}, {user.city}, {user.state} - {user.zip_code}"

        order = Order.objects.create(user=user, address=full_address, total=total)
        if not full_address:
            messages.error(request, "Address is required.")
            return redirect('checkout')
        
        if full_address and request.user.address != full_address:
            request.user.address = full_address
            request.user.save()

        # Create Order
        # order = Order.objects.create(user=request.user, address=address, total=total)

        for item in cart_items:
            if item.quantity > item.product.stock:
                messages.error(request, f"Not enough stock for {item.product.name}. Available: {item.product.stock}")
                return redirect('app:mycart')
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            item.product.stock -= item.quantity
            item.product.save()
            
        # Clear cart after order
        cart.items.all().delete()
        
        messages.success(request, "Order placed successfully!")
        return redirect('app:thank_you', order_id=order.id)
    
    return render(request, 'app/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })

    
    
    
    
@login_required
def my_orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_at')
    return render(request, 'app/myorders.html', {'orders': orders})


@login_required
def thank_you(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'app/thankyou.html', {'order': order})
    

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

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('app:user_details') 
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'app/edit_profile.html', {'form': form})
    
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
    sort_by = request.GET.get('sort', 'name')  # Default sort
    sort_options = {
        'price_asc': 'price',
        'price_desc': '-price',
        'name': 'name',
        'name_desc': '-name',
        'latest': '-id',
    }
    sort_field = sort_options.get(sort_by, 'name')

    product_list = Product.objects.all().order_by(sort_field)

    paginator = Paginator(product_list, 8)  # Show 8 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'sort': sort_by,
    }
    return render(request, 'app/products.html', context)


def details(request, product_id):
    product = get_object_or_404(Product, id=product_id) 
    reviews = Review.objects.filter(product=product) 
    form = ReviewForm()
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('app:details', product_id=product.id)
    else:
        form = ReviewForm()
        
    return render(request, 'app/details.html',
        {'product': product,
        'reviews': reviews,
        'form': form,
        'related_products': related_products})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    messages.success(request, 'Added to wishlist!')
    return redirect('app:details', product_id=product.id)

@login_required
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'app/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    messages.success(request, 'Removed from wishlist.')
    return redirect('app:view_wishlist')

