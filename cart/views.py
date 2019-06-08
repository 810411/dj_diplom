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
        customer_pk = request.user.customer.pk
        product_pk = request.GET.get('product_id')

        if f'customer-{customer_pk}' not in request.session:
            request.session[f'customer-{customer_pk}'] = {
                'cart': {}
            }

        customer_session = request.session.get(f'customer-{customer_pk}')

        if 'cart' in customer_session:
            cart = customer_session['cart']

            if product_pk not in cart:
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
    customer_pk = request.user.customer.pk

    context = {
        'next': next_,
    }

    customer_session = request.session.get(f'customer-{customer_pk}', None)

    if customer_session:
        cart = customer_session['cart']
        products = Product.objects.filter(pk__in=cart.keys())

        for key in cart.keys():
            cart[key]['product'] = products.get(pk=key)

        context['cart'] = cart

    return render(request, 'cart/cart.html', context)
