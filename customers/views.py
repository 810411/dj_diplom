from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Customer, Order, ProductsInOrder
from products.models import Product
from .forms import CustomerLoginForm, CustomerRegisterForm


def login_view(request):
    form = CustomerLoginForm(request.POST or None)
    next_ = request.GET.get('next')
    print(next_)

    if form.is_valid():
        data = form.cleaned_data

        email = data['email']
        password = data['password']

        user = User.objects.get(email=email)
        username = user.username

        user = authenticate(username=username, password=password)

        login(request, user=user)
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or 'home'

        request.session['cart'] = {}

        return redirect(redirect_path)

    context = {'form': form}

    return render(request, 'customers/registration/login.html', context)


@login_required(login_url='login')
def logout_view(request):
    try:
        del request.session['cart']
    except KeyError:
        pass

    logout(request)
    return redirect('home')


def signup_view(request):
    if request.method == 'POST':
        register_form = CustomerRegisterForm(request.POST)

        if register_form.is_valid():
            register_form.save()
            return redirect('login')
    else:
        register_form = CustomerRegisterForm()

    context = {'form': register_form}

    return render(request, 'customers/registration/signup.html', context)


@login_required(login_url='login')
def order_view(request):
    if request.method == 'POST':
        customer_pk = request.user.customer.pk
        customer = Customer.objects.get(pk=customer_pk)

        cart = request.session['cart']

        if len(cart) > 0:
            order = Order.objects.create(customer=customer)

            for key, value in cart.items():
                product = Product.objects.get(pk=key)
                quantity = value['quantity']
                ProductsInOrder.objects.create(order=order, product=product, quantity=quantity)

            request.session['cart'] = {}
            request.session.modified = True

            messages.success(request, 'Заказ принят')

    return redirect('cart')
