from django.db import models
#
# from products.models import Product
# from customers.models import Customer
#
#
# class Cart(models.Model):
#     customer = models.OneToOneField(Customer, related_name='customer',
#                                     on_delete=models.CASCADE, verbose_name='Покупатель')
#     products = models.ManyToManyField(Product, verbose_name='Товары', blank=True, through='ProductCountInCart')
#
#     class Meta:
#         verbose_name = 'Корзина'
#         verbose_name_plural = 'Корзины'
#
#     def __str__(self):
#         return f'{self.pk} - {self.customer.email}'
#
#
# class ProductCountInCart(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')
#     product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар', related_name='count_in_cart',)
#     quantity = models.PositiveSmallIntegerField(verbose_name='Количество товара в корзине')
