from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from module import settings


class MyUser(AbstractUser):
    # attribute for sum of money, the user has.
    wallet = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    last_login = models.DateTimeField(auto_now=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.wallet = settings.MONEY_WALLET
        return super(MyUser, self).save(*args, **kwargs)


class Goods(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    # image = models.ImageField(upload_to='goods_images/')
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    id_last_manager = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title


class Purchase(models.Model):
    id_user = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING)
    id_goods = models.ForeignKey(Goods, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()
    date_time = models.DateTimeField(auto_now_add=True, editable=False)
    was_returned = models.BooleanField(default=False)
    return_accepted = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f'{self.date_time.date()}'


class Goods_Return(models.Model):
    id_purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    id_admin = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, blank=True, null=True)

