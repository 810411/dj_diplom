# Generated by Django 2.2 on 2019-04-30 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20190430_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.URLField(default=False, verbose_name='Ссылка на изображение'),
        ),
    ]
