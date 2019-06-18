from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

from products.models import Product
from customers.models import Customer


def customer_check(user):
    return Customer.objects.filter(user=user).first()


@login_required(login_url='login')
@user_passes_test(customer_check, login_url='login')
def create_or_update_cart_view(request):
    next_ = request.GET.get('next')

    if request.method == 'POST':
        product_pk = request.GET.get('product_id')

        if 'cart' not in request.session:
            request.session['cart'] = {}

        cart = request.session.get('cart')

        if product_pk in cart:
            cart[product_pk]['quantity'] += 1

        else:
            cart[product_pk] = {
                'quantity': 1
            }

    request.session.modified = True

    return redirect(next_)


@login_required(login_url='login')
@user_passes_test(customer_check, login_url='login')
def cart_view(request):
    next_ = request.GET.get('next')

    context = {
        'next': next_,
    }

    cart = request.session.get('cart', None)

    if cart:
        products = {}
        product_list = Product.objects.filter(pk__in=cart.keys()).values('id', 'name', 'description')

        for product in product_list:
            products[str(product['id'])] = product

        for key in cart.keys():
            cart[key]['product'] = products[key]

        context['cart'] = cart

    return render(request, 'cart/cart.html', context)
