from .models import Customer, Order

def get_cart_info(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(name=request.user.username)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    return items, order, cartItems