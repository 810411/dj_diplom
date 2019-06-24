from django.shortcuts import render

from articles.models import Article


def home_view(request):
    articles = Article.objects.order_by('created')

    context = {
        'articles': articles,
    }

    return render(request, 'index.html', context)
