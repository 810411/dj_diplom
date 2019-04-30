from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

from dj_diplom.views import get_menu
from products.models import Product
from customers.models import Customer
# from .models import Cart, ProductCountInCart


def customer_check(user):
    return Customer.objects.filter(user=user).first()


@login_required(login_url='login')
@user_passes_test(customer_check, login_url='login')
def create_or_update_cart_view(request):
    next_ = request.GET.get('next')

    if request.method == 'POST':
        customer_pk = request.user.customer.pk
        product_pk = request.GET.get('product_id')

        if f'customer-{customer_pk}' not in request.session.keys():
            request.session[f'customer-{customer_pk}'] = {
                'cart': {}
            }

        customer_session = request.session.get(f'customer-{customer_pk}')

        if 'cart' in customer_session.keys():
            cart = customer_session['cart']

            if product_pk not in cart.keys():
                cart[product_pk] = {
                    'quantity': 0
                }

            cart[product_pk]['quantity'] += 1

        else:
            customer_session['cart'] = {
                product_pk: {
                    'quantity': 1
                }
            }

        request.session.modified = True

    return redirect(next_)


@login_required(login_url='login')
@user_passes_test(customer_check, login_url='login')
def cart_view(request):
    next_ = request.GET.get('next')
    menu = get_menu()
    customer_pk = request.user.customer.pk

    context = {
        'next': next_,
        'menu': menu,
    }

    customer_session = request.session.get(f'customer-{customer_pk}', None)

    if customer_session:
        cart = customer_session['cart']

        for key in cart.keys():
            cart[key]['product'] = Product.objects.get(pk=key)

        context['cart'] = cart

    return render(request, 'cart/cart.html', context)


# @login_required(login_url='login')
# def create_cart_view(request):
#     next_ = request.GET.get('next')
#
#     if request.method == 'POST':
#         customer = request.user.customer
#         product_id = request.GET.get('product_id')
#
#         cart = Cart.objects.get_or_create(customer=customer)[0]
#         product = Product.objects.get(pk=product_id)
#
#         if ProductCountInCart.objects.filter(cart=cart, product=product).exists():
#             product_count_in_cart = ProductCountInCart.objects.get(cart=cart, product=product)
#             product_count_in_cart.quantity += 1
#             product_count_in_cart.save()
#
#         else:
#             ProductCountInCart.objects.create(cart=cart, product=product, quantity=1)
#
#     return redirect(next_)


# @login_required(login_url='login')
# def cart_view(request):
#     next_ = request.GET.get('next')
#     customer = request.user.customer
#     menu = get_menu()
#
#     context = {
#         'next': next_,
#         'menu': menu,
#     }
#
#     cart = Cart.objects.filter(customer=customer).first()
#     products_with_count = ProductCountInCart.objects.filter(cart=cart)
#
#     if cart:
#         context['cart'] = products_with_count
#
#     return render(request, 'cart/cart.html', context)
