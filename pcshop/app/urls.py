from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'app'

urlpatterns = [
    path("", views.base, name="base"),
    path("search/", views.search, name="search"),
    path("index/", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("mycart/", views.mycart, name="mycart"),
    path("products/", views.products, name="products"),
    path('products/<int:product_id>/', views.details, name='details'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)