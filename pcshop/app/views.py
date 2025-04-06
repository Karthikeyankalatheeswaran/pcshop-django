from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Product,Category
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm

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
                auth_login(request, user)
                return redirect('app:base')  
        else:
            form = AuthenticationForm()

        return render(request, 'app/login.html', {'form': form})

def mycart(request):
    return render(request , 'app/mycart.html')

def register(request):
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user)
                return redirect('app:login')  
        else:
            form = CustomUserCreationForm()
        return render(request, 'app/register.html', {'form': form})

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



