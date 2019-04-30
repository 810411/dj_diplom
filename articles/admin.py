from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')


admin.site.register(Article, ArticleAdmin)
