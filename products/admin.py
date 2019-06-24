from django.contrib import admin

from .models import Section, Category, Product, Review


class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'slug',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description', 'slug',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'rating', 'created')


admin.site.register(Section, SectionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
