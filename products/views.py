from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404


from dj_diplom.views import get_menu
from .models import Category, Product, Review
from .forms import ReviewForm


def product_list_view(request, section_slug=None, category_slug=None):
    menu = get_menu()
    products = Product.objects.all()
    category_name = 'Все товары'

    if section_slug and category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = category.products.all()
        category_name = category.name.capitalize()

    page = request.GET.get('page')
    paginator = Paginator(products, 6)
    products_paginate = paginator.get_page(page)

    context = {
        'menu': menu,
        'category_name': category_name,
        'products_paginate': products_paginate,
    }

    return render(request, 'products/product-list.html', context)


def product_view(request, section_slug=None, category_slug=None, slug=None):
    if section_slug and category_slug and slug:
        category = get_object_or_404(Category, slug=category_slug)
        product = get_object_or_404(category.products, slug=slug)
        menu = get_menu()
        reviews = product.reviews.all()
        name = request.user.username or None
        form = ReviewForm(initial={'name': name})

        for review_ in reviews:
            review_.rating_view = '\u2605' * review_.rating

        if request.method == 'POST':
            form = ReviewForm(request.POST or None)

            if form.is_valid():
                data = form.cleaned_data

                review = Review(
                    product=product,
                    name=data['name'],
                    content=data['content'],
                    rating=data['rating']
                )
                review.save()

                return redirect('product', product.category.section.slug, product.category.slug, product.slug)

        context = {
            'menu': menu,
            'product': product,
            'reviews': reviews,
            'form': form,
        }

        return render(request, 'products/product.html', context)
