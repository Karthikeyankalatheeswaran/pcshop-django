from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'app'

urlpatterns = [
    path("", views.base, name="base"),
    path("search/", views.search, name="search"),
    path("index/", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("mycart/", views.mycart, name="mycart"),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/<str:action>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path("products/", views.products, name="products"),
    path('products/<int:product_id>/', views.details, name='details'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('user-details/', views.user_details, name='user_details'),
    path('logout/', views.logout_view, name='logout'),
    path('logout/', LogoutView.as_view(template_name='app/logout.html'), name='logout'),
    path('myorders/', views.my_orders_view, name='myorders'),
    path('user-details/edit/', views.edit_profile, name='edit_profile'),
    path('thankyou/<int:order_id>/', views.thank_you, name='thank_you'),
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)