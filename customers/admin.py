from django.contrib import admin

from .models import Customer, Order, ProductsInOrder


class ProductsInOrderInline(admin.TabularInline):
    model = ProductsInOrder

    verbose_name = 'Заказанный товар'
    verbose_name_plural = 'Заказанные товары'


class OrderAdmin(admin.ModelAdmin):
    ordering = ('created',)
    list_display = ('customer', 'quantity', 'created', )

    inlines = (ProductsInOrderInline,)

    def quantity(self, obj):
        products = ProductsInOrder.objects.filter(order=obj)
        return len(products)

    quantity.short_description = 'Количество позиций'


admin.site.register(Order, OrderAdmin)
admin.site.register(Customer)
