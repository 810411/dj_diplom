from django.shortcuts import render, redirect

from articles.models import Article
from products.models import Section


def get_menu():
    return Section.objects.all()


def home_view(request):
    menu = get_menu()
    articles = Article.objects.order_by('created')

    context = {
        'menu': menu,
        'articles': articles,
    }

    return render(request, 'index.html', context)
