# Generated by Django 3.0.3 on 2020-03-18 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modshop', '0003_auto_20200318_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='id_last_manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
