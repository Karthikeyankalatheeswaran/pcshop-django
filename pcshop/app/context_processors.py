from .models import CartItem, Cart

def cart_item_count(request):
    count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = CartItem.objects.filter(cart=cart).count()
        except Cart.DoesNotExist:
            count = 0
    return {'cart_item_count': count}