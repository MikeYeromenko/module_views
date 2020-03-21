from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import Group

from modshop.models import MyUser
from modshop import models


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['username', ]

    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        group = Group.objects.get(name='Users')
        if commit:
            user.save()
            user.groups.add(group)
        return user


class BuyingForm(forms.Form):
    quantity = forms.IntegerField(min_value=0, initial=1)


class GoodsUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Goods
        fields = ['title', 'description', 'price', 'quantity']

    def save(self, commit=True, user=None):
        goods_update = super(GoodsUpdateForm, self).save(commit=False)
        if user:
            goods_update.id_last_manager = user
        if commit:
            goods_update.save()
        return goods_update
