# Generated by Django 3.0.3 on 2020-03-18 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modshop', '0002_goods_goods_return_purchase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='wallet',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
    ]
