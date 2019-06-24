from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .models import Category, Product, Review
from .forms import ReviewForm

PRODUCTS_PER_PAGE = 6


def product_list_view(request, section_slug=None, category_slug=None):
    products = Product.objects.all()
    category_name = 'Все товары'

    if section_slug and category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = list(category.products.all())
        category_name = category.name.capitalize()

    page = request.GET.get('page')
    paginator = Paginator(products, PRODUCTS_PER_PAGE)
    products_paginate = paginator.get_page(page)

    context = {
        'category_name': category_name,
        'products_paginate': products_paginate,
    }

    return render(request, 'products/product-list.html', context)


def product_view(request, section_slug, category_slug, slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(category.products, slug=slug)
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
                **data
            )
            review.save()

            return redirect('product', product.category.section.slug, product.category.slug, product.slug)

    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
    }

    return render(request, 'products/product.html', context)
